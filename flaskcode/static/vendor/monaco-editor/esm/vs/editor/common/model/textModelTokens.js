/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/
import * as arrays from '../../../base/common/arrays.js';
import { onUnexpectedError } from '../../../base/common/errors.js';
import { LineTokens } from '../core/lineTokens.js';
import { Position } from '../core/position.js';
import { TokenizationRegistry } from '../modes.js';
import { nullTokenize2 } from '../modes/nullMode.js';
import { Disposable } from '../../../base/common/lifecycle.js';
import { StopWatch } from '../../../base/common/stopwatch.js';
import { MultilineTokensBuilder, countEOL } from './tokensStore.js';
import { setImmediate } from '../../../base/common/platform.js';
export class TokenizationStateStore {
    constructor() {
        this._beginState = [];
        this._valid = [];
        this._len = 0;
        this._invalidLineStartIndex = 0;
    }
    _reset(initialState) {
        this._beginState = [];
        this._valid = [];
        this._len = 0;
        this._invalidLineStartIndex = 0;
        if (initialState) {
            this._setBeginState(0, initialState);
        }
    }
    flush(initialState) {
        this._reset(initialState);
    }
    get invalidLineStartIndex() {
        return this._invalidLineStartIndex;
    }
    _invalidateLine(lineIndex) {
        if (lineIndex < this._len) {
            this._valid[lineIndex] = false;
        }
        if (lineIndex < this._invalidLineStartIndex) {
            this._invalidLineStartIndex = lineIndex;
        }
    }
    _isValid(lineIndex) {
        if (lineIndex < this._len) {
            return this._valid[lineIndex];
        }
        return false;
    }
    getBeginState(lineIndex) {
        if (lineIndex < this._len) {
            return this._beginState[lineIndex];
        }
        return null;
    }
    _ensureLine(lineIndex) {
        while (lineIndex >= this._len) {
            this._beginState[this._len] = null;
            this._valid[this._len] = false;
            this._len++;
        }
    }
    _deleteLines(start, deleteCount) {
        if (deleteCount === 0) {
            return;
        }
        if (start + deleteCount > this._len) {
            deleteCount = this._len - start;
        }
        this._beginState.splice(start, deleteCount);
        this._valid.splice(start, deleteCount);
        this._len -= deleteCount;
    }
    _insertLines(insertIndex, insertCount) {
        if (insertCount === 0) {
            return;
        }
        const beginState = [];
        const valid = [];
        for (let i = 0; i < insertCount; i++) {
            beginState[i] = null;
            valid[i] = false;
        }
        this._beginState = arrays.arrayInsert(this._beginState, insertIndex, beginState);
        this._valid = arrays.arrayInsert(this._valid, insertIndex, valid);
        this._len += insertCount;
    }
    _setValid(lineIndex, valid) {
        this._ensureLine(lineIndex);
        this._valid[lineIndex] = valid;
    }
    _setBeginState(lineIndex, beginState) {
        this._ensureLine(lineIndex);
        this._beginState[lineIndex] = beginState;
    }
    setEndState(linesLength, lineIndex, endState) {
        this._setValid(lineIndex, true);
        this._invalidLineStartIndex = lineIndex + 1;
        // Check if this was the last line
        if (lineIndex === linesLength - 1) {
            return;
        }
        // Check if the end state has changed
        const previousEndState = this.getBeginState(lineIndex + 1);
        if (previousEndState === null || !endState.equals(previousEndState)) {
            this._setBeginState(lineIndex + 1, endState);
            this._invalidateLine(lineIndex + 1);
            return;
        }
        // Perhaps we can skip tokenizing some lines...
        let i = lineIndex + 1;
        while (i < linesLength) {
            if (!this._isValid(i)) {
                break;
            }
            i++;
        }
        this._invalidLineStartIndex = i;
    }
    setFakeTokens(lineIndex) {
        this._setValid(lineIndex, false);
    }
    //#region Editing
    applyEdits(range, eolCount) {
        const deletingLinesCnt = range.endLineNumber - range.startLineNumber;
        const insertingLinesCnt = eolCount;
        const editingLinesCnt = Math.min(deletingLinesCnt, insertingLinesCnt);
        for (let j = editingLinesCnt; j >= 0; j--) {
            this._invalidateLine(range.startLineNumber + j - 1);
        }
        this._acceptDeleteRange(range);
        this._acceptInsertText(new Position(range.startLineNumber, range.startColumn), eolCount);
    }
    _acceptDeleteRange(range) {
        const firstLineIndex = range.startLineNumber - 1;
        if (firstLineIndex >= this._len) {
            return;
        }
        this._deleteLines(range.startLineNumber, range.endLineNumber - range.startLineNumber);
    }
    _acceptInsertText(position, eolCount) {
        const lineIndex = position.lineNumber - 1;
        if (lineIndex >= this._len) {
            return;
        }
        this._insertLines(position.lineNumber, eolCount);
    }
}
export class TextModelTokenization extends Disposable {
    constructor(_textModel, _languageIdCodec) {
        super();
        this._textModel = _textModel;
        this._languageIdCodec = _languageIdCodec;
        this._isScheduled = false;
        this._isDisposed = false;
        this._tokenizationStateStore = new TokenizationStateStore();
        this._tokenizationSupport = null;
        this._register(TokenizationRegistry.onDidChange((e) => {
            const languageId = this._textModel.getLanguageId();
            if (e.changedLanguages.indexOf(languageId) === -1) {
                return;
            }
            this._resetTokenizationState();
            this._textModel.clearTokens();
        }));
        this._register(this._textModel.onDidChangeContentFast((e) => {
            if (e.isFlush) {
                this._resetTokenizationState();
                return;
            }
            for (let i = 0, len = e.changes.length; i < len; i++) {
                const change = e.changes[i];
                const [eolCount] = countEOL(change.text);
                this._tokenizationStateStore.applyEdits(change.range, eolCount);
            }
            this._beginBackgroundTokenization();
        }));
        this._register(this._textModel.onDidChangeAttached(() => {
            this._beginBackgroundTokenization();
        }));
        this._register(this._textModel.onDidChangeLanguage(() => {
            this._resetTokenizationState();
            this._textModel.clearTokens();
        }));
        this._resetTokenizationState();
    }
    dispose() {
        this._isDisposed = true;
        super.dispose();
    }
    _resetTokenizationState() {
        const [tokenizationSupport, initialState] = initializeTokenization(this._textModel);
        this._tokenizationSupport = tokenizationSupport;
        this._tokenizationStateStore.flush(initialState);
        this._beginBackgroundTokenization();
    }
    _beginBackgroundTokenization() {
        if (this._isScheduled || !this._textModel.isAttachedToEditor() || !this._hasLinesToTokenize()) {
            return;
        }
        this._isScheduled = true;
        setImmediate(() => {
            this._isScheduled = false;
            if (this._isDisposed) {
                // disposed in the meantime
                return;
            }
            this._revalidateTokensNow();
        });
    }
    _revalidateTokensNow() {
        const textModelLastLineNumber = this._textModel.getLineCount();
        const MAX_ALLOWED_TIME = 1;
        const builder = new MultilineTokensBuilder();
        const sw = StopWatch.create(false);
        let tokenizedLineNumber = -1;
        do {
            if (sw.elapsed() > MAX_ALLOWED_TIME) {
                // Stop if MAX_ALLOWED_TIME is reached
                break;
            }
            tokenizedLineNumber = this._tokenizeOneInvalidLine(builder);
            if (tokenizedLineNumber >= textModelLastLineNumber) {
                break;
            }
        } while (this._hasLinesToTokenize());
        this._beginBackgroundTokenization();
        this._textModel.setTokens(builder.tokens, !this._hasLinesToTokenize());
    }
    tokenizeViewport(startLineNumber, endLineNumber) {
        const builder = new MultilineTokensBuilder();
        this._tokenizeViewport(builder, startLineNumber, endLineNumber);
        this._textModel.setTokens(builder.tokens, !this._hasLinesToTokenize());
    }
    reset() {
        this._resetTokenizationState();
        this._textModel.clearTokens();
    }
    forceTokenization(lineNumber) {
        const builder = new MultilineTokensBuilder();
        this._updateTokensUntilLine(builder, lineNumber);
        this._textModel.setTokens(builder.tokens, !this._hasLinesToTokenize());
    }
    getTokenTypeIfInsertingCharacter(position, character) {
        if (!this._tokenizationSupport) {
            return 0 /* Other */;
        }
        this.forceTokenization(position.lineNumber);
        const lineStartState = this._tokenizationStateStore.getBeginState(position.lineNumber - 1);
        if (!lineStartState) {
            return 0 /* Other */;
        }
        const languageId = this._textModel.getLanguageId();
        const lineContent = this._textModel.getLineContent(position.lineNumber);
        // Create the text as if `character` was inserted
        const text = (lineContent.substring(0, position.column - 1)
            + character
            + lineContent.substring(position.column - 1));
        const r = safeTokenize(this._languageIdCodec, languageId, this._tokenizationSupport, text, true, lineStartState);
        const lineTokens = new LineTokens(r.tokens, text, this._languageIdCodec);
        if (lineTokens.getCount() === 0) {
            return 0 /* Other */;
        }
        const tokenIndex = lineTokens.findTokenIndexAtOffset(position.column - 1);
        return lineTokens.getStandardTokenType(tokenIndex);
    }
    isCheapToTokenize(lineNumber) {
        if (!this._tokenizationSupport) {
            return true;
        }
        const firstInvalidLineNumber = this._tokenizationStateStore.invalidLineStartIndex + 1;
        if (lineNumber > firstInvalidLineNumber) {
            return false;
        }
        if (lineNumber < firstInvalidLineNumber) {
            return true;
        }
        if (this._textModel.getLineLength(lineNumber) < 2048 /* CHEAP_TOKENIZATION_LENGTH_LIMIT */) {
            return true;
        }
        return false;
    }
    _hasLinesToTokenize() {
        if (!this._tokenizationSupport) {
            return false;
        }
        return (this._tokenizationStateStore.invalidLineStartIndex < this._textModel.getLineCount());
    }
    _tokenizeOneInvalidLine(builder) {
        if (!this._hasLinesToTokenize()) {
            return this._textModel.getLineCount() + 1;
        }
        const lineNumber = this._tokenizationStateStore.invalidLineStartIndex + 1;
        this._updateTokensUntilLine(builder, lineNumber);
        return lineNumber;
    }
    _updateTokensUntilLine(builder, lineNumber) {
        if (!this._tokenizationSupport) {
            return;
        }
        const languageId = this._textModel.getLanguageId();
        const linesLength = this._textModel.getLineCount();
        const endLineIndex = lineNumber - 1;
        // Validate all states up to and including endLineIndex
        for (let lineIndex = this._tokenizationStateStore.invalidLineStartIndex; lineIndex <= endLineIndex; lineIndex++) {
            const text = this._textModel.getLineContent(lineIndex + 1);
            const lineStartState = this._tokenizationStateStore.getBeginState(lineIndex);
            const r = safeTokenize(this._languageIdCodec, languageId, this._tokenizationSupport, text, true, lineStartState);
            builder.add(lineIndex + 1, r.tokens);
            this._tokenizationStateStore.setEndState(linesLength, lineIndex, r.endState);
            lineIndex = this._tokenizationStateStore.invalidLineStartIndex - 1; // -1 because the outer loop increments it
        }
    }
    _tokenizeViewport(builder, startLineNumber, endLineNumber) {
        if (!this._tokenizationSupport) {
            // nothing to do
            return;
        }
        if (endLineNumber <= this._tokenizationStateStore.invalidLineStartIndex) {
            // nothing to do
            return;
        }
        if (startLineNumber <= this._tokenizationStateStore.invalidLineStartIndex) {
            // tokenization has reached the viewport start...
            this._updateTokensUntilLine(builder, endLineNumber);
            return;
        }
        let nonWhitespaceColumn = this._textModel.getLineFirstNonWhitespaceColumn(startLineNumber);
        const fakeLines = [];
        let initialState = null;
        for (let i = startLineNumber - 1; nonWhitespaceColumn > 1 && i >= 1; i--) {
            const newNonWhitespaceIndex = this._textModel.getLineFirstNonWhitespaceColumn(i);
            if (newNonWhitespaceIndex === 0) {
                continue;
            }
            if (newNonWhitespaceIndex < nonWhitespaceColumn) {
                initialState = this._tokenizationStateStore.getBeginState(i - 1);
                if (initialState) {
                    break;
                }
                fakeLines.push(this._textModel.getLineContent(i));
                nonWhitespaceColumn = newNonWhitespaceIndex;
            }
        }
        if (!initialState) {
            initialState = this._tokenizationSupport.getInitialState();
        }
        const languageId = this._textModel.getLanguageId();
        let state = initialState;
        for (let i = fakeLines.length - 1; i >= 0; i--) {
            const r = safeTokenize(this._languageIdCodec, languageId, this._tokenizationSupport, fakeLines[i], false, state);
            state = r.endState;
        }
        for (let lineNumber = startLineNumber; lineNumber <= endLineNumber; lineNumber++) {
            const text = this._textModel.getLineContent(lineNumber);
            const r = safeTokenize(this._languageIdCodec, languageId, this._tokenizationSupport, text, true, state);
            builder.add(lineNumber, r.tokens);
            this._tokenizationStateStore.setFakeTokens(lineNumber - 1);
            state = r.endState;
        }
    }
}
function initializeTokenization(textModel) {
    const languageId = textModel.getLanguageId();
    let tokenizationSupport = (textModel.isTooLargeForTokenization()
        ? null
        : TokenizationRegistry.get(languageId));
    let initialState = null;
    if (tokenizationSupport) {
        try {
            initialState = tokenizationSupport.getInitialState();
        }
        catch (e) {
            onUnexpectedError(e);
            tokenizationSupport = null;
        }
    }
    return [tokenizationSupport, initialState];
}
function safeTokenize(languageIdCodec, languageId, tokenizationSupport, text, hasEOL, state) {
    let r = null;
    if (tokenizationSupport) {
        try {
            r = tokenizationSupport.tokenize2(text, hasEOL, state.clone(), 0);
        }
        catch (e) {
            onUnexpectedError(e);
        }
    }
    if (!r) {
        r = nullTokenize2(languageIdCodec.encodeLanguageId(languageId), text, state, 0);
    }
    LineTokens.convertToEndOffset(r.tokens, text.length);
    return r;
}

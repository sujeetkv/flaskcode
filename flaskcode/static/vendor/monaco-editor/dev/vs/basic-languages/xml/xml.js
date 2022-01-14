/*!-----------------------------------------------------------------------------
 * Copyright (c) Microsoft Corporation. All rights reserved.
 * Version: 0.31.1(337587859b1c171314b40503171188b6cea6a32a)
 * Released under the MIT license
 * https://github.com/microsoft/monaco-editor/blob/main/LICENSE.txt
 *-----------------------------------------------------------------------------*/
define("vs/basic-languages/xml/xml",[],()=>{
var moduleExports = (() => {
  var __create = Object.create;
  var __defProp = Object.defineProperty;
  var __getOwnPropDesc = Object.getOwnPropertyDescriptor;
  var __getOwnPropNames = Object.getOwnPropertyNames;
  var __getProtoOf = Object.getPrototypeOf;
  var __hasOwnProp = Object.prototype.hasOwnProperty;
  var __markAsModule = (target) => __defProp(target, "__esModule", { value: true });
  var __commonJS = (cb, mod) => function __require() {
    return mod || (0, cb[Object.keys(cb)[0]])((mod = { exports: {} }).exports, mod), mod.exports;
  };
  var __export = (target, all) => {
    __markAsModule(target);
    for (var name in all)
      __defProp(target, name, { get: all[name], enumerable: true });
  };
  var __reExport = (target, module, desc) => {
    if (module && typeof module === "object" || typeof module === "function") {
      for (let key of __getOwnPropNames(module))
        if (!__hasOwnProp.call(target, key) && key !== "default")
          __defProp(target, key, { get: () => module[key], enumerable: !(desc = __getOwnPropDesc(module, key)) || desc.enumerable });
    }
    return target;
  };
  var __toModule = (module) => {
    return __reExport(__markAsModule(__defProp(module != null ? __create(__getProtoOf(module)) : {}, "default", module && module.__esModule && "default" in module ? { get: () => module.default, enumerable: true } : { value: module, enumerable: true })), module);
  };

  // build/fillers/monaco-editor-core-amd.ts
  var require_monaco_editor_core_amd = __commonJS({
    "build/fillers/monaco-editor-core-amd.ts"(exports, module) {
      module.exports = self.monaco;
    }
  });

  // src/basic-languages/xml/xml.ts
  var xml_exports = {};
  __export(xml_exports, {
    conf: () => conf,
    language: () => language
  });

  // src/fillers/monaco-editor-core.ts
  var monaco_editor_core_exports = {};
  __markAsModule(monaco_editor_core_exports);
  __reExport(monaco_editor_core_exports, __toModule(require_monaco_editor_core_amd()));

  // src/basic-languages/xml/xml.ts
  var conf = {
    comments: {
      blockComment: ["<!--", "-->"]
    },
    brackets: [["<", ">"]],
    autoClosingPairs: [
      { open: "<", close: ">" },
      { open: "'", close: "'" },
      { open: '"', close: '"' }
    ],
    surroundingPairs: [
      { open: "<", close: ">" },
      { open: "'", close: "'" },
      { open: '"', close: '"' }
    ],
    onEnterRules: [
      {
        beforeText: new RegExp(`<([_:\\w][_:\\w-.\\d]*)([^/>]*(?!/)>)[^<]*$`, "i"),
        afterText: /^<\/([_:\w][_:\w-.\d]*)\s*>$/i,
        action: {
          indentAction: monaco_editor_core_exports.languages.IndentAction.IndentOutdent
        }
      },
      {
        beforeText: new RegExp(`<(\\w[\\w\\d]*)([^/>]*(?!/)>)[^<]*$`, "i"),
        action: { indentAction: monaco_editor_core_exports.languages.IndentAction.Indent }
      }
    ]
  };
  var language = {
    defaultToken: "",
    tokenPostfix: ".xml",
    ignoreCase: true,
    qualifiedName: /(?:[\w\.\-]+:)?[\w\.\-]+/,
    tokenizer: {
      root: [
        [/[^<&]+/, ""],
        { include: "@whitespace" },
        [/(<)(@qualifiedName)/, [{ token: "delimiter" }, { token: "tag", next: "@tag" }]],
        [
          /(<\/)(@qualifiedName)(\s*)(>)/,
          [{ token: "delimiter" }, { token: "tag" }, "", { token: "delimiter" }]
        ],
        [/(<\?)(@qualifiedName)/, [{ token: "delimiter" }, { token: "metatag", next: "@tag" }]],
        [/(<\!)(@qualifiedName)/, [{ token: "delimiter" }, { token: "metatag", next: "@tag" }]],
        [/<\!\[CDATA\[/, { token: "delimiter.cdata", next: "@cdata" }],
        [/&\w+;/, "string.escape"]
      ],
      cdata: [
        [/[^\]]+/, ""],
        [/\]\]>/, { token: "delimiter.cdata", next: "@pop" }],
        [/\]/, ""]
      ],
      tag: [
        [/[ \t\r\n]+/, ""],
        [/(@qualifiedName)(\s*=\s*)("[^"]*"|'[^']*')/, ["attribute.name", "", "attribute.value"]],
        [
          /(@qualifiedName)(\s*=\s*)("[^">?\/]*|'[^'>?\/]*)(?=[\?\/]\>)/,
          ["attribute.name", "", "attribute.value"]
        ],
        [/(@qualifiedName)(\s*=\s*)("[^">]*|'[^'>]*)/, ["attribute.name", "", "attribute.value"]],
        [/@qualifiedName/, "attribute.name"],
        [/\?>/, { token: "delimiter", next: "@pop" }],
        [/(\/)(>)/, [{ token: "tag" }, { token: "delimiter", next: "@pop" }]],
        [/>/, { token: "delimiter", next: "@pop" }]
      ],
      whitespace: [
        [/[ \t\r\n]+/, ""],
        [/<!--/, { token: "comment", next: "@comment" }]
      ],
      comment: [
        [/[^<\-]+/, "comment.content"],
        [/-->/, { token: "comment", next: "@pop" }],
        [/<!--/, "comment.content.invalid"],
        [/[<\-]/, "comment.content"]
      ]
    }
  };
  return xml_exports;
})();
return moduleExports;
});

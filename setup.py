# -*- coding: utf-8 -*-
"""flaskcode module setup"""
from setuptools import setup
import flaskcode


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name=flaskcode.__title__,
    version=flaskcode.__version__,
    license=flaskcode.__license__,
    author=flaskcode.__author__,
    author_email=flaskcode.__email__,
    url=flaskcode.__uri__,
    description=flaskcode.__description__,
    long_description=readme(),
    long_description_content_type='text/markdown',
    packages=['flaskcode'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    keywords='flaskcode code editor code-editor',
    entry_points={
        'console_scripts': [
            'flaskcode = flaskcode.cli:main',
        ]
    },
    python_requires='>=2.7',
    install_requires=['Flask>=1.0.0'],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest>=4.5.0',
    ],
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Text Editors :: Text Processing',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)

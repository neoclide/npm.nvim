# Npm.nvim

[![](http://img.shields.io/github/issues/neoclide/npm.nvim.svg)](https://github.com/neoclide/denite-extra/issues)
[![](http://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![](https://img.shields.io/badge/doc-%3Ah%20npm.txt-red.svg)](doc/npm.txt)


Npm plugin to make vim user works with npm easier.

## Commands

* `Denite npm` show all npm packages of current project.
* `Denite func` show functions location using
  [parsefunc](https://github.com/chemzqm/parsefunc)
* `NpmInstall` run npm install command in nvim terminal.
* `NpmOutaded` show outdated npm packages info in denite interface.
* `NpmDev` show developing npm modules.
* `NpmRun [script]` run npm script in nvim terminal.
* `NpmSearch [name]` search npm package in browser
* TODO: `Denite npm/used` show all npm packages that you have ever been used.

For detail, see `:h npm.txt`

## Requirement

* node > 9.0
* python 3
* [neovim](https://github.com/neovim/neovim) > 0.2.2
* [denite.nvim](https://github.com/Shougo/denite.nvim)

## Installation

Firsly, copy file `rplugin/python3/denite/kind/npm.py` to `denite.nvim/rplugin/python3/denite/kind/npm.py`,
since denite doesn't support custom kind in separate plugins.

Take [vim-plug](https://github.com/junegunn/vim-plug) for example:

    Plug 'neoclide/npm.nvim' {'do' : 'npm install'}

Run command `:UpdateRemotePlugins` to regist this remote plugin if needed.

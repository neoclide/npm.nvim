'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = undefined;

var _dec, _dec2, _dec3, _dec4, _class, _desc, _value, _class2;

var _neovim = require('neovim');

var _pify = require('pify');

var _pify2 = _interopRequireDefault(_pify);

var _fs = require('fs');

var _fs2 = _interopRequireDefault(_fs);

var _path = require('path');

var _path2 = _interopRequireDefault(_path);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _applyDecoratedDescriptor(target, property, decorators, descriptor, context) {
  var desc = {};
  Object['ke' + 'ys'](descriptor).forEach(function (key) {
    desc[key] = descriptor[key];
  });
  desc.enumerable = !!desc.enumerable;
  desc.configurable = !!desc.configurable;

  if ('value' in desc || desc.initializer) {
    desc.writable = true;
  }

  desc = decorators.slice().reverse().reduce(function (desc, decorator) {
    return decorator(target, property, desc) || desc;
  }, desc);

  if (context && desc.initializer !== void 0) {
    desc.value = desc.initializer ? desc.initializer.call(context) : void 0;
    desc.initializer = undefined;
  }

  if (desc.initializer === void 0) {
    Object['define' + 'Property'](target, property, desc);
    desc = null;
  }

  return desc;
}

let NpmPlugin = (_dec = (0, _neovim.Plugin)({ dev: !!process.env.NVIM_NODE_HOST_DEBUG }), _dec2 = (0, _neovim.Autocmd)('BufEnter', {
  sync: false,
  pattern: 'package.json',
  eval: 'expand("<afile>:p")'
}), _dec3 = (0, _neovim.Function)('NpmPackages', { sync: true }), _dec4 = (0, _neovim.Function)('NpmScripts', { sync: true }), _dec(_class = (_class2 = class NpmPlugin {
  async onFileEnter(file) {
    let content = await (0, _pify2.default)(_fs2.default.readFile)(_path2.default.join(dir, 'package.json'), 'utf8');
    let obj = JSON.parse(content);
    let o = obj['dependencies'] || {};
    Object.keys(obj['devDependencies'] || {}).forEach(key => {
      o[key] = obj['devDependencies'][key];
    });
    // TODO insert into sql
  }

  async findDirectory() {
    let p = await this.nvim.eval('getcwd()');
    while (true) {
      if (!p || p == '/') break;
      let stat = await (0, _pify2.default)(_fs2.default.stat)(_path2.default.join(p, 'package.json'));
      if (stat.isFile()) {
        return p;
      }
      p = _path2.default.dirname(p);
    }
  }

  async loadPackageJson(dir) {
    let content = await (0, _pify2.default)(_fs2.default.readFile)(_path2.default.join(dir, 'package.json'), 'utf8');
    return JSON.parse(content);
  }

  async npmPackages() {
    let dir = await this.findDirectory();
    if (!dir) return [];
    let obj = await this.loadPackageJson(dir);
    let res = [];
    for (let key of ['devDependencies', 'dependencies']) {
      let o = obj[key];
      if (o) {
        for (let name of Object.keys(o)) {
          let f = _path2.default.join(dir, `node_modules/${name}/package.json`);
          let json = await (0, _pify2.default)(_fs2.default.readFile)(f, 'utf8');
          res.push({
            name,
            isDev: key === 'devDependencies',
            version: JSON.parse(json).version
          });
        }
      }
    }
    return res;
  }

  async npmScripts() {
    let dir = await this.findDirectory();
    if (!dir) return [];
    let obj = await this.loadPackageJson(dir);
    return obj['scripts'] || {};
  }
}, (_applyDecoratedDescriptor(_class2.prototype, 'onFileEnter', [_dec2], Object.getOwnPropertyDescriptor(_class2.prototype, 'onFileEnter'), _class2.prototype), _applyDecoratedDescriptor(_class2.prototype, 'npmPackages', [_dec3], Object.getOwnPropertyDescriptor(_class2.prototype, 'npmPackages'), _class2.prototype), _applyDecoratedDescriptor(_class2.prototype, 'npmScripts', [_dec4], Object.getOwnPropertyDescriptor(_class2.prototype, 'npmScripts'), _class2.prototype)), _class2)) || _class);
exports.default = NpmPlugin;
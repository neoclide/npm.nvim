import { Plugin, Function, Autocmd, Command } from 'neovim'
import pify from 'pify'
import fs from 'fs'
import path from 'path'

@Plugin({ dev: !!process.env.NVIM_NODE_HOST_DEBUG })
export default class NpmPlugin {

  async findDirectory() {
    let p = await this.nvim.eval('getcwd()')
    while(true) {
      if (!p || p == '/') break
      let stat = await pify(fs.stat)(path.join(p, 'package.json'))
      if (stat.isFile()) {
        return p
      }
      p = path.dirname(p)
    }
  }

  async loadPackageJson(dir) {
    let content = await pify(fs.readFile)(path.join(dir, 'package.json'), 'utf8')
    return JSON.parse(content)
  }

  @Function('NpmPackages', {sync: true})
  async npmPackages() {
    let dir = await this.findDirectory()
    if (!dir) return []
    let obj = await this.loadPackageJson(dir)
    let res = []
    for (let key of ['devDependencies', 'dependencies']) {
      let o = obj[key]
      if (o) {
        for (let name of Object.keys(o)) {
          let f = path.join(dir, `node_modules/${name}/package.json`)
          let json = await pify(fs.readFile)(f, 'utf8')
          res.push({
            name,
            isDev: key === 'devDependencies',
            version: JSON.parse(json).version
          })
        }
      }
    }
    return res
  }

  @Function('NpmUsedModules', {sync: true})
  async npmUsedModules() {
    // TODO: query all used modules
    return []
  }

  @Function('NpmScripts', {sync: true})
  async npmScripts() {
    let dir = await this.findDirectory()
    if (!dir) return []
    let obj = await this.loadPackageJson(dir)
    return obj['scripts'] || {}
  }
}

require = patchRequire(global.require)

env = "localdev"
settings = {
  localdev : "http://localhost:8080"
  gaedev : "http://dev-appupw.appspot.com"
}

if casper.cli.has('env')
  env = casper.cli.get('env')

exports.baseURL = ->
  baseURL = settings[env]
  return baseURL

exports.env = ->
  return env

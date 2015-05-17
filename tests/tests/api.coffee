system = require 'system'

# load global settings
settings = require '../helpers/settings'

casper.test.begin 'url shorten api', 9, (test) ->

  casper.thenOpen settings.baseURL() + "/api/v1/shorturls", ->
    test.assertHttpStatus 200

  # add entity by post
  casper.thenOpen settings.baseURL() + "/api/v1/shorturls",
    method: "post"
    data:
      long_url: "http://appu.pw/"
  , ->
    @echo "POST request has been sent."
    test.assertHttpStatus 201
    @echo @getPageContent()
    jsonData = JSON.parse(@getPageContent())
    test.assertEquals jsonData.status,"success","post request by session is success"

  casper.wait(1000)

  casper.thenOpen settings.baseURL() + "/api/v1/shorturls", ->
    test.assertHttpStatus 200
    jsonData = JSON.parse(@getPageContent())
    test.assertEquals jsonData['short_urls'][0].long_url,"http://appu.pw/"
    @thenOpen settings.baseURL() + "/api/v1/shorturls/"+jsonData['short_urls'][0].path,
      method: "delete"

  casper.thenOpen settings.baseURL() + "/api/apikey/list", ->
    test.assertHttpStatus 200
    @clickLabel "Create new entity"
    @waitForSelector "#f_description", ->
      @sendKeys("#f_description", "hoge")
      @clickLabel "Save"
      @waitForSelector "#createEntity"

  casper.wait(1000)

  casper.thenOpen settings.baseURL() + "/api/v1/apikeys", ->
    test.assertHttpStatus 200
    jsonData = JSON.parse(@getPageContent())
    phantom.clearCookies()
    @thenOpen settings.baseURL() + "/api/v1/shorturls", ->
      test.assertHttpStatus 400
    @thenOpen settings.baseURL() + "/api/v1/shorturls?key="+jsonData.api_keys[0], ->
      test.assertHttpStatus 200

  casper.run ->
    do test.done

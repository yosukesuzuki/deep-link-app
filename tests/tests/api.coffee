system = require 'system'

# load global settings
settings = require '../helpers/settings'

casper.test.begin 'url shorten api', 14, (test) ->

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
    test.assertEquals jsonData["short_urls"].length, 1
    test.assertEquals jsonData["short_urls"][0].long_url,"http://appu.pw/"
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
    @thenOpen settings.baseURL() + "/api/v1/shorturls?key="+jsonData.api_keys[0],
      method: "post"
      data:
        long_url: "http://appu.pw/hoge1"
    , ->
      @echo "POST request has been sent."
      @echo @getPageContent()
      test.assertHttpStatus 201
      @wait(1000)
    @thenOpen settings.baseURL() + "/api/v1/shorturls?key="+jsonData.api_keys[0], ->
      test.assertHttpStatus 200
      jsonDataUrls = JSON.parse(@getPageContent())
      test.assertEquals jsonDataUrls.short_urls.length, 1
      @thenOpen settings.baseURL() + "/api/v1/shorturls/"+jsonDataUrls.short_urls[0].path+"?key="+jsonData.api_keys[0],
        method: "delete"
      , ->
        test.assertHttpStatus 204
  casper.run ->
    do test.done

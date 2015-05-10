import json
import urllib
import urlparse
import urllib2
import addon_util


## Documentation for getJson.
#
#  Return Json from URL.
def getJson(url) :
	json_string = urllib2.urlopen(url).read()
	data = json.loads(json_string)
	addon_util.log_debug("getJson json_string : [%s]" %(json_string))
	return data

## Documentation for getJsonSiteMap.
#
#  Return SiteMap.
def getJsonSiteMap(host, port, name, id):
    url = 'http://'+host+':'+port+'/rest/sitemaps/'+name+'/'+id+'?type=json'
    addon_util.log_debug("getJsonSiteMap url : [%s]" %(url))
    return getJson(url)

## Documentation for getJsonItem.
#
#return Item
def getJsonItem(item) :
    global host,port
    url = 'http://'+host+':'+port+'/rest/items/'+item+'?type=json'
    addon_util.log_debug("getJsonItem url : [%s]" %(url))
    return getJson(url)

## Documentation for updateItem.
#
#return Item
def updateItem(item):
	data = item.typeItem.state
	url = item.typeItem.link
	addon_util.log_debug("updateItem request url : [%s] state:[%s]" %(url, item.typeItem.state))
	req = urllib2.Request(url, data, {'Content-Type': 'text/plain'})
	f = urllib2.urlopen(req)
	response = f.read()
	addon_util.log_debug("updateItem response [%s]" %(response))
	f.close()

class Item:
	def __init__(self, id, label, link):
		self.id=id
		self.label=label
		self.link=link

# state value : on/off
class Switch(Item):
	def __init__(self, state, id, label, link):
		Item.__init__(self, id, label, link)
		self.state=state

# roller shutter value : unitialized (-1), 0-100
class RollerShutter(Item):
	def __init__(self, state, id, label, link):
		Item.__init__(self, id, label, link)
		self.state=state
	
# number value : int (affichage)
class Number(Item):
	def __init__(self, state, id, label, link):
		Item.__init__(self, id, label, link)
		self.state=state

# contact value : open/close (affichage)
class Contact(Item):
	def __init__(self, state, id, label, link):
		Item.__init__(self, id, label, link)
		self.state=state
	
# dimmer value : unitialized (-1), 0-100
class Dimmer(Item):
	def __init__(self, state, id, label, link):
		Item.__init__(self, id, label, link)
		self.state=state
	
# color value : RGB (triple slider)
class Color(Item):
	def __init__(self, state, id, label, link):
		Item.__init__(self, id, label, link)
		self.state=state
	
# string value : string
class String(Item):
	def __init__(self, state, id, label, link):
		Item.__init__(self, id, label, link)
		self.state=state

# dateTime value : date
class DateTime(Item):
	def __init__(self, state, id, label, link):
		Item.__init__(self, id, label, link)
		self.state=state
		

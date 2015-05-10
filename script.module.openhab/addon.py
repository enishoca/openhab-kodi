import xbmc, xbmcplugin, xbmcgui, xbmcaddon, xbmc
import sys, os, os.path, traceback
import urllib2, urllib, urlparse
import json
import resources.lib.openhab as openhab
import resources.lib.gui as gui
import resources.lib.addon_util as addon_util

class Floor:
	## Constructor of Floor.
	#@param self The object pointer.
	#@param label The Floor label.
	#@param url The Floor url.
	#@param id The Floor id.
	#@param leaf If the Floor is a leaf.
	#@return Return a floor or room
	#
	#Used to save the floor and room list. If this is a room, the Floor is a leaf. 
    def __init__(self, label, url, id, leaf):
        self.label = label
        self.url = url
        self.id = id
        self.leaf = leaf


# To recover info of sentors
class openHabItem:
		## Constructor of openHabItem.
		#@param self The object pointer.
		#@param label The item label.
		#@param url The item url.
		#@param state the item state.
		#@param typeItem The type of item.
		#@param id The item id.
		#@return Return an openHab item
	def __init__(self, label, url, state, typeItem, id):
		self.typeItem = self.defItem(label, url, state, typeItem, id)
        
	## Documentation for defItem.
		#@param self The object pointer.
		#@param label The item label.
		#@param url The item url.
		#@param state the item state.
		#@param typeItem The type of item.
	#@param id The item id.
	#@return Return the correspondant typeItem - Item
	#
	#
	def defItem(self, label, link, state, typeItem, id):
		print(typeItem)
		if typeItem == "SwitchItem":
			return openhab.Switch(state, id, label, link)
		elif typeItem == "RollershutterItem":
			return openhab.RollerShutter(state, id, label, link)
		elif typeItem == "NumberItem":
			return openhab.Number(state, id, label, link)
		elif typeItem == "ContactItem":
			return openhab.Contact(state, id, label, link)
		elif typeItem == "DimmerItem":
			return openhab.Dimmer(state, id, label, link)
		elif typeItem == "ColorItem":
			return openhab.Color(state, id, label, link)
		elif typeItem == "DateTimeItem":
			return openhab.DateTime(state, id, label, link)
		else:
			return openhab.Switch(state, id, label, link)

####Functions ##########

## Documentation for createListingSite.
	#@param data.
	#@return Return the floor into list
#
#Create the floor list
def createListingSite(data):
	listing = []
	widgets1 = data['widget']
	widgets2 = []

	for w in widgets1:
		widgets2.append(w['widget'])

	for floor in widgets2[0]:
		tmp_floor = Floor(floor['label'],floor['item']['link'], floor['linkedPage']['id'], floor['linkedPage']['leaf'])
		listing.append(tmp_floor)

	return listing

## Documentation for createListingFloor.
	#@param data.
	#@return Return the room into list
#
#Create the room list
def createListingFloor(data):
	listing = []
	widgets = data['widget']

	for w in widgets:
			listing.append(Floor(w['label'],w['item']['link'], w['linkedPage']['id'], w['linkedPage']['leaf']))
	
	return listing

## Documentation for createListingSensorRoom.
	#@param data.
	#@return Return the room sensor into list
#
#Create the room sensor into list
def createListingSensorRoom(data):
    listing = []
    widgets = data['widget']

    if type(widgets) is list:
        for w in widgets:
            listing.append(openHabItem(w['label'],w['item']['link'], w['item']['state'], w['item']['type'], w['widgetId']))
    else :   
        listing.append(openHabItem(widgets['label'],widgets['item']['link'], widgets['item']['state'], widgets['item']['type'], widgets['widgetId']))

    return listing
     

#Main 
# Info global 

addon_util.log("Starting")
addon_util.log_debug("Debug Flag is true")
base_url = sys.argv[0]
thisPlugin = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

# Recuperation auto dans les settings de XBMC 
__addon__      = xbmcaddon.Addon()
host = __addon__.getSetting('host')
port = __addon__.getSetting('port')
name = __addon__.getSetting('name')
debug = __addon__.getSetting('debug')

id = __addon__.getSetting('id')
mode = args.get('mode', None)
langage = __addon__.getLocalizedString


# Navigation dans les menus
if mode is None:
	addon_util.log("Initializing - Main Menu")
	try:
		siteMap = openhab.getJsonSiteMap(host, port, name, id)
		listing = createListingSite(siteMap)
		for item in listing:
			if(item.leaf == 'false'):
				url = addon_util.build_url({'mode': 'floor', 'id': item.id},base_url)
				listItem = xbmcgui.ListItem(item.label)
				addon_util.log_debug("Adding Floor : [%s]" %(item.label))
				xbmcplugin.addDirectoryItem(handle=thisPlugin, url=url,listitem=listItem, isFolder=True)
			else:
				url = addon_util.build_url({'mode': 'room', 'id': item.id, 'label': item.label},base_url)
				listItem = xbmcgui.ListItem(item.label)
				addon_util.log_debug("Adding Room : [%s]" %(item.label))
				xbmcplugin.addDirectoryItem(handle=thisPlugin, url=url,listitem=listItem, isFolder=False)
		xbmcplugin.endOfDirectory(thisPlugin)
	except Exception as e:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exc()
		addon_util.parseError("Main Menu", e, type(e).__name__, langage)
		xbmc.executebuiltin("XBMC.StopScript("+__addon__.getAddonInfo('id')+")")

elif mode[0] == 'floor':
	addon_util.log("Floor")
	try:
		id = args['id'][0]
		addon_util.log_debug("Floor Id: [%s]" %(id))
		floor = openhab.getJsonSiteMap(host, port, name, id)
		listing = createListingFloor(floor)
		for item in listing:
			url = addon_util.build_url({'mode': 'room', 'id': item.id, 'label':item.label},base_url)
			listItem = xbmcgui.ListItem(item.label)
			xbmcplugin.addDirectoryItem(handle=thisPlugin, url=url,listitem=listItem, isFolder=False)
			addon_util.log_debug("Floor Item : [%s]" %(item.label))
		xbmcplugin.endOfDirectory(thisPlugin)
	except Exception as e:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exc()
		addon_util.parseError("Floor", e, type(e).__name__, langage)
		xbmc.executebuiltin("XBMC.StopScript("+__addon__.getAddonInfo('id')+")")

elif mode[0] == 'room':
	addon_util.log("Room")
	try:
		id = args['id'][0]
		label = args['label'][0]
		room = openhab.getJsonSiteMap(host, port, name, id)
		listing = createListingSensorRoom(room)
		addon_util.log_debug("Room Id: [%s] : [%s]" %(id, label))
		window = gui.RoomWindow(label, listing)
		window.doModal()
		del window
	except Exception as e:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		traceback.print_exc()
		addon_util.parseError("Floor", e, type(e).__name__, langage)
		xbmc.executebuiltin("XBMC.StopScript("+__addon__.getAddonInfo('id')+")")

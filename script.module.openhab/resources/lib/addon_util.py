import xbmcgui
import urllib
import xbmcaddon

## Documentation for raiseError.
	#@param exceptionType
	#@param langage : User language
#

#Display a dialog Error in XBMC
def parseError(location, exception, exceptionType, langage):
	errorId = 30004
	print exceptionType
	log_error("Exception Location: [%s] Type:[%s] Exception:[%s]" % (location, exceptionType, exception))
	if exceptionType == "URLError":
		errorId += 1
	if exceptionType == "HTTPError":
		errorId += 2
	xbmcgui.Dialog().ok("Error",langage(errorId))


## Documentation for log.
	#@param logText.
#
#Display a logText in XBMC log
def log(logText):
	print("[openHab] " + logText)

def log_debug(msg):
    if xbmcaddon.Addon().getSetting('debug') == 'true':
        print '[openHab] DEBUG: %s' % msg

def log_error(msg):
    print '[openHab] ERROR: %s' % msg


## Documentation for build_url.
	#@param query.
	#@return Return the room list
#
#Create a XBMC query
def build_url(query,base_url):
    return base_url + '?' + urllib.urlencode(query)
 

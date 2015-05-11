## Introduction
This is a Kodi (formerly known as xbmc) plugin for Openhab.  It allows users to control Openhab from within the Kodi environment.  The orignal project was created for xmbc originally created by a group RICM5 2014 students. The original page in French is located here http://air.imag.fr/index.php/Extensions_XBMC.

The code as it stands now is compatible with the Kodi (Helix) the current version at the time of writing this.

## Installation and Usage
1. [Download](https://raw.githubusercontent.com/enishoca/openhab-kodi/master/openHab-Kodi.1.0.2.zip) the current version or alternatively click on the the zip file link above - then right click on 'View Raw' link and save the file.  
**DO NOT use the zip downloaded with ZIP button on this page directly on Kodi,** it downloads the source tree which amd it does not have the correct sturcture to load as an addin.
2. install it as you would normally install Kodi addons. You will need to go in the setings menu and change the default settings for the addon to match your installation.

e.g.

1. Server IP address : 127.0.0.1
1. Server port : 8080 
1. Sitemap name : default
1. Start page : default <br>
   Look at the first line of your sitemap it should looks like this: <br>
```
  sitemap default label="My Sitemap"
```  
  This is the name betweeen 'sitemap' and 'label' - here it is default
1. Debug: Off 


##Limitations
Thic code is not very flexible in how it deals with layouts.  It expects items to be under groups, if you have controls directly inside frames this code will not run, it ignores text times such as dates, temperature etc that may be directly under frames but will break on switches dimmers etc if they are not in groups.  The workaround for this is to create a seperate sitemap that is compatible with this software.  This sitemap should have all the items inside groupds not directly in frames.   

##Screenshots from the original addin

[![Add-on Home](images/Screenshot_xbmcOpenhab_1.png)](images/Screenshot_xbmcOpenhab_1.png)
[![View Floors](images/Screenshot_xbmcOpenhab_2.png)](images/Screenshot_xbmcOpenhab_2.png)
[![View rooms](images/Screenshot_xbmcOpenhab_3.png)](images/Screenshot_xbmcOpenhab_3.png)
[![Details parts](images/Screenshot_xbmcOpenhab_4.png)](images/Screenshot_xbmcOpenhab_4.png)


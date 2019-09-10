import xbmcaddon
import xbmcgui
 
addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')
 
line1 = "Reboot Dev!"
line2 = "Reboot dev addon."
line3 = "For timed reboot of system."
 
xbmcgui.Dialog().ok(addonname, line1, line2, line3)

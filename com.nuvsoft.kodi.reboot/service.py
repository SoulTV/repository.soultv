import time
import xbmc
import xbmcaddon

if __name__ == '__main__':
        monitor = xbmc.Monitor()
        addon = xbmcaddon.Addon()
        while not monitor.abortRequested():
                #Sleep/wait for abort for 10 seconds
                if monitor.waitForAbort(10):
                        # Abort was requested while waiting. We should exit
                        break
                if addon.getSetting("reboot_time") == time.strftime("%H:%M"):
                        xbmc.restart()

#!/usr/bin/env python

import ConfigHandler
import foursquare
import pynotify
import urllib
import gtk
import os
from gtk import gdk

class FoursquareNotifier():

	_cfgHandler = None
	notifier = None
	poll_timer = None

	def __init__(self):
		self._cfgHandler = ConfigHandler.ConfigHandler()

		if not pynotify.init("Foursquare Notifier"):
			print "Unable to initialise notifier"
			exit(1)
		print self._cfgHandler.options

		# Set the process timeour for checking for new checkins
                self.poll_timer = gtk.timeout_add(self._cfgHandler.options["poll_timeout"], self.poll_for_checkins )


	def poll_for_checkins(self):
		""" 
		Get the latest set of checkins from the foursquare api 
		"""

		fapi = foursquare.Api()
		checkins = fapi.get_checkins(self._cfgHandler.options["foursquare_username"], self._cfgHandler.options["foursquare_password"])
		print checkins

		# check the date of the checkin .. if it is newer than the last update time then display
		for checkin in checkins["checkins"]:
			# check if we already have their avatar image otherwise get it
			avatar_filename = os.path.basename(checkin["user"]["photo"])
			if not os.path.isfile("cache/"+avatar_filename):
				image = urllib.URLopener()
				image.retrieve(checkin["user"]["photo"], "cache/"+avatar_filename)
			
			notifymsg = checkin["display"] + "\n" + checkin["created"] 
			if checkin.has_key("shout"):
				notifymsg = notifymsg + "\n\nShouted: \"" + checkin["shout"] + "\""
			n = pynotify.Notification("Foursquare Checkin", notifymsg)
			pixbuf_image = gtk.gdk.pixbuf_new_from_file("cache/"+avatar_filename)
			n.set_icon_from_pixbuf(pixbuf_image)
			n.set_timeout(3000)
			n.show()

		return True

def main():
	gtk.main()


if __name__ == "__main__":
	print "Starting Foursquare Notifier"

	fs = FoursquareNotifier()
	 
	main()


#!/usr/bin/python

import ConfigParser
import os
import sys

class ConfigHandler:

	# defaults for the actual config options
	options = { 'foursquare_username': None,
		    'foursquare_password': None,
		    'poll_timeout': 0
		  }

	# the config parser
	config = None

	# list of files that can contain configuration
	# ~/.fs-notifier.conf
	# ./fs-notifier.conf
	config_files = [
		os.path.expanduser( "~/.fs-notifier.conf" ),
		sys.path[0]+"/fs-notifier.conf"
		]

	#
	# Start of actual code
	#
	def __init__(self):
		""" initialise class, read the config from one of the files """
		self.loadConfig()

        def loadConfig( self ):
		""" Actual method for reading configuration from file """
                self.config = ConfigParser.RawConfigParser()

                configFiles = self.config.read( self.config_files )

                for key in self.options.keys():
                        if ( self.config.has_option( 'options', key ) ):
                                if ( type(self.options[key]) == int ):
                                        self.options[key] = self.config.getint( 'options', key )
                                else:
                                        self.options[key] = self.config.get( 'options', key ).replace( '"', '' )




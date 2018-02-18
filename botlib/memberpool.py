# -*- coding: utf-8 -*-
# memberpool.py
# Copyright (C) 2018 Too-Naive and contributors
#
# This module is part of lottery-bot-telgram and is released under
# the GPL v3 License: https://www.gnu.org/licenses/gpl-3.0.txt
from libpy.Config import Config
from libpy import Log
from threading import Lock

class memberpool:
	def __init__(self, location=Config.bot.member_store):
		self.WriteLock = Lock()
		self.fileLocation = location
		try:
			with open(self.fileLocation) as fin:
				self.members = eval(fin.read())
		except IOError:
			self.members = {}
	
	def write(self, user_id, user_name):
		Log.debug(2, 'user_id is {}', user_id)
		with memberpool.WriteLock:
			self.members[user_id] = user_name
			self.writeFile(self.members)
		Log.info('Write {} to database successful', user_id)

	def check(self, user_id):
		return user_id in self.members
	
	def delete(self, user_id):
		pass

	def writeFile(self):
		with open(self.fileLocation, 'w') as fout:
			fout.write(repr(self.members))

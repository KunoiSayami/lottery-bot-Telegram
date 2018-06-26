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
	def __init__(self, location=Config.bot.member_store, usage_str=''):
		self.WriteLock = Lock()
		self.fileLocation = location
		self.usage_str = usage_str
		try:
			with open(self.fileLocation) as fin:
				self.members = eval(fin.read())
		except IOError:
			self.members = {}
	
	def write(self, user_id, user_name):
		Log.debug(2, 'user_id is {}', user_id)
		with self.WriteLock:
			self.members.update({user_id : user_name})
			self.writeFile()
		Log.debug(2 ,'{}: Write {} to database successful', self.usage_str, user_id)

	def check(self, user_id):
		return user_id in self.members
	
	def delete(self, user_id):
		with self.WriteLock:
			self.members.pop(user_id)
			self.writeFile()
		Log.debug(2 ,'{}: Delete {} from database successful', self.usage_str, user_id)
		

	def writeFile(self):
		with open(self.fileLocation, 'w') as fout:
			fout.write(repr(self.members))

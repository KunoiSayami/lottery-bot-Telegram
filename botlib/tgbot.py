# -*- coding: utf-8 -*-
# tgbot.py
# Copyright (C) 2018 Too-Naive and contributors
#
# This module is part of lottery-bot-telgram and is released under
# the GPL v3 License: https://www.gnu.org/licenses/gpl-3.0.txt
from libpy.Config import Config
from libpy.TgBotLib import telepot_bot
from botlib.memberpool import memberpool
from libpy import DaemonThread as DThread
import traceback
from base64 import b64encode

def parse_name(entity):
	if 'last_name' in entity:
		return b64encode('{} {}'.format(entity['first_name'],entity['last_name']))
	else:
		return b64encode(entity['first_name'])

class DaemonThread(DThread):
	def __init__(self, target=None, args=()):
		def __run(target, args):
			try:
				target(*args)
			except:
				Log.error('Daemon thread raised exception: {}',
					traceback.format_exc())
		self._t = Thread(target=__run, args=(target or self.run, args))
		self._t.daemon = True


class tgbot(telepot_bot):
	def custom_init(*args, **kwargs):
		self.memberpool = memberpool()
		self.aftermemberpool = memberpool(Config.bot.other_store)

	def onMessage(self, msg):
		DaemonThread(self.onMessageEx,(msg,)).start()

	def onMessageEx(self, msg):
		content_type, chat_type, chat_id = self.glance(msg)
		if content_type == 'new_chat_member' and not self.aftermemberpool.check(msg['new_chat_participant']['id']):
			self.aftermemberpool.write(msg['new_chat_participant']['id'],'null')
		elif content_type == 'private' and chat_type == 'text':
			if self.bot.getChatMember(Config.bot.group_id, chat_id)['status'] not 'member':
				return
			elif msg['text'] == '/flag 233':
				if not self.memberpool.check(msg['from']['id']) and \
					not self.aftermemberpool.check(msg['from']['id']):
					self.memberpool.write(msg['from']['id'], parse_name)
					self.sendMessage(chat_id, 'Register successful, your *user_id* is `{}`'.format(chat_id),
						parse_mode='Markdown')

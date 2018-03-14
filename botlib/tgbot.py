# -*- coding: utf-8 -*-
# tgbot.py
# Copyright (C) 2018 Too-Naive and contributors
#
# This module is part of lottery-bot-telgram and is released under
# the GPL v3 License: https://www.gnu.org/licenses/gpl-3.0.txt
from libpy.Config import Config
from libpy.TgBotLib import telepot_bot
from botlib.memberpool import memberpool
from libpy import DaemonThread
import traceback
from base64 import b64encode,b64decode
from libpy import Log

def parse_name(entity):
	if 'last_name' in entity:
		return b64encode('{} {}'.format(entity['first_name'],entity['last_name']))
	else:
		return b64encode(entity['first_name'])

class tgbot(telepot_bot):
	def custom_init(self, *args, **kwargs):
		self.memberpool = memberpool(usage_str='Member')
		self.Accept_new_register = False
		self.aftermemberpool = memberpool(Config.bot.other_store, 'New/Ignore member')
		self.message_loop(self.onMessage)

	def onMessage(self, msg):
		try:
			content_type, chat_type, chat_id = self.glance(msg)
			if content_type == 'new_chat_member' and not self.aftermemberpool.check(msg['new_chat_participant']['id']):
				self.aftermemberpool.write(msg['new_chat_participant']['id'],'new')
			elif content_type == 'text' and chat_type == 'private':
				msgStr = msg['text']
				if chat_id == int(Config.bot.owner):
					if msgStr[:5] == '/send':
						self.sendMessage(Config.bot.group_id, msgStr[6:], parse_mode='Markdown')
					elif msgStr == '/len':
						self.sendMessage(chat_id, 'Current people length: {}'.format(len(self.memberpool.members)))
					elif msgStr[:4] == '/del':
						self.aftermemberpool.write(int(msgStr[5:]),'other')
						self.memberpool.delete(int(msgStr[5:]))
						self.sendMessage(chat_id, '`{}` deleted!'.format(msgStr[5:]),
							parse_mode='Markdown')
					elif msgStr == '/list':
						s = ''
						for k,v in self.memberpool.members.items():
							s += '`{}`: {}\n'.format(k,b64decode(v))
						self.sendMessage(chat_id, s, parse_mode='Markdown')
						del s
					elif msgStr == '/switch':
						self.Accept_new_register = False if self.Accept_new_register else True
						self.sendMessage(chat_id, 'Switch to {} successful'.format(self.Accept_new_register))
					elif msgStr == '/status':
						self.sendMessage(chat_id, 'Current status: {}'.format(self.Accept_new_register))
				elif self.bot.getChatMember(int(Config.bot.group_id), chat_id)['status'] != 'member':
					return
				elif msgStr == '/flag 233':
					if not self.memberpool.check(msg['from']['id']) and \
						not self.aftermemberpool.check(msg['from']['id']) and \
							self.Accept_new_register:
						self.memberpool.write(msg['from']['id'], parse_name(msg['from']))
						self.sendMessage(chat_id, 'Register successful, your *user_id* is `{}`'.format(chat_id),
							parse_mode='Markdown')
				elif msgStr == '/ping':
					if self.memberpool.check(msg['from']['id']):
						self.sendMessage(chat_id, 'You already registed')
					else:
						self.sendMessage(chat_id, 'Unregistered, please send me /flag with flag to register')
		except Exception:
			Log.warn('Raised exception: \n{}', traceback.format_exc())

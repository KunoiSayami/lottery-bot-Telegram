# -*- coding: utf-8 -*-
# main.py
# Copyright (C) 2018 Too-Naive and contributors
#
# This module is part of lottery-bot-telgram and is released under
# the GPL v3 License: https://www.gnu.org/licenses/gpl-3.0.txt
import time
import sys
from libpy import Log
from botlib.tgbot import tgbot

def main():
	Log.info('Strat initializing....')
	Log.info('Debug enable: {}',Log.get_debug_info()[0])
	Log.debug(1,'Debug level: {}',Log.get_debug_info()[1])
	tgbot()
	Log.info('Bot is now running!')
	while True:
		time.sleep(30)


def init():
	reload(sys)
	sys.setdefaultencoding('utf8')

if __name__ == '__main__':
	init()
	main()
# -*- coding: utf-8 -*-
# Random.py
# Copyright (C) 2018 Too-Naive and contributors
#
# This module is part of lottery-bot-telgram and is released under
# the GPL v3 License: https://www.gnu.org/licenses/gpl-3.0.txt
import random
from libpy.Config import Config
from libpy import Log
from base64 import b64decode
import sys
from botlib.memberpool import memberpool

random.seed()

class rand:
	def __init__(self):
		with open(Config.bot.member_store) as fin:
			self.member = eval(fin.read())
		self.l = [k for k,v in self.member.items()]
		self.winner = []

	def rand_list(self):
		z = []
		while len(self.l) > 0:
			z.append(self.l.pop(random.randint(0,len(self.l)-1)))
		self.l = z
	
	def start(self, times):
		Log.info('Start random process')
		for time in xrange(0,times):
			Log.info('Current group:{}',repr(self.l))
			r = random.randint(50000,99999)
			Log.info('Randomize list {} times', r)
			for x in xrange(0,r):
				self.rand_list()
			Log.info('Randomize done. Current group:{}',repr(self.l))
			result = self.l.pop(random.randint(0,len(self.l)-1))
			self.winner.append(result)
			Log.info('Round {} Winner is : {} (id:{})', time+1,
				b64decode(self.member.pop(result)),result)
		self.cleanup()

	def cleanup(self):
		Log.info('Runing cleanup(), this function will print winner list.')
		memberpoolx = memberpool(usage_str='Member')
		aftermemberpool = memberpool(Config.bot.other_store, 'New/Ignore member')
		for x in self.winner:
			Log.info('{} : {}', x, b64decode(memberpoolx.members[x]))
			memberpoolx.delete(x)
			aftermemberpool.write(x,'null')
		Log.info('All clean up!')

def main():
	s = rand()
	if len(sys.argv) == 1:
		s.start(5)
	elif len(sys.argv) == 2 and isinstance(sys.argv[1],int):
		s.start(int(sys.argv[1]))

def init():
	reload(sys)
	sys.setdefaultencoding('utf8')

if __name__ == '__main__':
	init()
	main()

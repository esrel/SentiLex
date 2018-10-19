# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys, os
import argparse
reload(sys).setdefaultencoding("utf-8")

class IoUtilities:
	'''
	Class for Input/Output Reading
	'''

	def __init__(self):
		'''
		Constructor
		'''

	def readLex(self, ifile):
		''' read lexicon from file (single column) '''
		return [line.strip() for line in ifile]

	def readColumns(self, ifile, sep='\t', seg=False):
		''' read several columns file '''
		lines  = self.readLex(ifile)
		fields = [line.split(sep) for line in lines]
		out  = []
		sent = []
		for l in fields:
			cnum = len(l)
			if seg:
				if cnum == 1 and l[0] == '' and sent:
					out.append(sent)
					sent = []
				else:
					sent.append(l)
			else:
				if cnum != 1 and l[0] != '':
					out.append(l)
		return out

	def getColumn(self, lst, cnum):
		''' get column by number '''
		return [e[cnum] for e in lst]

	def printColumns(self, segs, sep='\t'):
		''' print 2D list in CoNLL format '''
		for s in segs:
			for e in s:
				print sep.join(map(str, e))
			print '\n',

#----------------------------------------------------------------------#
if __name__ == "__main__":

	argpar = argparse.ArgumentParser(description='Input/Output Utilities')
	argpar.add_argument('-f', '--ifile', type=file)
	argpar.add_argument('-s', '--sep'  , type=str, default='\t')
	argpar.add_argument('--segment', action='store_true',  help='segmentation')
	args = argpar.parse_args()

	iou = IoUtilities()
	#lex = iou.readLex(args.ifile)
	lex = iou.readColumns(args.ifile, args.sep, args.segment)
	print lex

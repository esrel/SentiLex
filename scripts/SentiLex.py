# -*- coding: utf-8 -*-
#!/usr/bin/env python

from LexTagger import *
from IoUtilities import *
import string
import nltk
import sys, os
import argparse
reload(sys).setdefaultencoding("utf-8")

class SentiLex:
	""" Lexicon-based sentiment analysis """
	def __init__(self):
		''' constructor '''

	def scoreText(self, txt):
		''' scores aggregated tags '''
		ind_lst = [key for key in txt]
		scores  = []
		icoef = 1
		scoef = 1

		for i in sorted(ind_lst):
			if txt[i]['type'] == 'punct':
				icoef = 1
				scoef = 1
			elif txt[i]['type'] == 'iword':
				icoef = txt[i]['num']
			elif txt[i]['type'] == 'sword':
				scoef = txt[i]['num']
			elif txt[i]['type'] == 'pword':
				iscore = self.intensifyPolarity(txt[i]['num'], icoef)
				sscore = self.shiftPolarity(iscore, scoef)
				scores.append(sscore)
		return sum(scores)

	def getPunctIndex(self, lst):
		''' get punctuation indices '''
		return [i for i,j in enumerate(lst) if j in string.punctuation]

	def mkLex(self, cols):
		''' construct lexicon as dict: 2 columns '''
		lex = {}
		for e in cols:
			lex[e[0]] = float(e[1])
		return lex

	def intensifyPolarity(self, ival, coef):
		''' modify polarity: intensifiers '''
		if type(ival) == float:
			return ival * coef
		else:
			return ival

	def shiftPolarity(self, ival, coef):
		''' change polarity '''
		if type(ival) == float:
			return ival * coef
		elif type(ival) == str:
			if istr.lower() == 'negative':
				return 'positive'
			elif istr.lower() == 'positive':
				return 'negative'
			else:
				return ival
		else:
			return ival # just keep it as is

	def nom2num(self, istr):
		''' convert nominal polarity to numeric '''
		if istr.lower() == 'negative':
			return float(-1)
		elif istr.lower() == 'positive':
			return float(1)
		elif istr.lower() == 'neutral':
			return float(0)
		else:
			return float(0)

	def num2nom(self, inum):
		''' convert numeric polarity to nominal '''
		if inum > 0:
			return 'positive'
		elif inum < 0:
			return 'negative'
		else:
			return 'neutral'

	def tag_doc(self, tagger, doc, ldict, llist, wtype, out=None):
		''' tag document (as list) w.r.t. ldict & llist '''
		if not out:
			out = {}

		doc_tagged = tagger.tagList(doc, llist)
		doc_tokens = [tagger.genString(tagger.getTokens(i, doc)) for i in doc_tagged]
		doc_scored = [ldict[i] for i in doc_tokens]
		for i in range(len(doc_tagged)):
			ind = tagger.flattenList(doc_tagged[i])
			beg = ind[0]
			out[beg] = {'type':wtype, 'num':doc_scored[i], 'word':doc_tokens[i], 'span':ind}
		return out


#----------------------------------------------------------------------#
if __name__ == "__main__":

	argpar = argparse.ArgumentParser(description='Lexicon-based Sentiment Analysis')
	argpar.add_argument('-x', '--xfile', type=file) # file for tagging as instance per line (lemmas|tokens)
	argpar.add_argument('-p', '--pfile', type=file) # polarity lexicon
	argpar.add_argument('-s', '--sfile', type=file) # polarity shifters
	argpar.add_argument('-i', '--ifile', type=file) # polarity intensifiers
	argpar.add_argument('-d', '--dsep', type=str, default='..') #
	argpar.add_argument('-t', '--tsep', type=str, default=' ')  # +
	argpar.add_argument('-f', '--fsep', type=str, default='\t') #

	args = argpar.parse_args()

	tag = LexTagger(args.tsep, args.dsep)
	sal = SentiLex()
	iou = IoUtilities()

	# document per line (?)
	if args.xfile:
		docs = [line.strip().split() for line in args.xfile]
	else:
		# demo
		#doc_str = 'bene non perfetto , ma brutto brutto'
		doc_str = "It 's just a phase , try to distract yourself from cleanliness and keep occupied ; just sounds as though you 're bored and that 's all your mind can focus on , I may be wrong ."
		docs = [doc_str.split()]
		print doc_str

	# shifters
	if args.sfile:
		scol = iou.readColumns(args.sfile, args.fsep)
		sdict = sal.mkLex(scol)
		slist = tag.readLex(iou.getColumn(scol, 0))

	# intensifiers
	if args.ifile:
		icol = iou.readColumns(args.ifile, args.fsep)
		idict = sal.mkLex(icol)
		ilist = tag.readLex(iou.getColumn(icol, 0))

	# polarity
	if args.pfile:
		pcol = iou.readColumns(args.pfile, args.fsep)
		pdict = sal.mkLex(pcol)
		plist = tag.readLex(iou.getColumn(pcol, 0))

	for doc in docs:
		if doc:
			txt = {} # aggregate of all tags
			puncts = sal.getPunctIndex(doc)
			for p in puncts:
				txt[p] = {'type':'punct'}

			if args.sfile:
				txt = sal.tag_doc(tag, doc, sdict, slist, 'sword', txt)

			if args.ifile:
				txt = sal.tag_doc(tag, doc, idict, ilist, 'iword', txt)

			# will over-write previous tags
			if args.pfile:
				txt = sal.tag_doc(tag, doc, pdict, plist, 'pword', txt)

			score = sal.scoreText(txt)
			#print score
			#print txt
			print sal.num2nom(score)


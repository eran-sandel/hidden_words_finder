#!/usr/bin/python

import sys
import argparse
import re

global args
global dictionary

MIN_WORD_SIZE = 5
MAX_WORD_SIZE = 10
MAX_JUMP_SIZE = 18
MIN_JUMP_SIZE = 5

def debug():
	import ipdb
	ipdb.set_trace()

def add_args(parser):
	parser.add_argument('--input', '-i', action="store",  required=True, help='input file')
	parser.add_argument('--dict', '-d', action="store",  required=False, help='dictionary file. In not set, dictionary will be taken from input file')


def openfile(filename):
	try:
		filedesc = open(filename,"r")
	except:
		print("Filename doest exist")
		exit(0)
	return filedesc

#clean line from non alphabetic chars. Remove words with less than MIN_WORD_SIZE
def clean_dictionary_line(line):
	regex = re.compile('[^a-zA-Z]')
	#First parameter is the replacement, second parameter is your input string
	line = regex.sub(' ', line)
	line = line.split()
	line = [word.lower() for word in line if len(word)>=MIN_WORD_SIZE and len(word) <=MAX_WORD_SIZE]
	return line

def build_dictionary_from_input_file(filedesc):
	global dictionary
	#import ipdb
	#ipdb.set_trace()
	for line in filedesc:
		regex = re.compile('[^a-zA-Z]')
		#First parameter is the replacement, second parameter is your input string
		line = regex.sub(' ', line)
		line = clean_dictionary_line(line)
		
		dictionary = dictionary.union(set(line))
	filedesc.seek(0)

def build_dictionary_from_dict_file(filedesc):
	global dictionary
	dictionary = filedesc.read().lower().split()

def get_all_permutation_from_here(text,idx):
	words = []
	for jump in range(MIN_JUMP_SIZE,MAX_JUMP_SIZE+1):
		words.append(text[idx:idx+MAX_WORD_SIZE*jump:jump])
	return words

def clean_search_line(line):
	regex = re.compile('[^a-zA-Z]')
	#First parameter is the replacement, second parameter is your input string
	line = regex.sub('', line).lower()
	return line

def search_words_in_dict(words):
	jumpIdx = MIN_JUMP_SIZE
	#go over all the words found
	for word in words:
		#for each word get all the valid word lengths
		for word_size in range(MIN_WORD_SIZE,MAX_WORD_SIZE+1):
			if word[-1*word_size:] in dictionary:
				print "found word: "+ word[-1*word_size:] + ", jump: " + str(jumpIdx)
		jumpIdx+=1

def search_words(filedesc):
	text = filedesc.read()
	text = clean_search_line(text)
	idx = 0
	for c in text:
		words = get_all_permutation_from_here(text,idx)
		search_words_in_dict(words)
		idx+=1

if __name__ == "__main__":
	global args
	global dictionary

	dictionary = set()
	parser = argparse.ArgumentParser(description='Pattern finder')
	add_args(parser)
	args = parser.parse_args()
	filedesc = openfile(args.input)

	#get dictionary
	if args.dict is not None:
		dictdesc = openfile(args.dict)
		build_dictionary_from_dict_file(dictdesc)
	else:
		build_dictionary_from_input_file(filedesc)
	print "dictionary length is: "+ str(len(dictionary))

	search_words(filedesc)

#!/usr/bin/python

import sys
import argparse
import re

global args
global dictionary
global active_words

# All words with length N. 
#on each column replace letter in +1 position with the current letter.
#i.e if the current letter is "c", row 2 will look:
# ['caa', 'aca', 'aac']

#active_words:
# ['a']
# ['aa', 'aa']
# ['aaa', 'aaa', 'aaa']
# ['aaaa', 'aaaa', 'aaaa', 'aaaa']
# ['aaaaa', 'aaaaa', 'aaaaa', 'aaaaa', 'aaaaa']

MIN_WORD_SIZE = 3
MAX_WORD_SIZE = 5
MAX_JUMP_SIZE = 6

NUM_OF_WORDS_INDEXES = MAX_WORD_SIZE-MIN_WORD_SIZE+1

def debug():
	import ipdb
	ipdb.set_trace()

def add_args(parser):
	parser.add_argument('--input', '-i', action="store",  required=True, help='input file')


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

def build_dictionary(filedesc):
	global dictionary
	#import ipdb
	#ipdb.set_trace()
	for line in filedesc:
		regex = re.compile('[^a-zA-Z]')
		#First parameter is the replacement, second parameter is your input string
		line = regex.sub(' ', line)
		line = clean_dictionary_line(line)
		
		dictionary = dictionary.union(set(line))

def print_active_words(text=""):
	global active_words
	print text
	for i in range(0,NUM_OF_WORDS_INDEXES):
		print active_words[i]

#init the active active_words list
def init_active_words():
	global active_words
	active_words = []
	for i in range(0,NUM_OF_WORDS_INDEXES):
		row = ["***" for j in range(0,MAX_WORD_SIZE)]
		active_words.append(row)

	for i in range(0,NUM_OF_WORDS_INDEXES):
		for j in range(0,i+MIN_WORD_SIZE):
			active_words[i][j] = '_'*(MIN_WORD_SIZE+i)

	print_active_words("init is:")

def clean_search_line(line):
	regex = re.compile('[^a-zA-Z]')
	#First parameter is the replacement, second parameter is your input string
	line = regex.sub(' ', line)
	line = line.lower()
	return line

def search_active_words_in_dict(line):
	global dictionary
	global active_words

	for i in range(0,NUM_OF_WORDS_INDEXES):
		last_word_idx = i+MIN_WORD_SIZE-1
		print last_word_idx
		if active_words[i][last_word_idx] in dictionary:
			print "found word: "+ active_words[i][last_word_idx]
			print line
		#remove last element in the list
		active_words[i].pop(last_word_idx)
		#instead insert a new element and start building a new word
		new_str = (i+MIN_WORD_SIZE)*"_"
		active_words[i] = [new_str]+active_words[i]
	print_active_words()

def update_active_words(c):
	for i in range(0,NUM_OF_WORDS_INDEXES):
		for j in range(0,i+MIN_WORD_SIZE):
			active_words[i][j] = active_words[i][j][1:]+c
	print c + ":"
	print_active_words()

def search_words(filedesc):
	filedesc.seek(0)
	for line in filedesc:
		line = clean_search_line(line)
		for c in line:
			if c.isalpha():
				update_active_words(c)
				print("active_words")
				search_active_words_in_dict(line)


if __name__ == "__main__":
	global args
	global dictionary

	dictionary = set()
	parser = argparse.ArgumentParser(description='Pattern finder')
	add_args(parser)
	args = parser.parse_args()
	filedesc = openfile(args.input)
	init_active_words()
	# search_active_words_in_dict("e")
	# search_active_words_in_dict("r")
	# search_active_words_in_dict("a")
	# search_active_words_in_dict("n")
	# search_active_words_in_dict("h")
	# search_active_words_in_dict(33)
	# update_active_words("o")
	# search_active_words_in_dict(33)
	# update_active_words("w")
	# search_active_words_in_dict(33)
	# update_active_words("a")
	# search_active_words_in_dict(33)
	# update_active_words("r")
	# search_active_words_in_dict(33)
	# update_active_words("e")
	# search_active_words_in_dict(33)
	# update_active_words("u")
	# search_active_words_in_dict(33)

	build_dictionary(filedesc)
	search_words(filedesc)
	print len(dictionary)
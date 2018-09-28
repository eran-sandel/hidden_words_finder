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

def print_active_words():
	global active_words
	for i in range(0,MAX_WORD_SIZE):
		print active_words[i][:i+1]

#init the active active_words list
def init_active_words():
	global active_words
	active_words = []
	for i in range(0,MAX_WORD_SIZE):
		row = ["" for j in range(0,MAX_WORD_SIZE)]
		active_words.append(row)

	for i in range(0,MAX_WORD_SIZE):
		for j in range(0,i+1):
			active_words[i][j] = ' '*(i+1)

def clean_search_line(line):
	regex = re.compile('[^a-zA-Z]')
	#First parameter is the replacement, second parameter is your input string
	line = regex.sub(' ', line)
	line = line.lower()
	return line

def search_words_in_dict(line):
	global dictionary
	global active_words

	for i in range(0,MAX_WORD_SIZE):
		if active_words[0] in dictionary:
			print active_words[0]
			print line

def update_active_words(c,index):
	for i in range(0,MAX_WORD_SIZE_TO_SEARCH):
		active_words[i] = active_words[i][1:]+c
	print active_words

def search_words(filedesc):
	filedesc.seek(0)
	letter_index = 0
	for line in filedesc:
		line = clean_search_line(line)
		for c in line:
			letter_index+=1
			update_active_words(c,letter_index)
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
	update_active_words("a")
	build_dictionary(filedesc)
	search_words(filedesc)
	print len(dictionary)
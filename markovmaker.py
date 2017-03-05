#!/usr/bin/env python
# coding=utf-8

"""
This is my attempt to generate text or names using Markov chains
"""

import argparse
import codecs
from nltk.tokenize import sent_tokenize, word_tokenize
import random


def get_arguments():
	"""
	Gets all of the possible arguments
	Right now the point is to be able to distinguish between word-level chains and
	text-level
	Other things to add in:
	-scan folders
	"""
	parser = argparse.ArgumentParser()

	parser.add_argument('-t', action='store_const', dest='analyze_level', const='text',
				help="Markov model at a text-level")

	parser.add_argument('-w', action="store_const", dest='analyze_level', const='word',
				help="Markov model at a word-level")
	parser.add_argument('file_name', action='store', help="This is the name of the file")

	
	return parser.parse_args()


def text_tokenizer(text_line):
	"""
	This tokenizes text.
	First it breaks the text into sentences
	Then into tokens
	"""
	final_list = ['<p>']

	sentences = sent_tokenize(text_line)

	for sentence in sentences:
		# I can't rstrip because newlines indicate paragraphs
		if sentence == '\n':
			pass
		else:
			final_list = final_list + word_tokenize(sentence)
	final_list.append("<p>")

	return tuple(final_list)

def text_analyzer(file_name):
	"""
	Reads and tokenizes text. Returns a list. Each paragraph is a list. And each sentence is a list.
	"""
	print "Reading file.\n"
	with codecs.open(file_name, 'r', 'utf-8') as open_text:
	
		print "file opened\n"

		paragraphs_list = []

		for line in open_text:
			if line.startswith("#"):
				# meta-info is behind the octothorp
				pass
			elif line == "\n":
				pass
			else:
				# here we receive a tuple of tuples of the sentences
				tokenized_paragraph = text_tokenizer(line)
				if len(tokenized_paragraph) > 1:
					paragraphs_list.append(tokenized_paragraph)

	return tuple(paragraphs_list)

def create_markov_matrix(input_text):
	"""
	This creates a matrix/dictionary where each word appearing in the text is a key.
	The value is another dictionary where each key is a word following the word, and the value
	is the number of times it occurs following.
	"""
	markov_matrix = {}

	# going through each paragraph/word
	for unit in input_text:
		# going through each word/letter
		for count, token in enumerate(unit):
			# add to dictionary if not in it
			if token not in markov_matrix:
				markov_matrix[token] = {}

			# add to the next word's count
			try:
				if unit[count + 1] not in markov_matrix[token]:
					markov_matrix[token][unit[count+1]] = 1
				else:
					markov_matrix[token][unit[count+1]] += 1
			except IndexError:
				pass

	return markov_matrix

def choose_next(choices):
	choice_list = []
	for thing in choices:
		choice_list = choice_list + [thing] * choices[thing]

	return random.choice(choice_list)

def create_text(parameter, matrix):
	"""
	A text creator. Returns a unit of text as indicated by the parameter
	"""

	end_of_file_terms = (".", "<p>", "!")
	chosen = False
	while chosen == False:
		first_word = choose_next(matrix["."])
		if first_word != '<p>':
			chosen = True

	sent = []
	sent.append(first_word)

	end_of_file = False
	seed_word = first_word

	while end_of_file == False:
		next_word = choose_next(matrix[seed_word])
		sent.append(next_word)
		if next_word in end_of_file_terms:
			end_of_file = True
		else:
			seed_word = next_word

	return sent
		
		

def main(args):
	
	to_markov = []
	if args.analyze_level=='text':

		# tokenize and clean text
		to_markov = text_analyzer(args.file_name)
	else:
		print "Sorry, I haven't gotten to that yet."
		quit()

	markov_matrix = create_markov_matrix(to_markov)
	end_parameter = "s"
	markoved =  create_text(end_parameter, markov_matrix)
	print " ".join(markoved)




if __name__ == "__main__":
	args = get_arguments()

	if args.analyze_level == None:
		print 'You need to specify a level to analyze. Please use the "-h" flag to see your options'
	else:
		main(args)

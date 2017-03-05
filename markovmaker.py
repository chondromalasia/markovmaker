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

def order_one_create_markov_matrix(input_text):
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

def order_two_create_markov_matrix(input_text):
	markov_matrix = {}
	for unit in input_text:
		for count, token in enumerate(unit):
			if count == 0:
				pass
			else:
				try:
					to_test = (token, unit[count+1])
					if to_test not in markov_matrix:
						markov_matrix[to_test] = {}

					if unit[count+2] not in markov_matrix[to_test]:
						markov_matrix[to_test][unit[count+2]] = 1
					else:
						markov_matrix[to_test][unit[count+2]] += 1
				except IndexError:
					pass

	return markov_matrix

def choose_next(choices):
	choice_list = []
	for thing in choices:
		choice_list = choice_list + [thing] * choices[thing]

	return random.choice(choice_list)

def create_text(parameter, unigrams, bigrams):
	"""
	A text creator. Returns a unit of text as indicated by the parameter
	"""

	end_of_file_terms = (".", "<p>", "!", "?")
	chosen = False
	while chosen == False:
		# make a list of seed words for the first word
		# you need to streamline this once going to third order
		final_dict = unigrams["."]
		for entity in unigrams["<p>"]:
			if entity in final_dict:
				final_dict[entity] += unigrams["<p>"][entity]
			else:
				final_dict[entity] = unigrams["<p>"][entity]

		first_word = choose_next(final_dict)
		if first_word != '<p>':
			chosen = True

	sent = []
	sent.append(first_word)

	end_of_file = False
	seed_word = first_word

	# now we do the second word
	seed_words = unigrams[seed_word]
	for word_pair in (("<p>", first_word), (".", first_word)):
		if word_pair in bigrams:
			for thing in bigrams[word_pair]:
				# bigrams are weighted by 4
				seed_words[thing] += (bigrams[word_pair][thing] * 4)
				
	sent.append(choose_next(seed_words))

	last_word = seed_word
	seed_word = sent[1]

	# the rest of the sentence
	while end_of_file == False:

		final_dict = unigrams[seed_word]
		bigram = (last_word, seed_word)

		if bigram in bigrams:
			for word in bigrams[bigram]:
				final_dict[word] += (bigrams[bigram][word] * 4)

		next_word = choose_next(final_dict)
		sent.append(next_word)

	
		if next_word in end_of_file_terms:
			end_of_file = True
		else:
			last_word = seed_word
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

	markov_matrix_one = order_one_create_markov_matrix(to_markov)
	markov_matrix_two = order_two_create_markov_matrix(to_markov)
	end_parameter = "s"
	markoved =  create_text(end_parameter, markov_matrix_one, markov_matrix_two)
	print ' '.join(markoved)




if __name__ == "__main__":
	args = get_arguments()

	if args.analyze_level == None:
		print 'You need to specify a level to analyze. Please use the "-h" flag to see your options'
	else:
		main(args)

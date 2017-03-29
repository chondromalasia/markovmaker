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

def normalizer(to_normalize):
	"""
	Normalizes text. Right now we're going to deal with contractions and lowercasing
	This may be optional depending on the size of the corpus
	"""

	for count, word in enumerate(to_normalize):
		if "'" in word:
			if word == "n't":
				to_normalize[count] = "not"
			elif word == "'re":
				to_normalize[count] = "are"
			elif word == "'ll":
				to_normalize[count] = "will"
			elif word == "'ve":
				to_normalize[count] = "have"
			elif word == "'m":
				to_normalize[count] = "am"
		else:
			to_normalize[count] = word.lower()

	return to_normalize

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

	final_list = normalizer(final_list)

	return tuple(final_list)

def text_analyzer(file_name):
	"""
	Reads and tokenizes text. Returns a list. Each paragraph is a list. And each sentence is a list.
	"""
	print "Reading file.\n"
	with codecs.open(file_name, 'r', 'utf-8') as open_text:
	
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
	print 'Creating order one matrix\n'

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
	print 'Creating order two matrix\n'
	markov_matrix = {}
	for unit in input_text:
		for count, token in enumerate(unit):
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

def order_three_create_markov_matrix(input_text):
	print 'Creating order three matrix\n'

	markov_matrix = {}
	for unit in input_text:
		for count, token in enumerate(unit):
			try:
				to_test = (token, unit[count+1], unit[count+2])

				# this should be its own function, in all examples
				if to_test not in markov_matrix:
					markov_matrix[to_test] = {}

				if unit[count+3] not in markov_matrix[to_test]:
					markov_matrix[to_test][unit[count+3]] = 1
				else:
					markov_matrix[to_test][unit[count+3]] += 1
			except IndexError:
				pass

	return markov_matrix

def order_four_create_markov_matrix(input_text):
	print 'Creating order four matrix\n'

	markov_matrix = {}

	for unit in input_text:
		for count, token in enumerate(unit):

			try:
				to_test = (token, unit[count+1], unit[count+2], unit[count+3])

				# creates the new 4-gram
				if to_test not in markov_matrix:
					markov_matrix[to_test] = {}

				# adds the next letter, if it's not there
				if unit[count+4] not in markov_matrix[to_test]:
					markov_matrix[to_test][unit[count+4]] = 1
				else:
					markov_matrix[to_test][unit[count+4]] += 1
			except IndexError:
				pass


	return markov_matrix

def order_five_create_markov_matrix(input_text):
	print 'Creating order five matrix\n'

	markov_matrix = {}

	for unit in input_text:
		for count, token in enumerate(unit):

			try:
				to_test = (token, unit[count+1], unit[count+2], unit[count+3], unit[count+4])

				if to_test not in markov_matrix:
					markov_matrix[to_test] = {}

				if unit[count+5] not in markov_matrix[to_test]:
					markov_matrix[to_test][unit[count+5]] = 1
				else:
					markov_matrix[to_test][unit[count+5]] +=1

			except IndexError:
				pass

	return markov_matrix

def weight_ngram(the_word_list, the_ngrams, the_ngram):
	weight = 4 ** (len(the_ngram) - 1)
	if the_ngram in the_ngrams:
		for word in the_ngrams[the_ngram]:
			the_word_list[word] += (the_ngrams[the_ngram][word] * weight)

	return the_word_list

		
def choose_next(choices):
	"""
	The way it makes a list where the word appears a weighted number of times, to reflect
	its weighting
	It comes into here weighted based on n-grams
	"""
	choice_list = []
	for thing in choices:
		choice_list = choice_list + [thing] * (choices[thing])

	return random.choice(choice_list)

def create_text(parameter, unigrams, bigrams, trigrams, fourgrams, fivegrams):
	"""
	A text creator. Returns a unit of text as indicated by the parameter
	It is much larger than I thought it would be, could use some cleaning up
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

	# advance
	last_word = seed_word
	seed_word = sent[1]

	# third word
	seed_words = unigrams[seed_word]
	bigram = (last_word, seed_word)

	# weight for bigrams
	seed_words = weight_ngram(seed_words, bigrams, bigram)
	
	# weight for trigrams
	trigrams_to_test = (("<p>", last_word, seed_word), (".", last_word, seed_word))
	for trigram in trigrams_to_test:
		if trigram in trigrams:
			for series in trigrams[trigram]:
				seed_words[series] += (trigrams[trigram][series] * 16)

	sent.append(choose_next(seed_words))


	# advance
	third_word = sent[0] 
	second_word = sent[1]
	seed_word = sent[2]

	# fourth word
	seed_words = unigrams[seed_word]
	bigram = (second_word, seed_word)
	
	# weighted bigrams
	seed_words = weight_ngram(seed_words, bigrams, bigram)

	# weighted trigrams
	trigram_to_test = (third_word, second_word, seed_word)
	seed_words = weight_ngram(seed_words, trigrams, trigram_to_test)

	# weighted 4grams
	fourgrams_to_test = (("<p>", third_word, second_word, seed_word), 
				(".", third_word, second_word, seed_word))
	for fourgram in fourgrams_to_test:
		if fourgram in fourgrams:
			for word in fourgrams[fourgram]:
				seed_words[word] += (fourgrams[fourgram][word] * 64)

	sent.append(choose_next(seed_words))

	# advance
	fourth_word = sent[0]
	third_word = sent[1]
	second_word = sent[2]
	seed_word = sent[3]

	# fifth word
	seed_words = unigrams[seed_word]
	bigram = (second_word, seed_word)

	seed_words = weight_ngram(seed_words, bigrams, bigram)
	trigram = (third_word, second_word, seed_word)
	seed_words = weight_ngram(seed_words, trigrams, trigram)

	# weight 4 gram
	fourgram = (fourth_word, third_word, second_word, seed_word)
	seed_words = weight_ngram(seed_words, fourgrams, fourgram)

	# weight 5 gram
	fivegrams_to_test = (("<p>", fourth_word, third_word, second_word, seed_word),
				(".", fourth_word, third_word, second_word, seed_word))

	for fivegram in fivegrams_to_test:
		if fivegram in fivegrams:
			for word in fivegrams[fivegram]:
				seed_words[word] += (fivegrams[fivegram][word] * 256)

	sent.append(choose_next(seed_words))

	# the rest of the sentence
	while end_of_file == False:

		final_dict = unigrams[seed_word]
		bigram = (second_word, seed_word)
		trigram = (third_word, second_word, seed_word)
		fourgram = (fourth_word, third_word, second_word, seed_word)

		if bigram in bigrams:
			for word in bigrams[bigram]:
				final_dict[word] += (bigrams[bigram][word] * 4)

		if trigram in trigrams:
			for word in trigrams[trigram]:
				final_dict[word] += (trigrams[trigram][word] * 16)

		if fourgram in fourgrams:
			for word in fourgrams[fourgram]:
				final_dict[word] += (fourgrams[fourgram][word] * 64)

		if fivegram in fivegrams:
			for word in fivegrams[fivegram]:
				final_dict[word] += (fivegrams[fivegram][word] * 256)

		next_word = choose_next(final_dict)
		sent.append(next_word)

	
		if next_word in end_of_file_terms:
			end_of_file = True
		else:
			third_word = second_word
			second_word = seed_word 
			seed_word = next_word

	return sent
		
def text_prettifier(to_prettify):
	"""
	Formats strings to be produced: capitalize first letter, eliminate spaces before commas
	"""
	
	punctuation = (",", "'", '"', ".", "?", "...")

	final_string = ""
	for count, word in enumerate(to_prettify):
		if count == 0:
			word = word.capitalize()

		try:
			if to_prettify[count+1] in punctuation:
				final_string = final_string+word
			else:
				final_string = final_string + word + " "

		except IndexError:
			# just add the final word
			final_string = final_string + word

	return final_string
		

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
	markov_matrix_three = order_three_create_markov_matrix(to_markov)
	markov_matrix_four = order_four_create_markov_matrix(to_markov)
	markov_matrix_five = order_five_create_markov_matrix(to_markov)
	end_parameter = "s"
	markoved =  create_text(end_parameter, markov_matrix_one, markov_matrix_two, markov_matrix_three, markov_matrix_four, markov_matrix_five)
	print(text_prettifier(markoved))




if __name__ == "__main__":
	args = get_arguments()

	if args.analyze_level == None:
		print 'You need to specify a level to analyze. Please use the "-h" flag to see your options'
	else:
		main(args)

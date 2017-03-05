# Markov Maker

This is a rudimentary text generator using Hidden Markov Models. The long term plan is to make it
work at both a word and a text level. Currently it only works at a text level, and even then it is very basic.

To use it, you will need the following packages:
* argparse
* codecs
* nltk
* random

Here is a sample invocation:
```
python markovmaker.py -t sample_text.txt
```

Text should be in a .txt file and it should be generally organized into paragraphs with newlines separating them.

To see a list of all flags or arguments just use the -h flag

## ToDo:
In rough order that I will attack them
* normalization of tokens
* quotes handling
* word level models
* phrase-level models
* smoothing
* saving of model
* folder import
* export of output
* sentence/paragraph export designation

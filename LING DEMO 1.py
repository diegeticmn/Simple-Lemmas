from sys import argv
import pandas as pd
import string

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import ngrams
from collections import Counter, OrderedDict
import string

#Open input data - replace text file with your data (in the form of a text file in the same directory as this file)
with open('emma.txt', encoding='utf-8') as f:
    text=f.read().replace('\n', ' ')


#Remove front matter

text = text.split('*END*THE SMALL PRINT! FOR PUBLIC DOMAIN ETEXTS*Ver.04.29.93*END*')
text = text[1]

#Remove back matter

text = text.split('End of The Project Gutenberg Etext')
text = text[0]


# split the document into sentences and tokenize each sentence
class Splitter(object):

	#Load tokenizer for english, Tokenize each word
    def __init__(self):
        self.splitter = nltk.data.load('tokenizers/punkt/english.pickle')
        self.tokenizer = nltk.tokenize.TreebankWordTokenizer()

#Split into separate words - each outputted list is a sentence
    def split(self,text):

        # split into single sentence
        sentences = self.splitter.tokenize(text)
        # tokenization in each sentences
        tokens = [self.tokenizer.tokenize(sent) for sent in sentences]
        return tokens

#Convert Penn Treebank tags to Wordnet tags, whoop!
class LemmatizationWithPOSTagger(object):
    def __init__(self):
        pass
    def get_wordnet_pos(self,treebank_tag):

        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            # As default pos in lemmatization is Noun
            return wordnet.NOUN

    def pos_tag(self,tokens):
        # Find POS tag for each word - outputs a list of tuples as [(Word, TAG), (Word, TAG)...]
        pos_tokens = [nltk.pos_tag(token) for token in tokens]

        # lemmatization using pos tag
        # convert into list of tuples as [('Word', 'Lemma', TAG), ('Word', 'Lemma', ['TAG'])
        pos_tokens = [ [(word, lemmatizer.lemmatize(word,self.get_wordnet_pos(pos_tag)), [pos_tag]) for (word,pos_tag) in pos] for pos in pos_tokens]
        return pos_tokens

#Initialize
lemmatizer = WordNetLemmatizer()
splitter = Splitter()
lemmatization_using_pos_tagger = LemmatizationWithPOSTagger()

#Make lowercase
text = text.lower()

#Remove punctuation
replace_punctuation = str.maketrans(string.punctuation, ' '*len(string.punctuation))
text = text.translate(replace_punctuation)

#split document into sentence followed by tokenization
tokens = splitter.split(text)

#lemmatize with pos tagger
lemma_pos_token = lemmatization_using_pos_tagger.pos_tag(tokens)
lemma_list = []

#Get just the lemmas
for i in lemma_pos_token:
	lemma = []
	for j in i:
		lemma.append(j[1])
	lemma_list.append(lemma)

#Initialize the counter
frequencies = Counter([])


#Iterates through sentences, finds ngrams and counts frequences
for i in lemma_list:
	types = ngrams(i, 1) #Replace 1 with n for n-grams
	frequencies += Counter(types)

frequencies = OrderedDict(frequencies.most_common())

#Count total tokens
tokes = text.split()
total_tokens = len(tokes)

print('Total number of tokens:\t', total_tokens)

print('Total number of types:\t', len(frequencies))

with open('frequency_output.csv', encoding='utf-8-sig', mode='w') as fp:
	fp.write('Type|Frequency\n')
	for tag, count in frequencies.items():
		fp.write('{}|{}\n'.format(tag, count))


# Objects:
# 	Word (tuple):
#		- key: string word
#		- value: int count (3 or greater is treated the same)
#	WordProbability:
#		- string name
#		- Zero-Probability
#		- One-Probability
#		- Two-Probability
#		- Lots-Probability

# Data Structures:
#	Spam email dictionary:
#		- filename of email as key
#		- list of Words as value
#	Ham email dictionary:
#		- filename of email as key
#		- list of Words as value
#	Word-Spam Probability:
#		- a dictionary of (string wordname, WordProbability object)
#	Word-Ham Probability:
#		- a dictionary of (string wordname, WordProbability object)

# Algorithms
#	Word Probability given Spam (Word-Ham Probability created similarly):

#		- How is it created?
#			list zero; list one; list two; list lots;	// string as key, int as value
#			For each email in Spam email dictionary
#				For each word in dict.txt 
#					if word is in email
#						if word.count == 1
#							one[word]++
#						else if word.count == 2
#							two[word]++
#						else
#							lots[word]++
#					else
#						zero[word]++
#			dictionary wordSpamProbability
#			For each word in dict.txt
#				float zeroProbability, oneProbability, twoProbability, Lots-Probability
#				zeroProbability = zero[word] / SpamEmailDictionary.size
#				oneProbability 	= one[word] / SpamEmailDictionary.size
#				twoProbability 	= two[word] / SpamEmailDictionary.size
#				lotsProbability = lots[word] / SpamEmailDictionary.size

#		- How is it useful?
#			It enables a O(1) lookup time to determine probability of (w=# given Spam)

import os
import wordprobability

''' 
Begin by creating the necessary data structures.
This includes the 
	- list of words, 
	- dictionary of spam emails, 
	- dictionary of ham emails, 
	- probability dictionary of spam words 
	- probability dictionary of ham words 
''' 

''' creates a list of words from dict.txt '''
def createWordsList():
	f = file("dict.txt").read()
	words = []
	for word in f.split():
		words.append(word)
	return words

'''
Fills a dictionary by analyzing files for specific words,
and marking their word count.
'''
def createEmailDictionary(words, dictionary, folderName):
	for filename in os.listdir(folderName):
		wordsInEmail = []
		f = file(folderName + filename).read()
		for word in words:
			count = 0
			for emailWord in f.split():
				if word.lower() == emailWord.lower():
					count = count + 1
			if count != 0:
				wordsInEmail.append({word.lower() : count})
		dictionary[filename] = wordsInEmail

## Changing current working directory to data/
print os.getcwd()
print "Changing current working directory to \'data\'"
os.chdir("data/")
print os.getcwd()

words = createWordsList()
spamEmails = {}
createEmailDictionary(words, spamEmails, "train/spam/")
hamEmails = {}
createEmailDictionary(words, hamEmails, "train/ham/")

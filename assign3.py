
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
#			dict zero; dict one; dict two; dict lots;	// string as key, int as value
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
#				wordSpamProbability[word] = WordProbability (the four calculated values)

#		- How is it useful?
#			It enables a O(1) lookup time to determine probability of (w=# given Spam)

import os
import sys
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
def createEmailDictionary(words, folderName):
	# Set up progress bar
	numFiles = len(os.listdir(folderName))
	steps = numFiles / 10
	i = 0
	print "Beginning: [          ]",
	print '\b'*12,
	sys.stdout.flush()

	# create dictionary
	dictionary = {}
	for filename in os.listdir(folderName):
		wordsInEmail = []
		f = file(folderName + filename).read()
		for word in words:
			count = 0
			for emailWord in f.split():
				if word.lower() == emailWord.lower():
					count = count + 1
			if count != 0:
				wordsInEmail.append((word.lower(), count))
		dictionary[filename] = wordsInEmail

		# Print progress bar
		i = i+1
		if i%steps == 0:
			print '\b.',
			sys.stdout.flush()
		percent = i / numFiles

	# Finish
	print "\b] Done!"
	return dictionary
		
'''
Creates a dictionary filled with words as keys, and amounts as values.
a WordProbability object is provided to modulate.
'''
def createProbabilityDictionary(words, dictionary):
	zero = {}
	one = {}
	two = {}
	lots = {}
	for email in dictionary:
		for word in words:
			l = dictionary[email]
			count = 0
			for x in l:
				if word == x[0]:
					count = x[1]
					break
			if count == 0:
				if word in zero:
					zero[word] = zero[word] + 1
				else:
					zero[word] = 1
				continue
			if count == 1:
				if word in one:
					one[word] = one[word] + 1
				else:
					one[word] = 1
			elif count == 2:
				if word in two:
					two[word] = two[word] + 1
				else:
					two[word] = 1
			else:
				if word in lots:
					lots[word] = lots[word] + 1
				else:
					lots[word] = 1

	wordProbability = {}
	for word in words:
		zeroProbability = 0.0
		oneProbability = 0.0
		twoProbability = 0.0
		lotsProbability = 0.0
		if word in zero:
			zeroProbability = zero[word] / (len(dictionary) + 0.0)
		if word in one:
			oneProbability = one[word] / (len(dictionary) + 0.0)
		if word in two:
			twoProbability = two[word] / (len(dictionary) + 0.0)
		if word in lots:
			lotsProbability = lots[word] / (len(dictionary) + 0.0)
		wordProbability[word] = wordprobability.make_wordprobability(zeroProbability, oneProbability, twoProbability, lotsProbability)
	return wordProbability



## Changing current working directory to data/
print os.getcwd()
print "\nChanging current working directory to \'data\'\n"
os.chdir("data/")
print os.getcwd()


words = createWordsList()

print "Creating list of word counts for spam emails from the training set..."
spamEmails = createEmailDictionary(words, "train/spam/")

print "Creating list of word counts for ham emails from the training set..."
hamEmails = createEmailDictionary(words, "train/ham/")

spamProbability = len(spamEmails) / (len(spamEmails) + len(hamEmails) + 0.0) # adding 0.0 to make it return a float
print "Probability of an email being spam: " + str(spamProbability)

hamProbability = len(hamEmails) / (len(spamEmails) + len(hamEmails) + 0.0) # adding 0.0 to make it return a float
print "Probability of an email being ham: " + str(hamProbability)


wordProbabilityGivenSpam = createProbabilityDictionary(words, spamEmails)
wordProbabilityGivenHam = createProbabilityDictionary(words, hamEmails)

# Now determine whether the emails in the training and test set are spam or ham

# Create email dictionaries for test set and append them
print "Creating list of word counts for spam emails from the test set..."
spamEmailsTest = createEmailDictionary(words, "test/spam/")
spamEmailsFull = spamEmails.copy()
spamEmailsFull.update(spamEmailsTest)
print "Created larger set from training and test spam emails."
print "Training size: " + str(len(spamEmails))
print "Test size: " + str(len(spamEmailsTest))
print "Final size: " + str(len(spamEmailsFull))

print "Creating list of word counts for ham emails from the test set..."
hamEmailsTest = createEmailDictionary(words, "test/ham/")
hamEmailsFull = hamEmails.copy()
hamEmailsFull.update(hamEmailsTest)
print "Created larger set from training and test ham emails."
print "Training size: " + str(len(hamEmails))
print "Test size: " + str(len(hamEmailsTest))
print "Final size: " + str(len(hamEmailsFull))

# For each indeed spam email, determine the P(Spam|e) and P(Ham|E).  
	# If P(Spam|e) >= P(Ham|e)
		# increment spam prediction count

# For each indeed ham email, determine the P(Spam|e) and P(Ham|E).  
	# If P(Spam|e) >= P(Ham|e)
		# increment spam prediction count
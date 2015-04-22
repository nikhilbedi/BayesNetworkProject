

class WordProbability(object):
	zero = 0.0
	one = 0.0
	two = 0.0
	lots = 0.0

	# Class "Constructor"
	def __init__(self, zero, one, two, lots):
		self.zero = zero
		self.one = one
		self.two = two
		self.lots = lots

def make_wordprobability(zero, one, two, lots):
	wordprobability = WordProbability(zero, one, two, lots)
	return wordprobability
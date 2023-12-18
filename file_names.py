import random

N = [
"fox", "rainbow", "clock", "toy", "snake","night","lake",
"airport", "club","yard","authority","rat","quartz","glove",
"fish","theory","money", "river", "tree", "kin","cat","hole",
"monkey", "delight", "love", "duck", "goose", "hate", "joy",
"worm", "frost", "king", "queen", "light", "dark", "pine",
"time", "noise", "music", "poem", "witch","wizard", "magic",
"wish", "frog", "fire", "potion", "shoe", "cone", "sphere",
"culture", "discourse", "wire", "map", "spell", "feeling"
]

DET = [
"a", "the", "that", "this", "some", "which",
]

PREP = [
"of", "for", "to", "into", "from", "with", "by", "at", "via", "as"
]

#alias
def _r(list_):
	return random.choice(list_)

def NP():

	options = [
		[_r(N)],
		[_r(N),_r(N)],
		[_r(DET),_r(N)],
		[_r(DET),_r(N),_r(N)]
	]

	return "_".join(_r(options))


def PP():
	return "_".join([NP(),_r(PREP),NP()])

def pp_name():
	return PP()

if __name__ == "__main__":
	for i in range(10):
		print(pp_name())

#Want to add a better accessor so we can deal 
#with potentially nested indexes arbitrarily
class index(dict):
	def find(self, index_str):
		inds = index_str.split(".")
		inds.reverse()

		cursor = self
		while len(inds)>0:
			i = inds.pop()

			if i.isdigit():
				i = int(i)
			cursor = cursor[i]

		return cursor

	def assign(self, index_str, value):
		inds = index_str.split(".")
		inds.reverse()

		cursor = self
		while len(inds)>1:
			i = inds.pop()
			if i.isdigit():
				i = int(i)
			cursor = cursor[i]

		try:
			cursor[inds[0]] = value
		except TypeError:
			cursor[int(inds[0])] = value



if __name__ == "__main__":
	test = index({
		"a":"A",
		"b": ["B", "BB"],
		"c": {
			"a":"CA",
			"b":["CB","CBB"]
			},
		1:{
		  "A":"a",
		  "B":["c", "d"]
		}
		})

	print(test.find("a"))
	print(test.find("b.0"))
	print(test.find("b.1"))
	print(test.find("c.a"))
	print(test.find("c.b.0"))
	test.assign("c.b.1", "BBBBBBB")
	print(test.find("c.b.1"))
	print(test.find("1.B.0"))

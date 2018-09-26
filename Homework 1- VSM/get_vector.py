import math

fp = open("article3.txt", "r")
article_list = []
for data in fp.readlines():
	words = data.split()
	article_list.append(words)

tot_article = len(article_list)
words_set = set()
tf = []
for words in article_list:
	tot = len(words)
	tf_i = {}
	for word in words:
		if word in tf_i.keys():
			tf_i[word] += 1.0
		else :
			tf_i[word] = 1.0
		words_set.add(word)
	for word in tf_i.keys():
		tf_i[word] /= tot
	tf.append(tf_i)

idf = {}
for word in words_set:
	idf[word] = 0.0
for words in article_list:
	set0 = set()
	for word in words:
		set0.add(word)
	for word in set0:
		idf[word] += 1.0

for word in idf.keys():
	idf[word] = math.log(tot_article / idf[word])

word_id = {}
index = 0
for word in words_set:
	word_id[word] = index
	index += 1

tfidf = []
for tf_i in tf:
	list0 = []
	for word in words_set:
		if word in tf_i:
			list0.append(tf_i[word] * idf[word])
		else :
			list0.append(0)
	tfidf.append(list0)

fq = open("vector.txt", 'w')
for v in tfidf:
	list0 = []
	for i in v:
		list0.append(str(i))
	fq.write(" ".join(list0))
	fq.write("\n")
fq.close()


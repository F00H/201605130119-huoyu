import json
import nltk
from nltk.corpus import stopwords

def to_lowletter(word):
	new_word = ''
	for index in range(len(word)):
		if word[index] >= 'A' and word[index] <= 'Z':
			new_word += chr(ord(word[index]) - ord('A') + ord('a'))
		elif (word[index] >= 'a' and word[index] <= 'z'):
			new_word += word[index]
	return new_word

def tokenize(sentence):
	sentence = nltk.word_tokenize(sentence)
	#去掉标点符号
	english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%', '...']
	sentence = [to_lowletter(word) for word in sentence if word not in english_punctuations and to_lowletter(word) != ""]
	return sentence

fp = open("tweets.txt", "r");
data = []
for line in fp.readlines():
	data.append(json.loads(line))
fp.close()

word_list = []
word_set = set()
word_dic = {}
article = []
for i in range(len(data)):
	sentence = tokenize(data[i]["text"])
	if (len(sentence) > 2 and sentence[-2] == 'http'):
		sentence = sentence[:-2]
	for j in sentence:
		word_set.add((j, i))
	article.append(sentence)

word_list = list(word_set)
word_list.sort()
for i in word_list:
	if i[0] in word_dic.keys():
		word_dic[i[0]].append(i[1])
	else:
		word_dic[i[0]] = [i[1]]

fp = open("bool.txt", "w", encoding = 'utf-8')
for key, value in word_dic.items():
	#value = [str(i) for i in value]
	fp.write(key + " ")
	fp.write(str(value))
	fp.write("\n")
	#fp.write(key + " " + " ".join(value))
fp.close()



import json
import nltk

def init():
	fp = open("bool.txt", "r")
	word_dic = {}
	for i in fp.readlines():
		j = i.strip().split('[')
		k = j[1][:-1].split(', ')
		word_dic[j[0][:-1]] = [int(x) for x in k]
	return word_dic

def Or(x, y):
	n = len(x)
	m = len(y)
	i = 0
	j = 0
	z = []
	while i < n or j < m:
		if j == m or x[i] < y[j]:
			z.append(x[i])
			i += 1
		elif i == n or x[i] > y[j]:
			z.append(y[j])
			j += 1;
		else :
			z.append(x[i])
			i += 1
			j += 1
	return z

def And(x, y):
	n = len(x)
	m = len(y)
	i = 0
	j = 0
	z = []
	while i < n and j < m:
		if x[i] < y[j]:
			i += 1
		elif x[i] > y[j]:
			j += 1;
		else :
			z.append(x[i])
			i += 1
			j += 1
	return z

def Sub(x, y):
	y = And(x, y)
	n = len(x)
	m = len(y)
	i = 0
	j = 0
	z = []
	while i < n or j < m:
		if j == m or x[i] < y[j]:
			z.append(x[i])
			i += 1
		else :
			i += 1
			j += 1
	return z		

def Calc(s, word_dic):
	a = s.split()
	n = len(a)
	z = word_dic[a[0]]
	i = 0
	while i + 2 < n:
		y = word_dic[a[2]]
		if a[i + 1] == '&':
			z = And(z, y)
		elif a[i + 1] == '|':
			z = Or(z, y)
		elif a[i + 1] == '-':
			z = Sub(z, y)
		i += 2
	return z

def main():
	word_dic = init()
	s = 'shit & fuck'
	fp = open("article.txt", "r")
	article = fp.readlines()
	list0 = Calc(s, word_dic)
	print(list0)
	for i in list0:
		print(article[i])

if __name__ == '__main__':
	main()



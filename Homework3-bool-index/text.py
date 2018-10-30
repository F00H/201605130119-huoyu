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

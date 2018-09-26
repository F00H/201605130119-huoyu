import os
import re

path = "D:/Courses_homework/IR/homework1/20news-18828"

#分割单词
article_list = []
for file0 in os.listdir(path):
	file_path0 = os.path.join(path, file0)
	for file1 in os.listdir(file_path0):
		file_path1 = os.path.join(file_path0, file1)
		fp = open(file_path1, "rb")
		words = []
		for word in fp.readlines():
			words.extend(re.split('[.:,?!;" \t\n]', word.decode("utf8","ignore")))
		fp.close()
		article_list.append(words)

#Normalization  只保留拉丁字母,并把大写转小写
new_article_list = []
for list_ in article_list:
	new_words = []
	for word in list_:
		new_word = ''
		for index in range(len(word)):
			if word[index] >= 'A' and word[index] <= 'Z':
				new_word += chr(ord(word[index]) - ord('A') + ord('a'))
			elif (word[index] >= 'a' and word[index] <= 'z'):
				new_word += word[index]
		if len(new_word) > 0:
			new_words.append(new_word)
	new_article_list.append(new_words)
article_list = new_article_list

#去停用词
fp = open("stop_word.txt", 'r')
fq = open("article1.txt", 'w')
stop_word = []
for word in fp.readlines():
	word = word.strip()
	stop_word.append(word)
fp.close()

for index in range(len(article_list)):
	article_list[index] = [i for i in article_list[index] if i not in stop_word]
	fq.write(" ".join(article_list[index]))
	fq.write("\n")
fq.close()




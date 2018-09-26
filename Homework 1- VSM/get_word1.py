import matplotlib.pyplot as plt
import math

fp = open("article1.txt", "r")
article_list = []
for data in fp.readlines():
	words = data.split()
	article_list.append(words)

#Remove non-informative words
word_count = {}
for words in article_list:
	for word in words:
		if word in word_count.keys():
			word_count[word] += 1
		else :
			word_count[word] = 1

word_count = sorted(word_count.items(), key = lambda x:x[1], reverse = True) 
words_list = []
for keys, values in word_count:
	if values > 10:
		words_list.append(keys)

fq = open("article2.txt", 'w')
for index in range(len(article_list)):
	article_list[index] = [i for i in article_list[index] if i in words_list]
	fq.write(" ".join(article_list[index]))
	fq.write("\n")
fq.close()

#画图过程
'''
sets = set(word_count.values())
sets = sorted(sets, reverse = True)
list_x = []
for i in range(len(sets)):
	list_x.append(math.log(i + 1))
plt.plot(list_x, sets)   #在画布上画图
plt.savefig('Zipf’s_law1.png')  #生成图片

#tot_word = len(word_count)
list_ = []
list_ = list(rank_word_count.keys())
for i in range(len(list_)):
 	list_[i] = math.log(list_[i]) / math.log(2)
plt.plot(rank_word_count.values(), list_)   #在画布上画图
plt.savefig('Zipf’s_law.png')  #生成图片
'''
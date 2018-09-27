import os
import math

path = "D:/Courses_homework/IR/homework1/20news-18828"

#查找每一类新闻有多少文本
article_number = [] #每一类新闻个数
article_name = [] 	#每一类新闻名字
for file in os.listdir(path):
	file_path = os.path.join(path, file)
	article_name.append(file)
	article_number.append(len(os.listdir(file_path)));

#把每一类新闻分开，存于二维list中,划分训练数据和测试数据7/3
fp = open("article3.txt")
article_train = []
article_test = []
article_tot = 0#总的训练样本的个数
word_set = set() #所有单词的集合
topic_word_tot = [] #每一类新闻里单词的个数
for i in range(len(article_name)):
	topic_train = []
	topic_test = []
	num = 0
	for j in range(article_number[i]):
		words = fp.readline().split()
		for word in words:
			word_set.add(word)
		if (j * 10 / 7 < article_number[i]):
			topic_train.append(words)
			num += len(words)
		else :
			topic_test.append(words)
	article_tot += len(topic_train)
	article_train.append(topic_train)
	article_test.append(topic_test)
	topic_word_tot.append(num)

#朴素贝叶斯，统计每一类新闻包含哪些单词,有多少个
word_tot = len(word_set) #总的不同的单词的数量
article_train_words = [] #存储每一类单词有多少个
for i in range(len(article_train)):
	words = {}
	for j in range(len(article_train[i])):
		for word in article_train[i][j]:
			if word in words.keys():
				words[word] += 1
			else :
				words[word] = 1
	article_train_words.append(words)

#测试
alpha = 0.05
tot = 0 #测试总量
yes = 0 #测试正确数量
for i in range(len(article_test)):       	   #遍历测试数据的每一个topic
	for j in range(len(article_test[i])):	   #遍历测试数据每一个topic下的每一篇新闻
		tot += 1 							   #统计总的测试数据
		maxp = 0.0							   #最大的概率，初始为零
		ans = -1							   #记录最大的概率所对应的那个类，初始为-1
		for k in range(len(article_train_words)): 	#遍历训练数据的每一个topic
			p = 0.0;								#记录在当前topic下的概率
			for word in article_test[i][j]:			#遍历测试新闻的每一个单词，以此来计算概率
				if word in article_train_words[k]:	#如果当前训练数据的topic包含该测试单词，则按照公式计算概率加成
					p += math.log(len(article_train[k]) / article_tot * (article_train_words[k][word] + alpha) / (topic_word_tot[k] + word_tot * alpha))
				else :								#否则，则当该单词出现一次
					p += math.log(len(article_train[k]) / article_tot * alpha / (topic_word_tot[k] + word_tot * alpha))
			if ans == -1 or p > maxp:
				maxp = p
				ans = k
		if ans == i:
			yes += 1
print(yes, tot, yes / tot)

#测试结果 
#alpha = 1   正确：4705 总的：5642 正确率：0.8339241403757532 
#alpha = 1.5 正确：4667 总的：5642 正确率：0.8271889400921659
#alpha = 0.5 正确：4740 总的：5642 正确率：0.8401276143211627
#alpha = 0.1 正确：4771 总的：5642 正确率：0.8456221198156681

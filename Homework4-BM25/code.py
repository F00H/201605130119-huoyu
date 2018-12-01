import json
import nltk
import math
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
	if (len(sentence) > 2 and sentence[-2] == 'http'):
		sentence = sentence[:-2]
	return sentence

def read_json_file(file_name):
	with open(file_name, 'r', errors = 'ignore') as fp:
		Text_Id = []
		avg_len = 0
		Id_len = {} 
		for line in fp:
			message = json.loads(line)
			Text = tokenize(message['text'])
			Id = message['tweetId']
			avg_len += len(Text)
			Id_len[Id] = len(Text)
			Text_Id.append([Text, Id])
	return avg_len / len(Id_len), Text_Id, Id_len 

def data_process(Text_id):
	terms_list = []
	for x in Text_id:
		for word in x[0]:
			terms_list.append((word, x[1]))
	terms_list.sort()
	word_terms_dic = {}
	Len = len(terms_list)
	num = 1
	for i in range(Len):
		if i == Len - 1 or terms_list[i] != terms_list[i + 1]:
			if terms_list[i][0] in word_terms_dic.keys():
				word_terms_dic[terms_list[i][0]].append([terms_list[i][1], num])
			else :
				word_terms_dic[terms_list[i][0]] = [[terms_list[i][1], num]]
			num = 1
		else :
			num += 1
	return word_terms_dic

def read_question(file_name): 
	with open(file_name, 'r', errors = 'ignore') as f:
		Text = []
		Id = []
		for line in f:
			if line[:5] == '<num>':
				Id.append(line[16:19])
			elif line[:7] == '<query>':
				Text.append(line[8:-10])
	return [[Text[i], Id[i]] for i in range(len(Id))]

def calc(c, k, b, advl, d, df, M): #根据参数计算结果
	return c * (k + 1) * c / (c + k * (1 - b + b * d / advl)) * math.log((M + 1) / df)

def query_result(outfile, question, word_terms_dic, avg_len, Id_len, k, b):
	with open(outfile, 'w', encoding = 'utf-8') as f:
		for q in question:
			Id_dic = {}
			M = len(Id_len)
			Q = tokenize(q[0])
			for word in Q:
				if word in word_terms_dic.keys():
					Id_list = word_terms_dic[word]
					Len = len(Id_list)
					for Id_num in Id_list:
						if Id_num[0] in Id_dic.keys():
							Id_dic[Id_num[0]] += calc(Id_num[1], k, b, avg_len, Id_len[Id_num[0]], Len, M)
						else :
							Id_dic[Id_num[0]] = calc(Id_num[1], k, b, avg_len, Id_len[Id_num[0]], Len, M)
			
			answer = []
			for key, value in Id_dic.items():
				answer.append((value, key))
			answer.sort(reverse = True)
			for a in answer:
				f.write(q[1] + ' ' + a[1] + '\n')

def get_my_result():
	data_file = 'tweets.txt'
	question_file = 'question.txt'
	result_file = 'my_result.txt'
	#处理查询
	question = read_question(question_file)
	#处理数据集
	avg_len, Text_Id, Id_len = read_json_file(data_file)
	#构建terms
	word_terms_dic = data_process(Text_Id)
	#输出最终结果
	query_result(result_file, question, word_terms_dic, avg_len, Id_len, 100, 0.5)

if __name__ == '__main__':
	get_my_result()

	
	#照着学长的格式装扮了一下自己代码

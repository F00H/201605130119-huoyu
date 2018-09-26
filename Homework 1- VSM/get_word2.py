from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

fp = open("article2.txt", "r")
article_list = []
for data in fp.readlines():
	words = data.split()
	article_list.append(words)

#stemming和lemmatization  (NLTK进行stemming词干提取)

#wordnet_lemmatizer = WordNetLemmatizer()   词形还原效果不是很好
porter_stemmer = PorterStemmer()
fq = open("article3.txt", 'w')
for index in range(len(article_list)):
	article_list[index] = [porter_stemmer.stem(i) for i in article_list[index]]
	fq.write(" ".join(article_list[index]))
	fq.write("\n")
fq.close()
#print(wordnet_lemmatizer.lemmatize('effective'))
#print(porter_stemmer.stem('effective'))
'''
words_set = set()
for words in article_list:
	for word in words:
		words_set.add(word)
new_words_set = set()
for word in words_set:
	new_words_set.add(porter_stemmer.stem(word))
print(new_words_set)
'''
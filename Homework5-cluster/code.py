import json
from sklearn.cluster import *
from sklearn.feature_extraction.text import  TfidfVectorizer
import numpy as np
from sklearn.metrics import normalized_mutual_info_score 
from sklearn import mixture
import matplotlib.pyplot as plt


def data_pro(file_name):
	with open(file_name, 'r', errors = 'ignore') as fp:
		n_sample = []
		n_cluster = []
		for line in fp:
			message = json.loads(line)
			n_sample.append(message['text'])
			n_cluster.append(message['clusterNo'])
	return n_sample, n_cluster

def K_means(matrix, num_clusters):	
	km_cluster = KMeans(n_clusters=num_clusters, init='k-means++')
	result = km_cluster.fit_predict(matrix)
	return result

def test(X, Y):
	return normalized_mutual_info_score(X, Y)


def clustering_algorithm_comp():
	data_file = "tweets.txt"
	n_sample, n_cluster = data_pro(data_file)
	K = 3000
	n_sample = n_sample[:K]
	n_cluster = n_cluster[:K]
	num_clusters = len(set(n_cluster))
	vectorizer = TfidfVectorizer(lowercase=True)
	tfidf_matrix = vectorizer.fit_transform(n_sample)
	tfidf_matrix = tfidf_matrix.toarray()
	n_cluster = np.array(n_cluster)

	X = []
	result = K_means(tfidf_matrix, num_clusters)
	np.save("K_means.npy", result)
	print('K_means:', test(result, n_cluster))
	X.append(test(result, n_cluster))

	result = AffinityPropagation().fit(tfidf_matrix).labels_
	np.save("AffinityPropagation.npy", result)
	print('AffinityPropagation:', test(result, n_cluster))
	X.append(test(result, n_cluster))

	bandwidth = estimate_bandwidth(tfidf_matrix, quantile = 0.2)
	result = MeanShift(bandwidth = bandwidth, bin_seeding = True).fit(tfidf_matrix).labels_
	np.save("MeanShift.npy", result)
	print('MeanShift:', test(result, n_cluster))
	X.append(test(result, n_cluster))

	result = SpectralClustering(n_clusters = num_clusters).fit(tfidf_matrix).labels_
	np.save("spectral_clustering.npy", result)
	print('spectral_clustering:', test(result, n_cluster))
	X.append(test(result, n_cluster))

	result = AgglomerativeClustering(n_clusters = num_clusters).fit(tfidf_matrix).labels_
	np.save("AgglomerativeClustering.npy", result)
	print('AgglomerativeClustering:', test(result, n_cluster))
	X.append(test(result, n_cluster))

	#result = AgglomerativeClustering(n_clusters = num_clusters).fit(tfidf_matrix).labels_
	#np.save("AgglomerativeClustering.npy", result)
	#print('AgglomerativeClustering:', test(result, np.array(n_cluster)))

	result = DBSCAN().fit(tfidf_matrix).labels_
	np.save("DBSCAN.npy", result)
	print('DBSCAN:', test(result, n_cluster))
	X.append(test(result, n_cluster))

	gmm = mixture.GaussianMixture().fit(tfidf_matrix)
	result = gmm.predict(tfidf_matrix)
	np.save("GaussianMixture.npy", result)
	print('GaussianMixture:', test(result, n_cluster))
	X.append(test(result, n_cluster))

	result = Birch().fit(tfidf_matrix).labels_
	np.save("Birch.npy", result)
	print('Birch:', test(result, n_cluster))
	X.append(test(result, n_cluster))

	Y = ['KM', 'AP', 'MS', 'SC',
	 'AC', 'DBSCAN', 'GM', 'Birch']
	plt.bar(Y, X, width=0.4, color='red')
	plt.show()


if __name__ == '__main__':
	clustering_algorithm_comp()

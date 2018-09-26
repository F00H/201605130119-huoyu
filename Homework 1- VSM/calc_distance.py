import math

def calc(v1, v2, len):
	dot = 0.0 
	len1 = 0.0
	len2 = 0.0
	for i in range(len):
		dot += float(v1[i]) * float(v2[i])
		len1 += float(v1[i]) * float(v1[i])
		len2 += float(v2[i]) * float(v2[i])
	return dot / math.sqrt(len1) / math.sqrt(len2)

fp = open("vector.txt", "r")
vector = []
for v in fp.readlines():
#	list0 = []
#	v0 = v.split();
#	for i in v0:
#		list0.append(float(i))
	vector.append(v.split())

print(calc(vector[0], vector[1], len(vector[0])))

#!/usr/bin/python

from collections import Counter
import sys
import re

file = open(r"ent_all.csv", "r")


wordcount = Counter(file.read().split())


stopwords_file = open(r"stopwords01.txt", "r")
stopwords = stopwords_file.read()

d = {}
for item in wordcount.items():
	word = re.sub('["\',-]', '', item[0].strip())
	if word not in stopwords:
		d[word] = item[1]

sorted_dict = Counter(d)
for k, v in sorted_dict.most_common(40):
	print '%s: \t %i' % (k, v)

num_words = sum(d[w] for w in d)
print("Total words: %s " % num_words)

# -*- coding: utf-8 -*-
"""TP1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Y2OferXiT3H4eCxCpKwUUMSNnjtQkwDD
"""

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import math
import numpy as np
import random
import string
from urllib import request
from bs4 import BeautifulSoup
import sys


#url = "https://www.gutenberg.org/cache/epub/71950/pg71950.txt" #rawtext is taken from this url
#response = request.urlopen(url)
#raw = response.read().decode('utf8')

#filePath = input("Please specify the filepath: ")
filePath = sys.argv[1]
rawFile = open(filePath,"r")
raw = rawFile.read()

#basisFilePath = input("Please specify basis filepath: ")
basisFilePath = sys.argv[2]
basisFile = open(basisFilePath,"r")
basis = basisFile.readlines()

#targetFilePath = input("Please specify target filepath: ")
targetFilePath = sys.argv[3]
targetFile = open(targetFilePath,"r")
target = targetFile.readlines()

rawLower = raw.lower()
rawNoPunct = ""
for char in rawLower:
  if char not in string.punctuation + '”'+"’":
    rawNoPunct = rawNoPunct + char
  else:
    rawNoPunct = rawNoPunct + " "

rawNoPunctSplit = rawNoPunct.split()

#T = open("T.txt","r") #target word file
#target = T.readlines()

#B = open("B.txt","r") #basis word file
#basis = B.readlines()

contextWin = 5

##constructing Co-occurrence Matrix##
cMat = np.zeros((len(target),len(basis)))

count = 0
for i in range(len(rawNoPunctSplit)):
  if rawNoPunctSplit[i] +'\n' in target:
    for j in range(i-2,i+3):
      if j>=0 and j<len(rawNoPunctSplit):
        if rawNoPunctSplit[j]+'\n' in basis:
          i1 = target.index(rawNoPunctSplit[i] + '\n')
          i2 = basis.index(rawNoPunctSplit[j] + '\n')
          cMat[i1][i2] = cMat[i1][i2] + 1
          count = count+1

##PPMI calculation##
cMatPPMI = np.zeros((len(target),len(basis)))
PwList = np.sum(cMat,axis=1)
PcList = np.sum(cMat,axis=0)

for i in range (len(target)):
  for j in range (len(basis)):
    if cMat[i][j]>0:
      Pwc = cMat[i][j]/count
      Pw = PwList[i]/count
      Pc = PcList[j]/count
      PMIwc = math.log((Pwc/(Pw*Pc)),2)
      if PMIwc > 0:
        cMatPPMI[i][j] = PMIwc

##Cosine Similarity matrix construction##
cosSimMat = np.zeros((len(target),len(target)))
for i in range(len(target)):
  for j in range(len(target)):
    numeratorSum = 0
    denominatorSqSumI = 0
    denominatorSqSumJ = 0
    for k in range(len(basis)):
      numeratorSum += cMatPPMI[i][k]*cMatPPMI[j][k]
      denominatorSqSumI += math.pow((cMatPPMI[i][k]),2)
      denominatorSqSumJ += math.pow((cMatPPMI[j][k]),2)
    CosDenom = (math.pow(denominatorSqSumI,0.5)*math.pow(denominatorSqSumJ,0.5))
    if (CosDenom > 0):
      Cosij = numeratorSum/(math.pow(denominatorSqSumI,0.5)*math.pow(denominatorSqSumJ,0.5))
    else:
      Cosij = 0
    cosSimMat[i][j] = Cosij

dataset = cosSimMat
pca=PCA()
pca.fit(dataset)
plt.figure(figsize=(10, 8))
plt.plot (pca.explained_variance_ratio_.cumsum())

pca=PCA(n_components=2)
pca.fit(dataset)
pca_data=pca.transform(dataset)
pca_data

labels = target

####Plotting##
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111)

xs = pca_data[:,0]  #first component
ys = pca_data[:,1]  #second component


ax.scatter(xs, ys, s=50, alpha=0.6, edgecolors='w')


for x, y, label in zip(xs, ys, labels):
    ax.text(x, y, label)

##most similar word
wordPairs = []
for i in range(len(target)):
  minDist = 9999
  xi = pca_data[:,0][i]
  yi = pca_data[:,1][i]
  wordPairForTarget = target[i]
  for j in range(len(target)):
    xj = pca_data[:,0][j]
    yj = pca_data[:,1][j]
    distij = math.pow(math.pow((xi-xj),2)+math.pow((yi-yj),2),(1/2))
    if distij<minDist and i!=j:
      minDist = distij
      wordPairForTarget = target[j]
  if target[i][-1] == "\n":
    target[i] = target[i][:-1]
  if wordPairForTarget[-1] == "\n":
    wordPairForTarget = wordPairForTarget[:-1]
  wordPairs.append((target[i],wordPairForTarget))

print(" ")
print("Here are the target words paired with the target word closest to them")

for wordPair in wordPairs:
  print(wordPair)

print(" ")

rawFile.close()
basisFile.close()
targetFile.close()
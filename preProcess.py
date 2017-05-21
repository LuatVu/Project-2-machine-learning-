#!/usr/bin/python
# -*- coding: utf8 -*-

from os import listdir
import cPickle as cP
import math


# Chua dia chi cua file stop word
urlStopWord = "/home/luat/Desktop/ML/vietnamese-stopwords-master/vietnamese-stopwords-dash.txt"

stopWordFile = open(urlStopWord,'r')

stopWordString = stopWordFile.read()

# day se la list cac stop list duoc su dung de so sanh voi van ban
stopWordList = stopWordString.split()





#phai su dung ham nay de chuyen doi toan bo file van ban ve dang chu thuong, roi khi do moi co the loai bo tu dung
def convertUpperToLowerCase(folderNameInput, folderNameOutput):
	for f in listdir(folderNameInput):
		File1 = open(folderNameInput+f,'r')
		content = unicode(File1.read(), "utf8").lower().encode('utf8')
		File1.close()
		File2 = open(folderNameOutput+f,'w')
		File2.write(content)
		File2.close()


def Extract_SW(inputDirectory,outputFile):
	ListDocs = []
	listFile = [f for f in listdir(inputDirectory)]

	File = open(outputFile,'w')
	File.write(str(len(listFile) ) )
	File.write('\n')
	for f in listFile: 
		File0 = open(inputDirectory+f,'r')
		docs = File0.read()
		File0.close()
		wordDocs = docs.split()
		listExtract = [w for w in wordDocs if w not in stopWordList]
		content = ""
		for w in listExtract:
			content += w + " "
		File.write(content+"\n")
	File.close()	




def createDict(inputFolder):
	Dictionary = []
	words = []
	wordFrequent = []

	Docs = combineFiles(inputFolder)

	print "----word -----"
	countDoc = 0 # dung de dem pham % thuc hien
	for doc in Docs:
		print "%r\n"% round((1.0*countDoc/len(Docs))*100, 3 )# dem phan tram thuc hien
		countDoc = countDoc +1
		doc = doc.split()		
		for w in doc:
			if w not in words:
				words.append(w)
	print "---word completed---"

	print "---wordFrequent---"
	countWord = 0 # dung de dem phan tram thuc hien
	for w in words:
		print "%r\n" %round((1.0*countWord/len(words))*100,3)
		countWord = countWord + 1
		cou = 0
		for doc in Docs:
			doc = doc.split()
			if w in doc:
				cou+=1
		wordFrequent.append(cou)
	print "--wordFrequent completed--"			

	print "---Dictionary----"
	for i in range(0, len(wordFrequent) ):
		print "%r\n"% round(((1.0*i/len(wordFrequent))*100) ,3)# hien thi thoi gian chay
		if (1.0*wordFrequent[i]/len(Docs) >= 0.04):
			Dictionary.append(words[i])
	print "---Dictionary completed----"

	return Dictionary



#doc -> la 1 van ban o dang xau ki tu
#Docs -> la 1 tap hop van ban o dang list
#Dict -> la tu dien o dang xau ki tu



def tf(word, doc):
	count = 0
	doc = doc.split()
	for w in doc:		
		if word == w:
			count += 1
	return 1.0*count/len(doc)


# Docs la mot ta hop cac van ban cua tat ca cac the loai (Docs ban than la 1 danh sach)
def idf(word, Docs):
	count = 0
	for doc in Docs:
		doc = doc.split()
		if word in doc:
			count += 1
	return math.log10(1.0*len(Docs)/count)


# tra ve vector dang list
def vectorization(doc, Docs, Dict):
	Dict = Dict.split()
	vector = []
	for w in Dict:
		if w not in doc.split():
			vector.append(0)
		else:
			vector.append( tf(w,doc)*idf(w,Docs) )
	return vector


# chuan hoa vector
def standardingVector(vector):
	sum = 0
	for i in range(0,len(vector)):
		sum += math.pow(vector[i],2)
	sum = math.sqrt(sum)
	if(sum == 0 ):
		return None

	for i in range(0,len(vector)):
		vector[i] = round(1.0*vector[i]/sum, 3)
	return vector

#hop nhat cac file trong mot folder thanh mot van ban duy nhat
#van ban nay chi ton tai tren Ram khong ton tai tren o cung.
def combineFiles(inputFolder):
	Docs = []
	for f in listdir(inputFolder):
		File = open(inputFolder+f,'r')
		count = int(File.readline())
		for i in range(0,count):
			Docs.append(File.readline())
		File.close()
	return Docs





def encoding(inputFolder, outputFile, Dict):	
	trainingInput = [] # chua vecto dau vao x
	trainingOutput = [] # chua dau ra y (y la mot so chu kho phai la 1 vector)
	Docs = combineFiles(inputFolder)
	for f in listdir(inputFolder):
		if (f == 'PhapLuat.txt'):			
			File = open(inputFolder+f,'r')
			count = int(File.readline())
			for i in range(0,count):
				print "PhapLuat: %r \n"%round( (1.0 * i/count)*100, 5)
				doc = File.readline()
				vector = standardingVector( vectorization(doc, Docs, Dict) )
				if (vector != None):
					trainingInput.append(vector)
					trainingOutput.append(0)
			File.close()
		elif (f == 'KinhDoanh.txt'):		
			File = open(inputFolder+f,'r')
			count = int(File.readline())
			for i in range(0,count):
				print "KinhDoanh: %r \n" %round( (1.0 * i/count)*100, 5)
				doc = File.readline()
				vector = standardingVector( vectorization(doc, Docs, Dict) )
				if (vector != None):
					trainingInput.append(vector)
					trainingOutput.append(1)							
			File.close()
		elif (f == 'TheThao.txt'):			
			File = open(inputFolder+f,'r')
			count = int(File.readline())
			for i in range(0,count):
				print "TheThao: %r \n" %round( (1.0*i/count)*100, 5)
				doc = File.readline()
				vector = standardingVector( vectorization(doc, Docs, Dict) )
				if(vector != None):
					trainingInput.append(vector)				
					trainingOutput.append(2)
			File.close()	
		elif (f == "SucKhoe.txt"):						
			File = open(inputFolder+f,'r')
			count = int(File.readline())
			for i in range(0,count):
				print "SucKhoe: %r \n" %round( (1.0*i/count)*100, 5)
				doc = File.readline()
				vector = standardingVector( vectorization(doc, Docs, Dict) )
				if (vector != None):
					trainingInput.append(vector)
					trainingOutput.append(3)
			File.close()
		elif (f == 'GiaoDuc.txt'):			
			File = open(inputFolder+f,'r')
			count = int(File.readline())
			for i in range(0,count):
				print "GiaoDuc: %r \n" %round( (1.0*i/count)*100, 5)
				doc = File.readline()
				vector = standardingVector( vectorization(doc, Docs, Dict) )
				if (vector != None):
					trainingInput.append(vector)
					trainingOutput.append(4)
			File.close()
		elif (f == 'KhoaHoc.txt'):		
			File = open(inputFolder+f,'r')
			count = int(File.readline())
			for i in range(0,count):
				print "KhoaHoc: %r \n"%round( (1.0*i/count)*100, 5)
				doc = File.readline()
				vector = standardingVector( vectorization(doc, Docs, Dict))
				if (vector != None):
					trainingInput.append(vector)
					trainingOutput.append(5)
			File.close()
		elif (f == 'Xe.txt'):		
			File = open(inputFolder+f,'r')
			count = int(File.readline())
			for i in range(0,count):
				print "Xe: %r \n"%round( (1.0*i/count)*100, 5)
				doc = File.readline()
				vector = standardingVector( vectorization(doc, Docs, Dict) )
				if (vector != None):
					trainingInput.append(vector)
					trainingOutput.append(6)
			File.close()
	FileOutput = open(outputFile,'w')
	cP.dump( zip(trainingInput,trainingOutput), FileOutput)
	FileOutput.close()




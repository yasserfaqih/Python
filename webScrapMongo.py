import pymongo
import requests
from bs4 import BeautifulSoup
import sys
import os



# make a request :: 'http://pythonpodcast.com/'
def makeReq(path) :
	r = requests.get(path)
	return r.content

# make a soup
''' it takes the request response as arug'''
def makeSoup(html) :
	soup = BeautifulSoup(html)
	return soup


# get data from the so=oup
''' it takes a soup as arug'''
def getData(my_soup) :
	data = my_soup.find_all("article")
	return data


# get list of dictionaries for all data
''' it takes data as arug'''
def prepareData(my_data) :

	# define some holders
	episode_no = None
	title = None
	summary = None
	link = None

	itemDic = {}
	itemsList = []

	# produce the items list
	for item in my_data :
		episode_no 	= int(item.contents[1].find_all("a",{"rel":"bookmark"})[0].text.encode('utf-8').split()[1])
		title 		= str(" ".join(item.contents[1].find_all("a",{"rel":"bookmark"})[0].text.encode('utf-8').split()[3:]))
		summary 	= str(item.contents[3].find_all("p")[0].text.encode('utf-8'))
		link 		= str(item.contents[5].find_all("a")[0].get("href"))

		itemDic = {'episode_no': episode_no, 'title' : title, 'summary' : summary, 'link':link}

		itemsList.append(itemDic)

	return itemsList


# establish a connection to MongoDB
def connectMongoDB() :
	connection = pymongo.MongoClient("mongodb://localhost")
	db = connection.pypodcast
	collection = db.articles
	return collection

# insert clean data in MongoDB
''' it takes items list returned by  prepareData() '''
def insertData(connection ,clean_data) :
	for dic in clean_data :
		connection.insert_one(dic)

# retrive all data from MongoDB
def retrievData(connection) :
	cursor = connection.find().sort("episode_no", pymongo.ASCENDING)
	
	# for doc in cursor :
	# print(doc)
	# print('\n')

	DataList = [doc for doc in cursor]

	return DataList






def main() :
	#re = makeReq('http://pythonpodcast.com/')
	#so = makeSoup(re)
	#gd = getData(so)
	#pd = prepareData(gd)
	cn = connectMongoDB()
	#it = insertData(cn, pd)
	rt = retrievData(cn)
	#print(rt)

if __name__ == '__main__' :
	main()


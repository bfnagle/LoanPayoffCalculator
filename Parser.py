#This module reads the data into a structure and passes it to the main driver
from bs4 import BeautifulSoup
import requests
import os.path
#from twill.commands import *

def readTxtFile(fileName):
	loanData = []
	extension = os.path.splitext(fileName)[1]
	if extension != ".txt":
		return loanData
	try:
		file = open(fileName)
	except:
		return loanData
	for line in file:
		rawData = line.split(",")
		rawData[0] = float(rawData[0])
		rawData[1] = float(rawData[1])
		rawData[1] = rawData[1] / 100
		loanData.append(rawData)

	return loanData

def pullDataFromWebsite(website, username, pin, password):
	#loanData = []
	site = website

	#go(site)
	#showforms()
#	fv("1", "")

	#Pull the website html and pass it to BeautifulSoup
	# siteReq = requests.get(site)
	# page = BeautifulSoup(siteReq.content)

	#Here, we parse the webpage and navigate to the log in page
	# for link in page.find_all('a'):
	# 	if "log in" in link:
	# 		site = link.get('href')
	# 		print(site)
	# 		break

	# siteReq = requests.get(site)
	# page = BeautifulSoup(siteReq.content)

	#Now, parse that webpage and enter username

	#return loanData
#This module reads the data into a structure and passes it to the main driver
import os.path

def readTxtFile(fileName):
	loanData = []
	extension = os.path.splitext(fileName)[1]
	if extension != ".txt":
		print("\nFile needs to be in \".txt\" format.")
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
	# Importing these modules in the function because I cannot install them on my work computer
	# So, if I want to run the code on my work computer, I cannot use these modules
	# Rather than comment/uncomment every time, it is easier to just import only when running web requests
	# If I have to run on my work computer, I can still run from a file
	# If the modules are imported at the top level, then the whole Parser.py program does not work
	from bs4 import BeautifulSoup
	from selenium import webdriver
	from selenium.webdriver.common.keys import Keys
	from selenium.webdriver.chrome.options import Options
	
	loanData = []
	website = website.rstrip('/')
	chrome_options = Options()
	#chrome_options.add_argument("--headless")
	chrome_options.binary_location = 'C:\\Users\\bfnag\\AppData\\Local\\Google\\Chrome SxS\\Application\\chrome.exe'
	driver = webdriver.Chrome(executable_path = os.path.abspath("chromedriver"), chrome_options = chrome_options)
	driver.get(website)
	
	login_page = driver.find_element_by_id("login-link")
	login_page.click()

	userLogin = driver.find_element_by_id("userid")
	userLogin.clear()
	userLogin.send_keys(username)
	userLogin.send_keys(Keys.RETURN)

	try:
		pinPage = driver.find_element_by_id("pinNumber")
		pinPage.clear()
		pinPage.send_keys(pin)
		pinPage.send_keys(Keys.RETURN)
	except:
		print("No Pin Needed")

	passLogin = driver.find_element_by_id("password")
	passLogin.clear()
	passLogin.send_keys(password)
	passLogin.send_keys(Keys.RETURN)

	accountSummary = driver.find_element_by_link_text('Account Summary')
	accountSummary.click()

	accountDetails = driver.find_element_by_link_text('account and loan details')
	accountDetails.click()

	html = driver.page_source
	soup = BeautifulSoup(html, 'html.parser')

	printNext = False
	principal = []
	for box in soup.find_all("div", class_ = "glui-expand-outer LitA-expand"):
		for item in box.find_all("div"):
			if item.text == "Principal Balance":
				printNext = True
			elif printNext:
				loanAmount = item.text.replace("$","")
				if "," in loanAmount:
					loanAmount = loanAmount.replace(",","")
				principal.append(float(loanAmount))
				printNext = False


	interestRates = []
	for box in soup.find_all("div", class_ = "glui-click-to-toggle-outer loan"):
		for item in box.find_all("span", class_ = "LitA-right"):
			interestRates.append(float(item.text.replace("Interest Rate", "").replace("fixed", "").replace(" ", "").replace("%", "").replace("\n", "")) / 100)

	for num in range(len(principal)):
		tmpTuple = []
		tmpTuple.append(principal[num])
		tmpTuple.append(interestRates[num])
		loanData.append(tmpTuple)

	driver.close()

	return loanData
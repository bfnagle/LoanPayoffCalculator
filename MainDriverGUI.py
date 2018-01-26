#Python script to calculate loan payoff date and interest paid
#This module will get data and pass it to another module, which will do the calculation
#Another module will pull information from the website, or, to start out, a txt file
import Parser
import Calculator
from appJar import gui

def pressed(button):
	if button == "Cancel":
		app.stop()
	elif button == "Pull Data":
		try:
			app.clearMessage(feedbackMsg)
		except:
			app.addEmptyMessage(feedbackMsg)
		try:
			app.clearMessage(resultsMsg)
		except:
			app.addEmptyMessage(resultsMsg)

		global loanData
		if app.getRadioButton(radioButton) == fileRadio:
			fileName = app.getEntry("Data File")
			loanData = Parser.readTxtFile(fileName = fileName)
		else:
			username = app.getEntry("Username")
			pin = app.getEntry("Pin")
			password = app.getEntry("Password")
			loanWebsite = "https://" + app.getEntry("Loan Servicer Website") + "/"
			loanData = Parser.pullDataFromWebsite(website = loanWebsite, username = username, pin = pin, password = password)


		if loanData:
			message = ""
			message += "Successfully collected loan principle and interest information!\n"
			for loan in loanData:
				message += ("$" + str(loan[0]) + " at " + "{0:.2f}".format((loan[1] * 100)) + "%\n")
			app.setMessage(feedbackMsg, message)
		else:
			app.setMessage(feedbackMsg,"Failed to properly pull loan data")
			return
	else:
		try:
			app.clearMessage(feedbackMsg)
		except:
			app.addEmptyMessage(feedbackMsg)
		try:
			app.clearMessage(resultsMsg)
		except:
			app.addEmptyMessage(resultsMsg)

		if loanData == []:
			app.setMessage(feedbackMsg, "Pull loan data before calculating")
			return

		try:
			basePayment = float(app.getEntry("Minimum monthly payment"))
			actualPayment = float(app.getEntry("Actual monthly payment"))
			interestThreshold = float(app.getEntry("Interest rate cutoff for extra payments")) / 100.0
		except ValueError as err:
			app.setMessage(feedbackMsg, "Enter payment and interest information before running.")
			return
		extra = actualPayment - basePayment

		if actualPayment < basePayment:
			message += ("\nActual Payment supplied is less than the minimum monthly payment!\n")
			message += ("Using minimum monthly payment as actual payment.")
			app.setMessage(feedbackMsg, message)
			actualPayment = basePayment

		paymentPlan = Calculator.PaymentPlan(basePay = basePayment, actualPay = actualPayment)

		base = paymentPlan.calcBasePaymentInfo(loanData = loanData)

		result = ""
		result += ("Base payoff month: " + str(base[0].getMonth()) + "-" + str(base[0].getYear()) + "\n")
		result += ("Base interest paid: $" + str(base[1]) + "\n")

		savings = paymentPlan.calcActualPaymentInfo(loanData = loanData, rate = interestThreshold)

		result += ("Extra payments payoff month: " + str(savings[0].getMonth()) + "-" + str(savings[0].getYear()) + "\n")
		result += ("Extra payments interest paid: $" + str(savings[1]) + "\n")

		months = (base[0].getYear() - savings[0].getYear()) * 12 + base[0].getMonth() - savings[0].getMonth()
		result += ("Time saved: " + str(months) + " months\n")
		result += ("Interest saved: $" + str(base[1] - savings [1]) + "\n")

		app.setMessage(resultsMsg, result)
		
guiName = "Student Loan Payoff Calculator"
app = gui(guiName, "1000x700")

radioButton = "Loan Data"
fileRadio = "File"
onlineRadio = "Online"
app.addRadioButton(radioButton, fileRadio)
app.addRadioButton(radioButton, onlineRadio)

minField = "Minimum monthly payment"
actualField = "Actual monthly payment"
interestField = "Interest rate cutoff for extra payments"
app.addLabelEntry(minField)
app.setEntryDefault(minField, "300")
app.addLabelEntry(actualField)
app.setEntryDefault(actualField, "500")
app.addLabelEntry(interestField)
app.setEntryDefault(interestField, "6.5")

fileField = "Data File"
app.addFileEntry(fileField)

websiteField = "Loan Servicer Website"
userField = "Username"
pinField = "Pin"
passField = "Password"
app.addLabelEntry(websiteField)
app.setEntryDefault(websiteField, "example.com")
app.addLabelEntry(userField)
app.setEntryDefault(userField, "StudentDebtPayer1")
app.addLabelSecretEntry(pinField)
app.setEntryDefault(pinField, "1234")
app.addLabelSecretEntry(passField)
app.setEntryDefault(passField, "ChangeMe")

app.addButtons(["Calculate", "Pull Data", "Cancel"], pressed)
loanData = []
feedbackMsg = "Feedback"
resultsMsg = "Results"

app.go()
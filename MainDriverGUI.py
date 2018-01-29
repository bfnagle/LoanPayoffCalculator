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
			fileName = app.getEntry(fileField)
			loanData = Parser.readTxtFile(fileName = fileName)
			try:
				if loanData[0] < 0:
					if loanData[0] == -1:
						message = "File needs to be in \".txt\" format."
					elif loanData[0] == -2:
						message = "File did not open properly."
					elif loanData[0] == -3:
						message = "Could not parse file properly. Check data format in file.\n"
						message = message + "Format should be: loan,interestRate\\n. e.g.:\n1000,4.5\n4000,5.1"
					else:
						message = "Unknown error occurred."
					message += "\nPlease try again."
					app.setMessage(feedbackMsg, message)
					return
			except TypeError:
				pass


		else:
			username = app.getEntry(userField)
			pin = app.getEntry(pinField)
			password = app.getEntry(passField)
			if "https" not in app.getEntry(websiteField):
				loanWebsite = "https://" + app.getEntry(websiteField)
			else:
				loanWebsite = app.getEntry(websiteField)

			loanData = Parser.pullDataFromWebsite(website = loanWebsite, username = username, pin = pin, password = password)
			try:
				if loanData[0] < 0:
					if loanData[0] == -1:
						message = "Requested website not yet supported."
					elif loanData[0] == -2:
						message = "Problem accessing website."
					elif loanData[0] == -3:
						message = "Username not accepted."
					elif loanData[0] == -4:
						message = "Pin not accepted."
					elif loanData[0] == -5:
						message = "Password not accepted."
					elif loanData[0] == -6:
						message = "Issue with pulling data from the website."
					else:
						message = "Unknown error occurred."
				message += "\nPlease try again."
				app.setMessage(feedbackMsg, message)
				return
			except TypeError:
				pass


		if len(loanData) != 0:
			message = "Successfully collected loan principle and interest information!\n"
			for loan in loanData:
				message += ("$" + str(loan[0]) + " at " + "{0:.2f}".format((loan[1] * 100)) + "%\n")
			app.setMessage(feedbackMsg, message)
		else:
			app.setMessage(feedbackMsg, "Failed to properly pull loan data")
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

		try:
			if loanData == []:
				app.setMessage(feedbackMsg, "Pull loan data before calculating")
				return
			elif loanData[0] < 0:
				app.setMessage(feedbackMsg, "Data not pulled properly. Retry.")
				return
		except TypeError:
			pass

		try:
			basePayment = float(app.getEntry(minField))
			actualPayment = float(app.getEntry(actualField))
			interestThreshold = float(app.getEntry(interestField)) / 100.0
		except ValueError as err:
			app.setMessage(feedbackMsg, "Enter payment and interest information before running.")
			return

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
#Python script to calculate loan payoff date and interest paid
#This module will get data and pass it to another module, which will do the calculation
#Another module will pull information from the website, or, to start out, a txt file
import Parser
import Calculator
from appJar import gui

def pressed(button):
	if button == "Cancel":
		app.stop()
	else:
		try:
			app.clearMessage("Feedback")
		except:
			app.addEmptyMessage("Feedback")
		try:
			app.clearMessage("Results")
		except:
			app.addEmptyMessage("Results")


		loanData = []
		if app.getRadioButton("Loan Data") == "File":
			fileName = app.getEntry("Data File")
			loanData = Parser.readTxtFile(fileName = fileName)
		else:
			username = app.getEntry("Username")
			pin = app.getEntry("Pin")
			password = app.getEntry("Password")
			loanWebsite = app.getEntry("Loan Servicer Website")
			#Parser.pullDataFromWebsite(website = loanWebsite, username = username, pin = pin, password = password)
			app.setMessage("Feedback", "Web data not yet supported")
			return


		if loanData:
			message = ""
			message += "Successfully collected loan principle and interest information!\n"
			for loan in loanData:
				message += ("$" + str(loan[0]) + " at " + "{0:.2f}".format((loan[1] * 100)) + "%\n")
			app.setMessage("Feedback", message)
		else:
			app.setMessage("Feedback","Failed to properly pull loan data")
			return


		basePayment = float(app.getEntry("Minimum monthly payment"))
		actualPayment = float(app.getEntry("Actual monthly payment"))
		interestThreshold = float(app.getEntry("Interest rate cutoff for extra payments")) / 100.0
		extra = actualPayment - basePayment

		if actualPayment < basePayment:
			message += ("\nActual Payment supplied is less than the minimum monthly payment!\n")
			message += ("Using minimum monthly payment as actual payment.")
			app.setMessage("Feedback", message)
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

		app.setMessage("Results", result)
		

app = gui("Student Loan Payoff Caluclator", "1000x700")

app.addRadioButton("Loan Data", "File")
app.addRadioButton("Loan Data", "Online")

app.addLabelEntry("Minimum monthly payment")
app.setEntryDefault("Minimum monthly payment", "300")
app.addLabelEntry("Actual monthly payment")
app.setEntryDefault("Actual monthly payment", "500")
app.addLabelEntry("Interest rate cutoff for extra payments")
app.setEntryDefault("Interest rate cutoff for extra payments", "6.5")

app.addFileEntry("Data File")

app.addLabelEntry("Loan Servicer Website")
app.setEntryDefault("Loan Servicer Website", "https://www.example.com")
app.addLabelEntry("Username")
app.setEntryDefault("Username", "StudentDebtPayer1")
app.addLabelSecretEntry("Pin")
app.setEntryDefault("Pin", "1234")
app.addLabelSecretEntry("Password")
app.setEntryDefault("Password", "ChangeMe")

app.addButtons(["Calculate", "Cancel"], pressed)

app.go()
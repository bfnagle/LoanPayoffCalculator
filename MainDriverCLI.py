#Python script to calculate loan payoff date and interest paid
#This module will get data and pass it to another module, which will do the calculation
#Another module will pull information from the website, or, to start out, a txt file
import Parser
import Calculator
import sys
import getpass

if len(sys.argv) == 1 or len(sys.argv) > 2:
	print("Add flag -web to use data from the internet or flag -file to pull data from a file.")
	print("1 and only 1 flag must be supplied.")
	exit()

if sys.argv[1] == "-web":
	loanWebsite = input("Enter website of the loan servicer (not all will be supported): ")
	if "https" not in loanWebsite:
		loanWebsite = "https://" + loanWebsite
	loanWebsite = loanWebsite.rstrip("/")

	uname = input("Enter loan servicer username: ")
	pin = getpass.getpass("Enter loan servicer pin: ")
	passwd = getpass.getpass("Enter loan servicer password: ")
	loanData = Parser.pullDataFromWebsite(website = loanWebsite, username = uname, password = passwd, pin = pin)

	try:
		if loanData[0] < 0:
			if loanData[0] == -1:
				message = "\nRequested website not yet supported."
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
		print(message)
		exit()
	except TypeError:
		print("\n")

elif sys.argv[1] == "-file":
	filename = input("Enter name of file where the data is stored, including extension (e.g. data.txt): ")
	loanData = Parser.readTxtFile(filename)
	try:
		if loanData[0] < 0:
			if loanData[0] == -1:
				message = "\nFile needs to be in \".txt\" format."
			elif loanData[0] == -2:
				message = "File did not open properly."
			elif loanData[0] == -3:
				message = "Could not parse file properly. Check data format in file.\n"
				message = message + "Format should be: loan,interestRate\\n. e.g.:\n1000,4.5\n4000,5.1"
			else:
				message = "Unknown error occurred."
			message += "\nPlease try again."
			print(message)
			exit()
	except TypeError:
		print("\n")

else:
	print("Add flag -web to use data from the internet or flag -file to pull data from a file.")
	exit()

if len(loanData) == 0:
	print("Loan data not collected properly. Program exiting.")
	exit()


print("Collected loan principle and interest information:")
i = 1
for loan in loanData:
	print("Loan " + str(i) + ": $" + str(loan[0]) + " at " + "{0:.2f}".format((loan[1] * 100)) + "%")
	i += 1
	
basePayment = float(input("\n\nEnter minimum monthly payment (USD): "))
actualPayment =  float(input("Enter actual monthly payment to make (USD): "))
interestThreshold = float(input("Enter interest rate below which extra payments will not be made (e.g. enter 6.5 for 6.5%): "))
interestThreshold /= 100

if actualPayment < basePayment:
	print("\n\nActual Payment supplied is less than the minimum monthly payment!")
	print("Using minimum monthly payment as actual payment.")
	actualPayment = basePayment

paymentPlan = Calculator.PaymentPlan(basePay = basePayment, actualPay = actualPayment)

print("\nCalculating schedule for base loan payments...\n")
base = paymentPlan.calcBasePaymentInfo(loanData = loanData)

print("\nBase payoff month: " + str(base[0].getMonth()) + "-" + str(base[0].getYear()))
print("Base interest paid: $" + str(base[1]) + "\n\n")

print("Calculating schedule for actual loan payments...\n")
savings = paymentPlan.calcActualPaymentInfo(loanData = loanData, rate = interestThreshold)

print("\nExtra payments payoff month: " + str(savings[0].getMonth()) + "-" + str(savings[0].getYear()))
print("Extra payments interest paid: $" + str(savings[1]) + "\n")

months = (base[0].getYear() - savings[0].getYear()) * 12 + base[0].getMonth() - savings[0].getMonth()
print("\nTime saved: " + str(months) + " months")
print("Interest saved: $" + str(base[1] - savings [1]) + "\n")
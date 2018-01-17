#This module performs the calculation with data received from main
import calendar
import datetime
from copy import deepcopy
from operator import itemgetter

class PaymentPlan:
	def __init__(self, basePay, actualPay):
		self.__basePayment = basePay
		self.__actualPayment = actualPay

	def getBasePayment(self):
		return self.__basePayment

	def getExtraPayment(self):
		return self.__actualPayment - self.__basePayment

	def getActualPayment(self):
		return self.__actualPayment

	def calcBasePaymentInfo(self, loanData):
		tmpData = deepcopy(loanData)
		return self.__calc(loanData = tmpData, payment = self.getBasePayment())

	def calcActualPaymentInfo(self, loanData, rate):
		tmpData = deepcopy(loanData)
		return self.__calc(loanData = tmpData, payment = self.getBasePayment(), extraPay = self.getExtraPayment(), interestThreshold = rate)

	def __calc(self, loanData, payment, extraPay = 0, interestThreshold = 0):
		loanTotal = 0
		totalInterestPaid = 0
		date = MonthYear()

		for loan in loanData:
			loanTotal += loan[0]
		
		while (loanTotal > 0):
			#Sort every time in order to always apply extra payments to the most expensive loan
			if(extraPay != 0):
				loanData = sorted(loanData, key = itemgetter(1,0), reverse = True)

			monthlyInterest = 0
			for loan in loanData:
				monthlyInterest += self.__monthlyInterestPerLoan(loan = loan, date = date)

			totalInterestPaid += monthlyInterest
			remainingPayment = payment - monthlyInterest

			loanTotal = self.__applyBasePayment(loanData = loanData, remainingPayment = remainingPayment, loanTotal = loanTotal, date = date)

			if extraPay != 0:
				self.__applyExtraPayment(payment = extraPay, loanData = loanData, threshold = interestThreshold, date = date)

			if loanTotal != 0:
				date.incrementMonth()

		return [date, totalInterestPaid]

	def __applyBasePayment(self, loanData, remainingPayment, loanTotal, date):
		paidoffLoans = []
		tmpLoan = []
		for loan in loanData:
			tmpLoan.append(loan[0])
		recalc = False
		execOnce = True

		while (recalc or execOnce):
			execOnce = False
			leftover = 0

			if recalc:
				for item in paidoffLoans:
					applied = loanData[item][0]
					leftover += (remainingPayment * loanData[item][0] / loanTotal) - applied
					tmpLoan[item] = 0
			recalc = False

			i = 0

			for loan in loanData:
				if i in paidoffLoans:
					i += 1
					continue

				applied = (remainingPayment * loan[0] / loanTotal) + (leftover * loan[0] / loanTotal)
				if applied > loan[0]:
					applied = loan[0]
					recalc = True
					paidoffLoans.append(i)
					#self.__paidOff(rate = loan[1], date = date)
					break

				tmpLoan[i] = loan[0] - applied
				i += 1

		return self.__copyTmpLoan(loanData = loanData, tmpLoan = tmpLoan)



	def __applyExtraPayment(self, payment, loanData, threshold, date):
		tmpExtra = payment
		for loan in loanData:
			if loan[0] != 0:
				if loan[1] >= threshold:
					if loan[0] > tmpExtra:
						loan[0] -= tmpExtra
						break
					else:
						tmpExtra -= loan[0]
						loan[0] = 0
						#self.__paidOff(rate = loan[1], date = date)

	def __copyTmpLoan(self, loanData, tmpLoan):
		i = 0
		loanTotal = 0

		for loan in loanData:
			loan[0] = tmpLoan[i]
			loanTotal += loan[0]
			i += 1

		return loanTotal


	def __paidOff(self, date, rate):
		print("A loan with interest rate " + "{0:.2f}".format((rate * 100)) + "% was paid off in " + str(date.getMonth()) + "-" + str(date.getYear()))


	def __monthlyInterestPerLoan(self, loan, date):
		days = calendar.monthrange(date.getYear(), date.getMonth())[1]
		if calendar.isleap(date.getYear()):
			daysInYear = 366
		else:
			daysInYear = 365
		return loan[0] * loan[1] * float(days) / float(daysInYear)


class MonthYear:
	def __init__(self):
		today = datetime.date.today()
		self.__month = today.month
		self.__year = today.year


	def incrementMonth(self):
		if self.__month == 12:
			self.__month = 1
			self.incrementYear()
		else:
			self.__month += 1


	def incrementYear(self):
		self.__year += 1


	def getMonth(self):
		return self.__month


	def getYear(self):
		return self.__year
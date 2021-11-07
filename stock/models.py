from django.db import models

# create models here


class BalanceSheet(models.Model):
    id = models.AutoField
    year = models.IntegerField(default=0)
    name = models.CharField(max_length=50)
    product_year = models.CharField(max_length=50, default="")
    shareCapital = models.IntegerField(default=0)
    Reserves = models.IntegerField(default=0)
    Borrowings = models.IntegerField(default=0)
    OtherLiabilities = models.IntegerField(default=0)
    totalLiabilities = models.IntegerField(default=0)
    fixedAssets = models.IntegerField(default=0)
    cwip = models.IntegerField(default=0)
    investments = models.IntegerField(default=0)
    otherAssets = models.IntegerField(default=0)
    totalAssets = models.IntegerField(default=0)

    def __str__(self):
        return self.stockName

class ProfitAndLoss(models.Model):
    name = models.CharField(max_length=50)
    id = models.AutoField
    year = models.IntegerField(default=0)
    sales = models.IntegerField(default=0)
    expenses = models.IntegerField(default=0)
    operatingProfit = models.IntegerField(default=0)
    opm = models.IntegerField(default=0)
    otherIncome = models.IntegerField(default=0)
    interest = models.IntegerField(default=0)
    depreciation = models.IntegerField(default=0)
    pbt = models.IntegerField(default=0)
    tax = models.IntegerField(default=0)
    netProfit = models.IntegerField(default=0)
    eps = models.IntegerField(default=0)
    dividend = models.IntegerField(default=0)


    def __str__(self):
        return self.name

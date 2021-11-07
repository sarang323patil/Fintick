from django.http import HttpResponse
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from .models import ProfitAndLoss
from collections import namedtuple


# 1. Gets Pros and Cons
def getPC(soup, pc):
    # Get pros and cons of a company
    # input => string "pros", "cons"
    cons = soup.find("div",{"class", pc})
    cons = list(cons.children)[3]
    cons = cons.stripped_strings
    companyCons = []
    for item in cons:
        companyCons.append(item)
    return companyCons

# 2. Get the topMost row on table Eg :- dates 
def getTableHead(soup, tableHeading):
    quarters = soup.find(id=tableHeading)
    thead = quarters.find("thead") # for dates which are at the top of the tables
    theadRow = thead.find_all("th")
    myDate = []
    for item in theadRow:
        myDate.append(item.string)
    myDate = myDate[1:]
    return myDate

# 3. Geth other rows of table 
def getTableBody(soup, tableHeading):
    quarters = soup.find(id=tableHeading)
    trows = quarters.find_all("tr")  # for all the other details
    res = []
    for row in trows:
        cur = []
        rows = row.find_all("td")
        for item in rows:
            if(item.string!=None):
                cur.append(item.string.strip())
            # print(item.string, end=" ;,,; ")
        if(len(cur)):
            res.append(cur)
    return res

# 4. Get the table accordingly
def getTable(soup, tableHeading):
    # quarters
    # balance-sheet
    # profit-loss
    # cash-flow
    # ratios
    # shareholding
    myDate = getTableHead(soup, tableHeading)
    body = getTableBody(soup, tableHeading)
    res = []
    res.append(myDate)
    for cur in body:
        res.append(cur)
    return res

# 5. Getting pnl table from database
def getPnl(pnlObj, soup, stockName):
    pnlTerms = ["sales","expenses", "operatingProfit", "opm", "otherIncome", "interest", "depreciation", 
    "pbt", "tax", "netProfit", "eps", "dividend"]
    fetchPnl(pnlObj, stockName, soup, pnlTerms)
    n = len(pnlObj)
    print(n)
    res = []
    head = ["Year"]
    for i in range(2021-n+1, 2022):
        head.append(i)
    res.append(head)
    
    for var in pnlTerms:
        tempList = []
        tempList.append(var)
        for i in range(2021-n+1, 2022):
            tempList.append( getattr(pnlObj.get(year=i), var) )
        res.append(tempList)
    return res

# 6. Fetch Pnl of a particular stock
def fetchPnl(pnlObj, stockName, soup, pnlTerms):
    print("Fecthing......../ ")
    profitLossTable = getTable(soup, "profit-loss")
    profitLossTable = profitLossTable[:13]
    profitLossTable[0] = profitLossTable[0][:-1]
    profitLossTable[1].insert(0, "sales")
    profitLossTable[2].insert(0, "expense")
    profitLossTable[0].insert(0, "Dates")
    # for var in profitLossTable:
    #     print(var)

    for idx in range(len(profitLossTable[0])):
        year = strtonum(profitLossTable[0][idx])
        # print(year)
        if(year>2000):
            try:
                # print(year)
                pnlObj.get(year=year, name=stockName)
            except:
                # create the pnl table object
                print(stockName, year)
                tempObj = ProfitAndLoss.objects.create(year=year, name=stockName, 
                sales = strtonum( profitLossTable[1][idx] ) ,
                expenses = strtonum( profitLossTable[2][idx] ) ,
                operatingProfit = strtonum( profitLossTable[3][idx] ) ,
                opm = strtonum( profitLossTable[4][idx] ) ,
                otherIncome = strtonum( profitLossTable[5][idx] ) ,
                interest = strtonum( profitLossTable[6][idx] ) ,
                depreciation = strtonum( profitLossTable[7][idx] ) , 
                pbt = strtonum( profitLossTable[8][idx] ) ,
                tax = strtonum( profitLossTable[9][idx] ) ,
                netProfit = strtonum( profitLossTable[10][idx] ) ,
                eps = strtonum( profitLossTable[11][idx] ) ,
                dividend = strtonum( profitLossTable[12][idx] ) , 
                )
                tempObj.save()


# 7. Get numbers
def strtonum(s):
    s = s[::-1]
    numset = {"0","1","2","3","4","5","6","7","8","9"}
    res = int(0)
    cnt = int(0)
    for i in range(len(s)):
        if(s[i]=='-'):
            return res*-1
        elif(s[i]=='.'):
            res=0
        elif(s[i] in numset):
            res += int(s[i]) * pow(10, cnt)
            cnt+=1;
    return res;

#  ----- Pages --------------------------------

def index(request):
    print("inside the stock APP")
    # return HttpResponse("Stock Home")
    return render(request, 'stock/index.html')

def display(request):
    stockName = request.GET.get('inStock', 'default')
    r = requests.get("https://www.screener.in/company/" + stockName + "/")
    soup = BeautifulSoup(r.content, 'html.parser')

    pnlObj = ProfitAndLoss.objects.filter(name=stockName)
    pnlTable = getPnl(pnlObj, soup, stockName)
    
    params = {"profitLossTable": pnlTable}

    return render(request, 'stock/display.html', params)




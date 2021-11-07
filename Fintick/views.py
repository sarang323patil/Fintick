from django.http import HttpResponse
from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

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



#  ----- Pages --------------------------------


def index(request):
    return render(request, 'index.html')

def display(request):
    stockName = request.GET.get('inStock', 'default')
    # print(stockName)
    r = requests.get("https://www.screener.in/company/" + stockName + "/")
    soup = BeautifulSoup(r.content, 'html.parser')
    pros = getPC(soup, "pros")
    cons = getPC(soup, "cons")
    quarterTable = getTable(soup, "quarters")
    quarterTable = quarterTable[:-1]
    profitLossTable = getTable(soup, "profit-loss")
    balanceSheetTable = getTable(soup, "balance-sheet")
    cashFlowTable = getTable(soup, "cash-flow")
    shareHoldingTable = getTable(soup, "shareholding")
    ratiosTable = getTable(soup, "ratios")
    params = {}
    params["ratiosTable"] = ratiosTable
    params["shareHoldingTable"] = shareHoldingTable
    params["cashFlowTable"] = cashFlowTable
    params["balanceSheetTable"] = balanceSheetTable
    params["profitLossTable"] = profitLossTable
    params["stockName"] = stockName
    params["pros"] = pros
    params["cons"] = cons
    params["quarterTable"] = quarterTable
    return render(request, 'display.html', params)




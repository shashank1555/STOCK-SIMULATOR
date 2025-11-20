import random
import time

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

stocks = {
    "APPLE": 150,
    "GOOGLE": 2800,
    "AMAZON": 3400,
    "TESLA": 700
}


old_prices = {
    "APPLE": 150,
    "GOOGLE": 2800,
    "AMAZON": 3400,
    "TESLA": 700
}

balance = 10000
portfolio = {}


def update_prices():
    for s in stocks:
        old_prices[s] = stocks[s]           
        change = random.randint(-5,5)
        stocks[s] = stocks[s] + change


def show_market():
    print("\n--- MARKET PRICES ---")

    for s in stocks:
        current = stocks[s]
        previous = old_prices[s]

        if previous != 0:
            percent = ((current - previous) / previous) * 100
        else:
            percent = 0

        
        if percent > 0:
            color = GREEN
            sign = "+"
        elif percent < 0:
            color = RED
            sign = ""
        else:
            color = RESET
            sign = ""

        print(YELLOW + s , ": $", current, RESET, "  ", color + "(" + sign + str(round(percent,2)) + "%)" + RESET)

    print("")


def calc_profit():
    invested = 0
    current = 0

    for s in portfolio:
        qty = portfolio[s]["qty"]
        buy_price = portfolio[s]["buy_price"]
        now = stocks[s]

        invested = invested + (qty * buy_price)
        current = current + (qty * now)

    total = current - invested
    return total


def buy():
    global balance
    show_market()

    stock = input("Enter stock to buy: ").upper()

    if stock not in stocks:
        print(RED + "Invalid stock" + RESET)
        return

    qty = input("Enter quantity: ")

    if not qty.isdigit():
        print(RED + "Invalid quantity" + RESET)
        return

    qty = int(qty)
    cost = qty * stocks[stock]

    if cost > balance:
        print(RED + "Not enough balance" + RESET)
        return

    balance = balance - cost

    if stock in portfolio:
        portfolio[stock]["qty"] = portfolio[stock]["qty"] + qty
    else:
        portfolio[stock] = {"qty": qty, "buy_price": stocks[stock]}

    print(GREEN + "Bought", qty, "shares of", stock, "for $", cost, RESET)


def sell():
    global balance

    if len(portfolio) == 0:
        print(RED + "No stocks to sell" + RESET)
        return

    print("\nYou own:")
    for s in portfolio:
        print(GREEN + s, ":", portfolio[s]["qty"], "shares" + RESET)

    stock = input("\nEnter stock to sell: ").upper()

    if stock not in portfolio:
        print(RED + "You don't own this stock" + RESET)
        return

    qty = input("Enter quantity to sell: ")

    if not qty.isdigit():
        print(RED + "Invalid quantity" + RESET)
        return

    qty = int(qty)

    if qty > portfolio[stock]["qty"]:
        print(RED + "Not enough shares" + RESET)
        return

    sale = qty * stocks[stock]
    balance = balance + sale

    portfolio[stock]["qty"] = portfolio[stock]["qty"] - qty

    if portfolio[stock]["qty"] == 0:
        del portfolio[stock]

    print(GREEN + "Sold", qty, "shares of", stock, "for $", sale, RESET)


def show_portfolio():
    print("\n--- YOUR PORTFOLIO ---")

    if len(portfolio) == 0:
        print("No stocks owned")
        print("Balance: $", balance)
        return

    for s in portfolio:
        qty = portfolio[s]["qty"]
        buy = portfolio[s]["buy_price"]
        now = stocks[s]

        invested = qty * buy
        curr = qty * now
        profit = curr - invested

        print(s, ":", qty, "shares")
        print(" Buy Price: $", buy)
        print(" Current Price: $", now)
        print(" Current Value: $", curr)

        if profit >= 0:
            print(" ", GREEN + "Profit: $", profit, RESET, "\n")
        else:
            print(" ", RED + "Loss: $", abs(profit), RESET, "\n")

    print("Balance: $", balance)

while True:
    update_prices()
    diff = calc_profit()

    print("\n===== STOCK MARKET SIMULATOR =====")
    print("Balance: $", balance)

    if diff > 0:
        print(GREEN + "Profit: $", diff, RESET)
    elif diff < 0:
        print(RED + "Loss: $", abs(diff), RESET)
    else:
        print("Profit/Loss: $0")

    print("\n1. View Market")
    print("2. Buy Stock")
    print("3. Sell Stock")
    print("4. View Portfolio")
    print("5. Exit\n")

    choice = input("Choose an option: ")

    if choice == "1":
        show_market()
    elif choice == "2":
        buy()
    elif choice == "3":
        sell()
    elif choice == "4":
        show_portfolio()
    elif choice == "5":
        print("Thank you!")
        break
    else:
        print(RED + "Invalid choice" + RESET)

    time.sleep(1)

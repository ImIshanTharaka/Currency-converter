from requests import get
from pprint import PrettyPrinter  # pprint is a built-in module

BASE_URL = "https://free.currconv.com"  # send the request to this url
API_KEY = "4192fb3af2e24de10b07"

# printer = PrettyPrinter()  allows to get nicely formatted output for json

def get_currencies():
    endpoint = f"/api/v7/currencies?apiKey={API_KEY}"   # what's starts with a ? is a query parameter - some data that send to the url (here API_KEY)
    url = BASE_URL + endpoint
    data = get(url).json()['results']   # get data from the url as a json and get the value of the key "results"
    data = list(data.items())  # convert data dict to a list of tuples
    data.sort()  # make list items ascending order
    return data

def print_currencies(currencies):
    for name, currency in currencies:   # currencies will be a list of tuples --> tuple has two items-string(name) and a dictionary(currency)
        name = currency['currencyName']  # getting values from the dictionary
        _id = currency['id']
        symbol = currency.get("currencySymbol", "")     # .get try to find the key "currencysymbol", if it exist gives the value, otherwise will return " "
        print(f"{_id} - {name} - {symbol}")

def exchange_rate(currency1, currency2):
    endpoint = f"/api/v7/convert?q={currency1}_{currency2}&compact=ultra&apiKey={API_KEY}"       # after ? query parameters
    url = BASE_URL + endpoint
    data = get(url).json()
    if len(data) == 0:
        print("Invalid currencies")
        return
    rate = list(data.values())[0]
    print(f"{currency1} --> {currency2} = {rate}")
    return rate

def convert(currency1, currency2, amount):
    rate = exchange_rate(currency1, currency2)
    if rate is None:
        return
    try:
        amount = float(amount)
    except:
        print("Invalid amount")
        return
    converted_amount = rate*amount
    print(f"{amount}{currency1} is equal to {converted_amount} {currency2}")
    return converted_amount

def main():
    currencies = get_currencies()

    print("Welcome to currency converter..!")
    print("List - list the different currencies")
    print("Convert - convert from one currency to another")
    print("Rate - get exchange rate of two currencies")
    print()  # print a blank line

    while True: 
        command = input("Enter a command (q to quit):").lower()     # convert string to lowercase
        if command == "q":
            break
        elif command == "list":
            print_currencies(currencies)
        elif command == "convert":
            currency1 = input("Enter a base currency:").upper()
            amount = input(f"Enter an amount in {currency1}:")
            currency2 = input("Enter a currency to convert to:").upper()
            convert(currency1, currency2, amount)
        elif command == "rate":
            currency1 = input("Enter a base currency:").upper()
            currency2 = input("Enter a currency to convert to:").upper()
            exchange_rate(currency1, currency2)
        else:
            print("Unrecognized command!")
main()
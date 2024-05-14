import requests
import tkinter as tk
from tkinter import messagebox
import time

def get_bitcoin_price(currency):
    if currency == "BRL":
        url = "https://api.coindesk.com/v1/bpi/currentprice/BRL.json"
    else:
        url = f"https://api.coindesk.com/v1/bpi/currentprice/{currency}.json"
    
    response = requests.get(url)
    data = response.json()
    price = data["bpi"][currency]["rate_float"]
    return price

def get_currency_symbol(currency):
    currency_symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "BRL": "R$"
    }
    return currency_symbols.get(currency, "")

def is_price_increasing(last_price, current_price):
    return current_price > last_price

def notify(last_price, current_price, currency):
    price_change = current_price - last_price
    message = ""

    if price_change > 0:
        message += "O preço do Bitcoin está em alta!\n"
    elif price_change < 0:
        message += "O preço do Bitcoin está em baixa!\n"
    else:
        message += "O preço do Bitcoin permanece inalterado.\n"

    currency_symbol = get_currency_symbol(currency)
    message += f"Valor anterior: {currency_symbol}{last_price:.2f}\n"
    message += f"Valor atual: {currency_symbol}{current_price:.2f}\n"

    if current_price < last_price:
        message += "Sugestão: Este pode ser um bom momento para comprar Bitcoin!"

    return message

def calculate_value(bitcoin_amount, current_price):
    return bitcoin_amount * current_price

def update_label():
    selected_currency = currency_var.get()
    current_price = get_bitcoin_price(selected_currency)
    message = notify(last_price.get(), current_price, selected_currency)
    value_in_usd = calculate_value(bitcoin_amount.get(), current_price)
    message += f"\nValor do seu Bitcoin: ${value_in_usd:.2f} {get_currency_symbol(selected_currency)}"
    label.config(text=message)
    last_price.set(current_price)

def update_info():
    update_label()

root = tk.Tk()
root.title("Verificador de Preço do Bitcoin")

last_price = tk.DoubleVar()
last_price.set(get_bitcoin_price("USD"))

currency_var = tk.StringVar()
currency_var.set("USD")

bitcoin_amount = tk.DoubleVar()
bitcoin_amount.set(1.0)

currency_label = tk.Label(root, text="Escolha a moeda:")
currency_label.pack(padx=20, pady=5)

currency_options = ["USD", "EUR", "GBP", "BRL"]  # Adicione mais moedas, se desejar
currency_menu = tk.OptionMenu(root, currency_var, *currency_options)
currency_menu.pack(padx=20, pady=5)

amount_label = tk.Label(root, text="Quantidade de Bitcoin:")
amount_label.pack(padx=20, pady=5)

amount_entry = tk.Entry(root, textvariable=bitcoin_amount)
amount_entry.pack(padx=20, pady=5)

update_button = tk.Button(root, text="Atualizar", command=update_info)
update_button.pack(padx=20, pady=10)

label = tk.Label(root, text="Preço inicial do Bitcoin: $" + str(last_price.get()), font=("Helvetica", 14))
label.pack(padx=20, pady=20)

update_label()

root.mainloop()

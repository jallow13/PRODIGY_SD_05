import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import ttk

URL = "https://books.toscrape.com/catalogue/category/books_1/page-2.html"

response = requests.get(URL)
web_page = response.text

soup = BeautifulSoup(web_page, 'html.parser')


products = soup.select("h3 a")
products_title = [product.get('title') for product in products]

product_price = [price.getText() for price in soup.find_all(name='p', class_='price_color')]
ratings = soup.select("p.star-rating")
product_rating = [rating.get('class')[1] for rating in ratings]

# Create a CSV file and write the data
with open('books.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Price', 'Rating'])
    for title, price, rating in zip(products_title, product_price, product_rating):
        writer.writerow([title, price, rating])

data = {
    'Title': products_title,
    'Price': product_price,
    'Rating': product_rating
}
df = pd.DataFrame(data)


def display_data(df):
    root = tk.Tk()
    root.title("Books Data")

    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(frame, columns=list(df.columns), show='headings')
    tree.pack(fill=tk.BOTH, expand=True)

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor=tk.CENTER)

    for index, row in df.iterrows():
        tree.insert("", "end", values=list(row))

    root.mainloop()


# Display in GUI
display_data(df)
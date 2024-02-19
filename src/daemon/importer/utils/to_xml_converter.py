import csv
import xml.etree.ElementTree as ET
from entities.country import Country
from entities.product import Product
from entities.order import Order

class CSVtoXMLConverter:
    def __init__(self, path):
        self._path = path
        self.products = {}
        self.countries = {}

    def process_csv(self):
        with open(self._path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                country_name = row["Country"]
                if country_name not in self.countries:
                    self.countries[country_name] = Country(country_name)

                stock_code = row["StockCode"]
                if stock_code not in self.products:
                    self.products[stock_code] = Product(stock_code, row["Description"])

                order = Order(row["InvoiceNo"], row["Quantity"], row["InvoiceDate"], row["UnitPrice"])
                self.products[stock_code].add_order(order)

    def to_xml(self):
        self.process_csv()
        root_el = ET.Element("SalesData")

        countries_el = ET.Element("Countries")
        for country in self.countries.values():
            countries_el.append(country.to_xml())
        root_el.append(countries_el)

        products_el = ET.Element("Products")
        for product in self.products.values():
            products_el.append(product.to_xml())
        root_el.append(products_el)

        return root_el

    def to_xml_str(self):
        root_el = self.to_xml()
        return ET.tostring(root_el, encoding='utf-8').decode()



import xml.etree.ElementTree as ET

class Product:
    counter = 0
    def __init__(self, stock_code, description):
        Product.counter += 1
        self._id = Product.counter
        self._stock_code = stock_code
        self._description = description
        self._orders = []

    def add_order(self, order):
        self._orders.append(order)

    def to_xml(self):
        el = ET.Element("Product")
        el.set("id", str(self._id))
        el.set("stock_code", self._stock_code)
        el.set("description", self._description)

        orders_el = ET.Element("Orders")
        for order in self._orders:
            orders_el.append(order.to_xml())
        el.append(orders_el)

        return el

    def __str__(self):
        return f"Product {self._description} with stock code {self._stock_code}"

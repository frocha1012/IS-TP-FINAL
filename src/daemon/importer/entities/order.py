import xml.etree.ElementTree as ET

class Order:
    counter = 0
    def __init__(self, invoice_no, quantity, invoice_date, unit_price):
        Order.counter += 1
        self._id = Order.counter
        self._invoice_no = invoice_no
        self._quantity = quantity
        self._invoice_date = invoice_date
        self._unit_price = unit_price

    def to_xml(self):
        el = ET.Element("Order")
        el.set("id", str(self._id))
        el.set("invoice_no", self._invoice_no)
        el.set("quantity", str(self._quantity))
        el.set("invoice_date", self._invoice_date)
        el.set("unit_price", str(self._unit_price))
        return el

import xml.etree.ElementTree as ET

class Country:
    counter = 0
    def __init__(self, name):
        Country.counter += 1
        self._id = Country.counter
        self._name = name

    def to_xml(self):
        el = ET.Element("Country")
        el.set("id", str(self._id))
        el.set("country", self._name)
        return el

    def get_id(self):
        return self._id

    def __str__(self):
        return f"country: {self._name}, id: {self._id}"
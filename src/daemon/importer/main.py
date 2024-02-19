import asyncio
import os
import time
import uuid
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent
from utils.to_xml_converter import CSVtoXMLConverter
from utils.connectionDb import Database
import xml.etree.ElementTree as ET
import math


NUM_XML_PARTS = 50
PARTS_PER_DIRECTORY = 10 


def insert_imported_document(cursor, file_name, xml_content):
    insert_query = """INSERT INTO public.imported_documents(file_name, xml) VALUES (%s, %s);"""
    cursor.execute(insert_query, (file_name, xml_content))


def insert_converted_document(cursor, src, file_size, dst, xml_part_content):
    insert_query = """INSERT INTO public.converted_documents(src, file_size, dst, xml_part) VALUES (%s, %s, %s, %s);"""
    cursor.execute(insert_query, (src, file_size, dst, xml_part_content))



def split_xml_file(original_xml_path, output_directory):
    tree = ET.parse(original_xml_path)
    root = tree.getroot()
    total_elements = len(root)
    elements_per_file = math.ceil(total_elements / NUM_XML_PARTS)
    splitted_files = []

    for i in range(NUM_XML_PARTS):
        
        dir_num = i // PARTS_PER_DIRECTORY
        subdirectory = f"{output_directory}/dir_{dir_num}"
        os.makedirs(subdirectory, exist_ok=True)  

    
        start = i * elements_per_file
        end = start + elements_per_file
        part_elements = root[start:end]
        
        new_root = ET.Element(root.tag, root.attrib)
        new_tree = ET.ElementTree(new_root)
        for elem in part_elements:
            new_root.append(elem)

        part_filename = f"{subdirectory}/{str(uuid.uuid4())}.xml"
        new_tree.write(part_filename)
        splitted_files.append(part_filename)
        print(f"Created {part_filename}")

    return splitted_files



def convert_csv_to_xml(in_path, out_path):
    converter = CSVtoXMLConverter(in_path)
    file = open(out_path, "w")
    file.write(converter.to_xml_str())
    return out_path


class CSVHandler(FileSystemEventHandler):
    def __init__(self, input_path, output_path):
        self._output_path = output_path
        self._input_path = input_path

        # generate file creation events for existing files
        for file in get_csv_files_in_input_folder(self._input_path):
            event = FileCreatedEvent(file)
            self.dispatch(event)

    async def convert_csv(self, csv_path):
        db = Database()
        db.connect()

        # Generate a unique file name for the XML file
        xml_file_name = os.path.basename(generate_unique_file_name(self._output_path))

        if db.is_file_already_converted(xml_file_name):
            print(f"The file {xml_file_name} has already been converted. Skipping...")
            db.cursor.close()
            db.connection.close()
            return

        print(f"New file to convert: '{csv_path}'")
        xml_path = generate_unique_file_name(self._output_path)
        convert_csv_to_xml(csv_path, xml_path)
        print(f"New XML file generated: '{xml_path}'")

        with open(xml_path, 'r') as file:
            xml_content = file.read()
            insert_imported_document(db.cursor, xml_file_name, xml_content)
            db.connection.commit()

            splitted_files = split_xml_file(xml_path, self._output_path)
            for part_filename in splitted_files:
                with open(part_filename, 'r') as part_file:
                    xml_part_content = part_file.read()  # Read the content of the XML part
                
                part_size = os.path.getsize(part_filename)
                part_src = os.path.basename(part_filename)
                insert_converted_document(db.cursor, part_src, part_size, part_src, xml_part_content)  # Pass the content of the XML part
                db.connection.commit()

        db.cursor.close()
        db.connection.close()


    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".csv"):
            asyncio.run(self.convert_csv(event.src_path))


def get_csv_files_in_input_folder(input_path):
    return [os.path.join(dp, f) for dp, dn, filenames in os.walk(input_path) for f in filenames if
            os.path.splitext(f)[1] == '.csv']


def generate_unique_file_name(directory):
    return f"{directory}/{str(uuid.uuid4())}.xml"


if __name__ == "__main__":

    CSV_INPUT_PATH = "/csv"  
    XML_OUTPUT_PATH = "/xml"  

    observer = Observer()
    observer.schedule(
        CSVHandler(CSV_INPUT_PATH, XML_OUTPUT_PATH),
        path=CSV_INPUT_PATH,
        recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

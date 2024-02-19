import time
import os
import psycopg2
import pika
import logging

# Setup basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Environment variables for database connection
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'is')
DB_USER = os.getenv('DB_USER', 'is')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'is')

# Environment variables for RabbitMQ connection
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_USER = os.getenv('RABBITMQ_DEFAULT_USER', 'is')
RABBITMQ_PASS = os.getenv('RABBITMQ_DEFAULT_PASS', 'is')
RABBITMQ_VHOST = os.getenv('RABBITMQ_DEFAULT_VHOST', 'is')

# Polling frequency (in seconds)
POLLING_FREQ = int(os.getenv('POLLING_FREQ', 5))

# Establish a connection to RabbitMQ
credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
parameters = pika.ConnectionParameters(RABBITMQ_HOST, 5672, RABBITMQ_VHOST, credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Declare the queue where messages will be published
channel.queue_declare(queue='xml_import_tasks')

def get_db_connection():
    """Establish a connection to the PostgreSQL database."""
    return psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)

def poll_db_and_publish_messages():
    """Poll the database for new or updated XML files and publish messages to RabbitMQ."""
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            # Select new or updated files
            cursor.execute(""" SELECT id, src FROM converted_documents WHERE is_processed = FALSE; """)
            files = cursor.fetchall()

            # Log the number of new/updated files found
            logging.info(f"Found {len(files)} new/updated file(s).")
            
            for file in files:
                file_id, file_name = file
                
                # Log the details of the file
                logging.info(f"Processing file: {file_name} with id: {file_id}")

                # Construct the message
                message = f"Process file: {file_name} with id: {file_id}"
                
                # Publish the message to RabbitMQ
                channel.basic_publish(
                    exchange='',
                    routing_key='xml_import_tasks',
                    body=message
                )
                
                # Log the publishing action
                logging.info(f"Published message for file: {file_name}")

if __name__ == '__main__':
    try:
        while True:
            poll_db_and_publish_messages()
            time.sleep(POLLING_FREQ)
    except KeyboardInterrupt:
        logging.info('Watcher stopped.')
    finally:
        connection.close()
        logging.info('RabbitMQ connection closed.')

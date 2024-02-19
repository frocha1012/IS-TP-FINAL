import psycopg2

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.user = "is"
        self.password = "is"
        self.host = "db-xml"
        self.port = "5432"
        self.database = "is"

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            print("\nDatabase connection established successfully.")
        except psycopg2.Error as error:
            print(f"\nDatabase connection error: {error}")
            self.connection = None
            self.cursor = None

    def is_file_already_converted(self, file_name):
        if self.connection is None or self.cursor is None:
            print("Database connection is not established.")
            return False 
        try:
            query = "SELECT EXISTS(SELECT 1 FROM public.converted_documents WHERE src = %s)"
            self.cursor.execute(query, (file_name,))
            return self.cursor.fetchone()[0]
        except psycopg2.Error as error:
            print(f"Error checking if file is already converted: {error}")
            return False
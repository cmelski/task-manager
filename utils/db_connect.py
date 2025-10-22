import os

import psycopg

class DBConnect:
    def __init__(self):

        self.connection = psycopg.connect(os.environ.get('DB_HOST'))

        self.cursor = self.connection.cursor()

    def commit(self):
        """Commit current transaction"""
        self.connection.commit()

    def close(self):
        """Close cursor and connection"""
        self.cursor.close()
        self.connection.close()


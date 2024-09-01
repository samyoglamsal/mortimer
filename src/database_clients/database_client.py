import logging
import sqlite3
import os

from datetime import datetime

class DatabaseClient:
    DATABASE_FOLDER = "db"
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.connection = self._create_connection("stats.db")
        self.cursor = self.connection.cursor()

    def _create_connection(self, filename: str):
        if not os.path.exists(filename):
            os.mknod(os.path.join(self.DATABASE_FOLDER, filename))

        return sqlite3.connect(filename)

    ###########################################################################
    #                                                                         #
    # SHITSHEET COMMANDS                                                      #
    #                                                                         #
    ###########################################################################

    def add_shitsheet_entry(self, user_id, user_name):
        # Check if table "shitsheet" exists, create if not
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='shitsheet'")
        if not self.cursor.fetchone():
            self.logger.info(f"Table 'shitsheet' does not exist, creating...")
            self.cursor.execute("CREATE TABLE shitsheet (timestamp TEXT PRIMARY KEY, user_id INTEGER, user_name TEXT)")

        current_time = datetime.now().isoformat()
        self.cursor.execute("INSERT INTO shitsheet VALUES (?, ?, ?)", (current_time, user_id, user_name))
        self.connection.commit()
        self.logger.info(f"Successfully inserted ({current_time}, {user_id}, {user_name}) into table shitsheet")

    def get_shitsheet_entries_by_user_id(self, user_id):
        self.cursor.execute("SELECT * FROM shitsheet WHERE user_id=?", (user_id,))
        return self.cursor.fetchall()

    ###########################################################################
    #                                                                         #
    # MORTIMER STATISTICS COMMANDS                                            #
    #                                                                         #
    ###########################################################################

    def add_mortimer_bald_count(self, count: int):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='mortimer'")
        if not self.cursor.fetchone():
            self.logger.info(f"Table 'mortimer' does not exist, creating...")
            self.cursor.execute("CREATE TABLE mortimer (timestamp TEXT PRIMARY KEY, count INTEGER)")

        current_time = datetime.now().isoformat()
        self.cursor.execute("INSERT INTO mortimer VALUES (?, ?)", (current_time, count))
        self.connection.commit()
        self.logger.info(f"Successfully inserted ({current_time}, {count}) into table mortimer")


    def get_mortimer_bald_counts(self):
        self.cursor.execute("SELECT * FROM mortimer")
        return self.cursor.fetchall()
import datetime
import logging
import sqlite3

class DatabaseClient:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.connection = sqlite3.connect("db/stats.db")
        self.cursor = self.connection.cursor()

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

        current_time = datetime.datetime.now().isoformat()
        self.cursor.execute("INSERT INTO shitsheet VALUES (?, ?, ?)", (current_time, user_id, user_name))
        self.connection.commit()
        self.logger.info(f"Successfully inserted ({current_time}, {user_id}, {user_name}) into table shitsheet")

    def get_shitsheet_entries_by_user_id(self, user_id):
        self.cursor.execute("SELECT * FROM shitsheet WHERE user_id=?", (user_id,))
        return self.cursor.fetchall()

import os
import sqlite3

DATABASE_FILE_PATH = os.path.relpath("src/database/files/db.sqlite")

class DatabaseClient:
    def __init__(self):
        self.con = sqlite3.connect(DATABASE_FILE_PATH) # Creates file if it doesn't exist

    def get_user_info(self, id: str) -> tuple:
        """
        Gets the row in the database corresponding to the user's Discord ID.
        """
        cur = self.con.cursor()
        res = cur.execute("SELECT * FROM users WHERE id = ?", (id,))
        row = res.fetchone()
        return row

    def execute_command(self, command: str, values: tuple | None = None):
        """
        Executes a given SQL command.
        """

        cur = self.con.cursor()
        if values:
            cur.execute(command, values)
        else:
            cur.execute(command)
        self.con.commit()
        

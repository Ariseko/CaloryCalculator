import sqlite3


class Database:
    def __init__(self, database_file):
        self.conn = sqlite3.connect(database_file)
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        with self.conn:
            result = self.cursor.execute("SELECT * FROM users WHERE tg_id = ?", (user_id,)).fetchmany(1)
            return bool(len(result))

    def add_user(self, user_id, username, date):
        with self.conn:
            return self.cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (user_id, username, date,))

    def update_message(self, text, entities):
        with self.conn:
            return self.cursor.execute("UPDATE messages SET text = (?), entities = (?) WHERE id = 0", (text, entities,))

    def update_message_for_broadcast(self, text, entities):
        with self.conn:
            return self.cursor.execute("UPDATE messages SET text = (?), entities = (?) WHERE id = 1", (text, entities,))

    def get_users(self):
        with self.conn:
            return self.cursor.execute("SELECT tg_id FROM users").fetchall()

    def get_messages(self):
        with self.conn:
            return self.cursor.execute("SELECT text, entities FROM messages WHERE id = 0").fetchone()

    def get_messages_for_broadcast(self):
        with self.conn:
            return self.cursor.execute("SELECT text, entities FROM messages WHERE id = 1").fetchone()

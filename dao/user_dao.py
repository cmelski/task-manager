class User_DAO:

    def __init__(self, db_connect):

        self.connect = db_connect

    def get_user_by_name(self, user_name):

        self.connect.cursor.execute("SELECT id, email, name FROM users WHERE name = %s", (user_name,))
        row = self.connect.cursor.fetchone()
        return row

    def delete_user(self, user_email):
        self.connect.cursor.execute("""
                                    DELETE FROM users
                                    WHERE email = %s;
                                    """,
                           (user_email,)
                           )
        self.connect.connection.commit()



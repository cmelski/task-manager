class User_DAO:

    def __init__(self, db_connect):

        self.connect = db_connect

    def get_user_by_email(self, user_email):

        self.connect.cursor.execute("SELECT id, email, name FROM users WHERE email = %s", (user_email,))
        row = self.connect.cursor.fetchone()
        return row

    def delete_user_by_user_email(self, user_email):
        self.connect.cursor.execute("""
                                    DELETE FROM users
                                    WHERE email = %s;
                                    """,
                           (user_email,)
                           )
        self.connect.connection.commit()



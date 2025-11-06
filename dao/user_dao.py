class User_DAO:

    def __init__(self, db_connect):
        self.connect = db_connect

    def get_user_by_email(self, user_email):
        cursor = self.connect.cursor()
        cursor.execute("SELECT id, email, name FROM users WHERE email = %s", (user_email,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def delete_user_by_user_email(self, user_email):
        cursor = self.connect.cursor()
        cursor.execute("""
                                    DELETE FROM users
                                    WHERE email = %s;
                                    """,
                       (user_email,)
                       )
        self.connect.connection.commit()

    def get_tasks_by_assignee_not_completed(self, user_id):
        cursor = self.connect.cursor()
        cursor.execute("""
            SELECT COALESCE(a.assignee, 'Unassigned') AS assignee, COUNT(*) AS open_task_count
            FROM items a
            JOIN list b ON a.list_id = b.id
            JOIN users c ON b.user_id = c.id
            WHERE c.id = %s AND a.completed = false
            GROUP BY COALESCE(a.assignee, 'Unassigned')
            ORDER BY assignee ASC;
        """, (user_id,))
        rows = cursor.fetchall()
        cursor.close()
        return rows

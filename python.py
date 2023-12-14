import sqlite3

connection_string = "todo.sqlite"

conn = sqlite3.connect(connection_string)

c = conn.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS todo (
    todo_int integer PRIMARY KEY,
    content text NOT NULL,
    created text
    )
""")


class ToDoApp:
    def __init__(self, db):
        self.db = db

    def chose_action(self):
        print("1 for creating a todo")
        print("2 for listing all existing todos")
        print("3 for deleting specific todos")
        print("4 for searching specific todos")

        inp = input("Enter your action number here: \n")

        if inp == "1":
            print("You chose to create a todo")
            inp_content = input("What is your todo? \n")
            if inp_content:
                c.execute("""
                    INSERT INTO todo (content, created)
                    VALUES (?, datetime('now'))
                """, (inp_content,))
                conn.commit()
                myTodos.chose_action()

        elif inp == "2":
            print("You chose to list all existing todos")
            c.execute("""
                SELECT * FROM todo
            """)
            results = c.fetchall()
            for result in results:
                print(result)
            conn.commit()
            myTodos.chose_action()

        elif inp == "3":
            print("You chose delete a certain todo")
            inp_delete = input("What is the task you want to delete? \n")
            if inp_delete:
                c.execute("""
                    DELETE FROM todo
                    WHERE content = ?
                """, (inp_delete,))
                print(f"You deleted {inp_delete}")
                conn.commit()
                myTodos.chose_action()

        elif inp == "4":
            print("You chose to search for a certain todo")
            inp_search = input("What task are you searching? \n")
            if inp_search:
                c.execute("""
                    SELECT todo_int, content, created FROM todo
                    WHERE content LIKE ?
                """, ("%" + inp_search + "%",))
                results = c.fetchall()
                for result in results:
                    print(result)
            conn.commit()
            myTodos.chose_action()


myTodos = ToDoApp(conn)

myTodos.chose_action()

conn.commit()
conn.close()

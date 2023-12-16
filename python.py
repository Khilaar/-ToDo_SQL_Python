import sqlite3

connection_string = "todo.sqlite"

conn = sqlite3.connect(connection_string)
c = conn.cursor()

class ToDoApp:
    def __init__(self, db):
        self.db = db
        self.selected_table = ""

    def chose_action(self):
        print(f"What do you want to do with the table {self.selected_table}? \n")
        print("1 for creating a todo")
        print("2 for listing all existing todos")
        print("3 for deleting specific todos")
        print("4 for searching specific todos")
        print("5 for changing table")

        inp = input("Enter your action number here: \n")

        if inp == "1":
            print("You chose to create a todo")
            inp_content = input("What is your todo? \n")
            due_date = input("If you want to add a due date write the date 'dd,mm,yyyy' in the next line: \n")
            if inp_content:
                c.execute(f"""
                            INSERT INTO {self.selected_table} (content, created, due_date)
                            VALUES (?, datetime('now'), ?)
                        """, (inp_content, due_date))
                conn.commit()
                self.chose_action()

        elif inp == "2":
            print("You chose to list all existing todos")
            c.execute(f"""
                SELECT * FROM {self.selected_table}
            """)
            results = c.fetchall()
            for result in results:
                print(result)
            print("\n")
            conn.commit()
            self.chose_action()

        elif inp == "3":
            print("You chose to delete a certain todo")
            inp_delete = input("What is the task you want to delete? \n")
            if inp_delete:
                c.execute(f"""
                    DELETE FROM {self.selected_table}
                    WHERE content = ?
                """, (inp_delete,))
                print(f"You deleted {inp_delete}")
                conn.commit()
                self.chose_action()

        elif inp == "4":
            print("You chose to search for a certain todo")
            inp_search = input("What task are you searching? \n")
            if inp_search:
                c.execute(f"""
                    SELECT todo_int, content, created FROM {self.selected_table}
                    WHERE content LIKE ?
                """, ("%" + inp_search + "%",))
                results = c.fetchall()
                for result in results:
                    print(result)
            conn.commit()
            self.chose_action()

        elif inp == "5":
            start_options()

myTodos = ToDoApp(conn)

def start_options():
    print("What do you want to do?")
    print("1. Show all tables")
    print("2. Choose a table and work on it")
    print("3. Create a new table")

    start_input = input("Type the number you want to execute on the next line \n")
    if start_input == "1":
        c.execute("""
                    SELECT name FROM sqlite_master WHERE type='table';
                    """)
        tables = c.fetchall()
        print("List of tables:")
        for table in tables:
            print(table[0])
        print("\n")
        start_options()
    elif start_input == "2":
        myTodos.selected_table = input("Type the name of the table you want to work on on the next line: \n")
        myTodos.chose_action()
    elif start_input == "3":
        new_table_name = input("Insert below this line how your new table should be called: \n")
        c.execute(f"""
                CREATE TABLE IF NOT EXISTS {new_table_name} (
                    todo_int integer PRIMARY KEY,
                    content text NOT NULL,
                    created text,
                    due_date text
                )
            """)
        print(f"Table '{new_table_name}' created successfully. \n")
        start_options()

start_options()
conn.commit()
conn.close()
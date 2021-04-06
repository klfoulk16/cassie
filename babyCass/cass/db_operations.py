"""Handles cassQL operations"""


def insert(database, table_name, columns, values):
    print("INSERT CALLED")
    # put values in database
    with open(database, "a") as file:
        data = str({table_name: {
            columns[i]: values[i] for i in range(len(columns))
        }})
        file.write(f"{data}\n")

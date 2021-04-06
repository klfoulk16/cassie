"""Handles cassQL operations"""
import json

def insert(database, table_name, columns, values):
    print("INSERT CALLED")
    # put values in database
    with open(database, "a") as file:
        data = {table_name: {
            columns[i]: values[i] for i in range(len(columns))
        }}
        file.write(json.dumps(data) + '\n')


def select(database, table_name):
    print("SELECT CALLED")
    with open(database, "r") as file:
        table_contents = []
        entries = [json.loads(line) for line in file.readlines()]
        for entry in entries:
            if table_name in entry:
                table_contents.append(entry[table_name])
    return table_contents
    
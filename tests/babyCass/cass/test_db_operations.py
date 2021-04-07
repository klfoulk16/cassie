import pytest
import tempfile
import babyCass.cass.db_operations as db_operations


def test_insert():
    """Assert that correct values are inserted into db file"""
    database = tempfile.NamedTemporaryFile()
    table_name = 'table_name'
    columns = ['col1', 'col2', 'col3']
    values = ['val1', 'val2', 'val3']
    db_operations.insert(database.name, table_name, columns, values)
    with open(database.name, "r") as file:
        assert file.readline() == "{'table_name': {'col1': 'val1', 'col2': 'val2', 'col3': 'val3'}}\n"
import babyCass.cassQL.tokens as tokens
import babyCass.cass.db_operations as db_operations
import sys


class cassParser:
    def __init__(self, lexer):
        self.lexer = lexer

        self.current_token = None
        self.peek_token = None
        self.next_token()
        self.next_token()

    def check_token(self, kind):
        return kind == self.current_token.kind

    def check_peek(self, kind):
        return kind == self.peek_token.kind

    def match(self, kind):
        if not self.check_token(kind):
            print(f"Expected {kind.name}, got {self.current_token.kind.name}")
            self.abort(f"Expected {kind.name}, got {self.current_token.kind.name}")
        self.next_token()

    def next_token(self):
        self.current_token = self.peek_token
        self.peek_token = self.lexer.get_token()

    def abort(self, message):
        sys.exit(f"Error. {message}")
    
    # Production rules.

    # program ::= {statement}
    def program(self):
        print("PROGRAM")

        # Parse all the statements in the program.
        while not self.check_token(tokens.TokenType.END):
            self.statement()

    # One of the following statements...
    def statement(self):
        # Check the first token to see what kind of statement this is.
        
        # "INSERT"
        if self.check_token(tokens.TokenType.INSERT):
            print("STATEMENT-INSERT")
            self.next_token()
            self.match(tokens.TokenType.INTO)
            self.match(tokens.TokenType.IDENTIFIER)    # do I need to specify what type of identifier?
            length = self.column_items()
            self.match(tokens.TokenType.VALUES)
            if length == self.column_items():
                self.match(tokens.TokenType.SEMICOLON)
                self.match(tokens.TokenType.END)
            else:
                self.abort("Number of columns doesn't match number of values.")
            db_operations.insert('table_name', 'columns', 'values')
        else:
            self.abort("Incorrect syntax. Try again.")

    def column_items(self):
        # eventually this should check that column names are valid against the table
        # could return length of self for insert statements to check against values
        print("COLUMN ITEMS")
        self.match(tokens.TokenType.OPEN_PARENTHESIS)
        self.match(tokens.TokenType.IDENTIFIER)
        col_count = 1
        while self.check_token(tokens.TokenType.COMMA):
            self.next_token()
            self.match(tokens.TokenType.IDENTIFIER)
            col_count += 1
        self.match(tokens.TokenType.CLOSE_PARENTHESIS)
        return col_count

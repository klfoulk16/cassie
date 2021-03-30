from config import TokenType

class cassParser:
    def __init__(self, lexer):
        self.lexer = lexer

        self.current_token = None
        self.peek_token = None
        self.next_token()
        print("first next")
        self.next_token()
        print("second next")

    def check_token(self, kind):
        return kind == self.current_token.kind

    def check_peek(self, kind):
        return kind == self.peek_token.kind

    def match(self, kind):
        if not self.check_token(kind):
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
        while not self.check_token(TokenType.END):
            self.statement()

    # One of the following statements...
    def statement(self):
        # Check the first token to see what kind of statement this is.
        
        # "INSERT"
        if self.check_token(TokenType.INSERT):
            print("STATEMENT-INSERT")
            self.next_token()
            self.match(TokenType.INTO)
            self.match(TokenType.IDENTIFIER)    # do I need to specify what type of identifier?
            length = self.column_items()
            self.match(TokenType.VALUES)
            if length == self.column_items():
                self.match(TokenType.SEMICOLON)
            else:
                self.abort("Number of columns doesn't match number of values.")


    def column_items(self):
        # eventually this should check that column names are valid against the table
        # could return length of self for insert statements to check against values
        print("COLUMN ITEMS")
        self.match(TokenType.OPEN_PARENTHESIS)
        self.match(TokenType.IDENTIFIER)
        col_count = 1
        while self.check_token(TokenType.COMMA):
            self.match(TokenType.IDENTIFIER)
            col_count += 1
        self.match(TokenType.CLOSE_PARENTHESIS)
        return col_count
import sys
import re
import babyCass.cassQL.tokens as tokens


class cassLexer():
    def __init__(self, line):
        self.segments = self.seperate_line(line)
        self.current_segment = ''
        self.current_position = -1
        self.next_segment()

    def seperate_line(self, line):
        """Split line into words and characters such as ',' '(' ')'"""
        segments = []
        words = line.split()
        for word in words:
            word_split = re.split(r"(\W)", word)
            for split in word_split:
                if split != '':
                    segments.append(split)
        return segments
    
    def next_segment(self):
        self.current_position += 1
        if self.current_position >= len(self.segments):
            self.current_segment = None
        else:
            self.current_segment = self.segments[self.current_position]

    def peek(self):
        if self.current_position + 1 >= len(self.segments):
            return None
        return self.segments[self.current_position + 1]

    def get_token(self):
        identifier_pattern = re.compile(r"\w+")
        # print(f"Current segment/peek token: {self.current_segment}")
        if self.current_segment is None:
            token = tokens.Token("END", tokens.TokenType.END)
        elif self.current_segment == 'INSERT':
            token = tokens.Token("INSERT", tokens.TokenType.INSERT)
        elif self.current_segment == 'INTO':
            token = tokens.Token("INTO", tokens.TokenType.INTO)
        elif self.current_segment == 'VALUES':
            token = tokens.Token("VALUES", tokens.TokenType.VALUES)
        elif self.current_segment == 'SELECT':
            token = tokens.Token("SELECT", tokens.TokenType.SELECT)
        elif self.current_segment == 'FROM':
            token = tokens.Token("FROM", tokens.TokenType.FROM)
        elif self.current_segment == ';':
            token = tokens.Token(";", tokens.TokenType.SEMICOLON)
        elif self.current_segment == '(':
            token = tokens.Token("(", tokens.TokenType.OPEN_PARENTHESIS)
        elif self.current_segment == ')':
            token = tokens.Token(")", tokens.TokenType.CLOSE_PARENTHESIS)
        elif self.current_segment == ',':
            token = tokens.Token(",", tokens.TokenType.COMMA)
        elif self.current_segment == '*':
            token = tokens.Token("*", tokens.TokenType.STAR)
        elif self.current_segment.isnumeric():
            token = tokens.Token(self.current_segment, tokens.TokenType.NUMBER)
        elif identifier_pattern.match(self.current_segment):
            token = tokens.Token(self.current_segment, tokens.TokenType.IDENTIFIER)
        else:
            # unknown token!!!
            self.abort(f"Unknown token: {self.current_segment}")
        self.next_segment()
        return token
    
    def abort(self, message):
        sys.exit(f"Lexing error: {message}")
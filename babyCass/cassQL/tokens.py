import enum

# Token contains the original text and the type of token.
class Token:
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText   # The token's actual text. Used for identifiers, strings, and numbers.
        self.kind = tokenKind   # The TokenType that this token is classified as.


# TokenType is our enum for all the types of tokens.
class TokenType(enum.Enum):
    END = -1
    # Items.
    IDENTIFIER = 1
    NUMBER = 2
    # Keywords.
    INSERT = 101
    INTO = 102
    VALUES = 103
    SELECT = 104
    FROM = 105
    # Operators.
    # Other Characters.
    SEMICOLON = 301
    OPEN_PARENTHESIS = 302
    CLOSE_PARENTHESIS = 303
    COMMA = 304
    STAR = 305
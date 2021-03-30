import pytest
from cassiequill.lexer import cassLexer
from cassiequill.tokens import TokenType


class TestLexer:
    @pytest.fixture
    def line(self):
        return "INSERT INTO table_name (col1, col2, col3) VALUES (val1, val2, val3);"

    @pytest.fixture
    def lexer(self, line):
        return cassLexer(line)

    def test_init(self, line):
        """test that all properties are properly initialized"""
        lexer = cassLexer(line)
        assert lexer.segments == lexer.seperate_line(line)
        assert lexer.current_position == 0
        assert lexer.current_segment == lexer.segments[lexer.current_position]

    @pytest.mark.parametrize('line, segments', [
        # ("INSERT INTO table_name (col1, col2, col3) VALUES (val1, val2, val3);",
        #  ['INSERT', 'INTO', 'table_name', '(', 'col1',
        #   ',', 'col2', ',', 'col3', ')', 'VALUES', '(',
        #   'val1', ',', 'val2', ',', 'val3', ')', ';']),
        ("INSERT", ["INSERT", ])
    ])
    def test_seperate_line(self, line, segments):
        """Make sure seperate line function working - lexer.segments stores the result of said function"""
        assert cassLexer(line).segments == segments

    def test_next_segment_first(self, lexer):
        """Make sure next_segment returns next segment"""
        assert len(lexer.segments) == 19
        assert lexer.current_position == 0
        assert lexer.current_segment == lexer.segments[lexer.current_position]

        lexer.next_segment()

        assert lexer.current_position == 1
        assert lexer.current_segment == lexer.segments[lexer.current_position]
    
    def test_next_segment_last(self, lexer):
        """Make sure next_segment returns None when line is over"""
        assert len(lexer.segments) == 19
        lexer.current_position = 18
        lexer.current_segment = lexer.segments[lexer.current_position]
        
        lexer.next_segment()

        assert lexer.current_position == 19
        assert lexer.current_segment is None

    def test_peek(self, lexer):
        """Make sure peek returns returns next segment"""
        assert lexer.current_position == 0
        assert lexer.peek() == lexer.segments[1]

    def test_peek_none(self, lexer):
        """Make sure peek returns None when the current_segment is the last"""
        assert len(lexer.segments) == 19
        lexer.current_position = 18
        assert lexer.peek() is None

    def test_get_token_identifier(self):
        lexer = cassLexer('table_name')
        token = lexer.get_token()
        assert token.text == 'table_name'
        assert token.kind is TokenType.IDENTIFIER

    def test_get_token_NUMBER(self):
        lexer = cassLexer('9')
        token = lexer.get_token()
        assert token.text == '9'
        assert token.kind is TokenType.NUMBER

    def test_get_token_insert(self):
        lexer = cassLexer('INSERT')
        token = lexer.get_token()
        assert token.text == 'INSERT'
        assert token.kind is TokenType.INSERT

    def test_get_token_INTO(self):
        lexer = cassLexer('INTO')
        token = lexer.get_token()
        assert token.text == 'INTO'
        assert token.kind is TokenType.INTO
    
    def test_get_token_VALUES(self):
        lexer = cassLexer('VALUES')
        token = lexer.get_token()
        assert token.text == 'VALUES'
        assert token.kind is TokenType.VALUES
    
    def test_get_token_SEMICOLON(self):
        lexer = cassLexer(';')
        token = lexer.get_token()
        assert token.text == ';'
        assert token.kind is TokenType.SEMICOLON

    def test_get_token_OPEN_PARENTHESIS(self):
        lexer = cassLexer('(')
        token = lexer.get_token()
        assert token.text == '('
        assert token.kind is TokenType.OPEN_PARENTHESIS

    def test_get_token_CLOSE_PARENTHESIS(self):
        lexer = cassLexer(')')
        token = lexer.get_token()
        assert token.text == ')'
        assert token.kind is TokenType.CLOSE_PARENTHESIS

    def test_get_token_COMMA(self):
        lexer = cassLexer(',')
        token = lexer.get_token()
        assert token.text == ','
        assert token.kind is TokenType.COMMA

    def test_get_token_abort(self):
        token = '%'
        lexer = cassLexer(token)
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            lexer.get_token()
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == f'Lexing error: Unknown token: {token}'
    
    def test_abort(self, lexer):
        message = "Test message"
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            lexer.abort(message)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == f"Lexing error: {message}"


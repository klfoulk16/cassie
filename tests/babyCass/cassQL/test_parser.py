import pytest
from babyCass.cassQL.lexer import cassLexer
from babyCass.cassQL.parser import cassParser
import babyCass.cassQL.tokens as tokens


class TestParser:
    @pytest.fixture
    def line(self):
        return "INSERT INTO table_name (col1, col2, col3) VALUES (val1, val2, val3);"

    @pytest.fixture
    def lexer(self, line):
        return cassLexer(line)
    
    @pytest.fixture
    def parser(self, lexer):
        return cassParser(lexer)
    
    def test_init(self, lexer):
        """test that all properties are properly initialized"""
        parser = cassParser(lexer)
        assert parser.lexer == lexer
        assert parser.current_token.text == "INSERT"
        assert parser.current_token.kind == tokens.TokenType.INSERT
        assert parser.peek_token.text == "INTO"
        assert parser.peek_token.kind == tokens.TokenType.INTO

    def test_check_token(self, parser):
        assert parser.current_token.kind == tokens.TokenType.INSERT
        assert parser.check_token(tokens.TokenType.INSERT) is True
        assert parser.check_token(tokens.TokenType.INTO) is False
    
    def test_check_peek(self, parser):
        assert parser.peek_token.kind == tokens.TokenType.INTO
        assert parser.check_peek(tokens.TokenType.INTO) is True
        assert parser.check_peek(tokens.TokenType.SEMICOLON) is False

    def test_match_no_abort(self, parser, mocker):
        assert parser.current_token.kind == tokens.TokenType.INSERT        
        parser.abort = mocker.patch("babyCass.cassQL.parser.cassParser.abort")
        parser.next_token = mocker.patch("babyCass.cassQL.parser.cassParser.next_token")
        
        parser.match(tokens.TokenType.INSERT)

        parser.next_token.assert_called()
        parser.abort.assert_not_called()

    def test_match_abort(self, parser, mocker):
        assert parser.current_token.kind == tokens.TokenType.INSERT  

        parser.next_token = mocker.patch("babyCass.cassQL.parser.cassParser.next_token")
        
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            parser.match(tokens.TokenType.INTO)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == f"Error. Expected {tokens.TokenType.INTO.name}, got {parser.current_token.kind.name}"
    
        parser.next_token.assert_not_called()

    def next_token_start(self, parser):
        assert parser.current_token.kind == tokens.TokenType.INSERT
        assert parser.peek_token.kind == tokens.TokenType.INTO

        parser.next_token()

        assert parser.current_token.kind == tokens.TokenType.INTO
        assert parser.peek_token.kind == tokens.TokenType.IDENTIFIER

    def next_token_end(self):
        # shall I have a TokenType.END instead of None?
        parser = cassParser(cassLexer("INSERT INTO"))

        assert parser.current_token.kind == tokens.TokenType.INSERT
        assert parser.peek_token.kind == tokens.TokenType.INTO

        parser.next_token()

        assert parser.current_token.kind == tokens.TokenType.INTO
        assert parser.peek_token is None

        parser.next_token()

        assert parser.current_token is None
        assert parser.peek_token is None

    def test_abort(self, parser):            
        message = "Test message"
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            parser.abort(message)
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == f"Error. {message}"

    @pytest.mark.timeout(1)
    def test_program(self, parser, mocker):
        """Assert that program function ends"""
        parser.program()

    def test_statement_incorrect(self):
        """Assert that incorrect statement is handled properly"""
        parser = cassParser(cassLexer("INSERT INTO random column;"))
        
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            parser.program()
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == "Error. Expected OPEN_PARENTHESIS, got IDENTIFIER"
    
    def test_statement_insert(self, parser, mocker):
        """Assert that correct function is run when insert statement is correct"""
        insert = mocker.patch("babyCass.cass.db_operations.insert")
        parser.statement()
        insert.assert_called()
    
    @pytest.mark.parametrize('line, col_count', [
        ("(col1, col2, col3)", 3),
        ("(val1, val2, val3)", 3),
        ("(val1, val2, val3, val4)", 4),
        ("(val1)", 1)
    ])
    def test_column_items_correct(self, line, col_count):
        parser = cassParser(cassLexer(line))
        assert parser.column_items() == col_count

    @pytest.mark.parametrize('line', [
        ("(val1, val2,)"),
        ("weeee"),
        ("(val1, val2,")
    ])
    def test_column_items_incorrect(self, line):
        parser = cassParser(cassLexer(line))
        with pytest.raises(SystemExit) as pytest_wrapped_e:
            parser.column_items()
            assert pytest_wrapped_e.type == SystemExit


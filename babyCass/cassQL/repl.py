"""A simple SQL-like REPL."""
# help: https://bip.weizmann.ac.il/course/python/PyMOTW/PyMOTW/docs/cmd/index.html#:~:text=The%20cmd%20module%20contains%20one,line%20editing%2C%20and%20command%20completion.

import cmd
from babyCass.cassQL.parser import cassParser
from babyCass.cassQL.lexer import cassLexer


class cassREPL(cmd.Cmd):
    """
    simple cassQL REPL
    """
    prompt = "cassQL > "
    intro = "cassQL version 0.0.1 2021\nEnter '?' for usage hints."

    def default(self, line):
        """"A SQL parser"""
        self.lexer = cassLexer(line)
        self.parser = cassParser(self.lexer)
        data = self.parser.program()
        if data:
            for entry in data:
                print(entry)

    def do_greet(self, line):
        print('hello,', line)

    def do_EOF(self, line):
        print('Type "bye" to exit.')
        # return True

    def do_bye(self, line):
        return True
"""A simple SQL-like REPL."""
# help: https://bip.weizmann.ac.il/course/python/PyMOTW/PyMOTW/docs/cmd/index.html#:~:text=The%20cmd%20module%20contains%20one,line%20editing%2C%20and%20command%20completion.

import cmd

class cassREPL(cmd.Cmd):
    """
    simple cassiequill REPL
    """
    prompt = "cass > "
    intro = "cassiequill version 0.0.1 2021\nEnter '?' for usage hints."

    def default(self, line):
        """"A SQL parser"""
        cassCompiler(line)

    def do_greet(self, line):
        print('hello,', line)

    def do_EOF(self, line):
        print('Type "bye" to exit.')
        # return True

    def do_bye(self, line):
        return True


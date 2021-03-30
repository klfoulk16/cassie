class cassCompiler:
    """
    simple cassiequill compiler
    """

    def __init__(self, line):
        self.tokens = cassLexer(line)
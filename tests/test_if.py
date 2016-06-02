from context import lift
from context import tube

from lift import Parser
from lift.Generator import Generator
from tube import Machine
from tube import Processor

import sys
import StringIO


def test_read(capsys):
    with open('demo/if-else.js', 'r') as f:
        mock_stdin = StringIO.StringIO("20\n")
        sys.stdin = mock_stdin

        reload(Parser)
        reload(Generator)
        reload(Machine)
        reload(Processor)
        Parser.build('Program')
        ast = Parser.yacc.parse(f.read())
        code = Generator.generate(ast)
        Machine.load(code.splitlines(True))
        Machine.run()
        out, err = capsys.readouterr()
        assert out == "'Guess how old I am?'\nPlease enter an integer.\n'Hey! You got it.'\n"

        sys.stdin = sys.__stdin__
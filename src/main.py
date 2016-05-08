import Parser

if __name__ == '__main__':
    Parser.build("Program")
    with open("../tests/statement.js") as file:
        ast = Parser.yacc.parse(file.read())
        Parser.printAST(ast)

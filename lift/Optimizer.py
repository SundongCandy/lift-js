"""
Optimizer module for Lift JS.
"""


def fold_constant(ast):
    # TODO
    return ast


def eliminate_unreachable(ast):
    # TODO
    return ast


def optimize(ast):
    ret = fold_constant(ast)
    ret = eliminate_unreachable(ret)
    return ret


def optimize_string_literal(string):
    return


def optimize_literal(ast):
    assert ast[0] == 'Literal'
    if type(ast[1]) == int:
        return
    elif type(ast[1]) == str:
        return
    elif type(ast[1]) == bool:
        return


def optimize_identifier(ast):
    assert ast[0] == 'Identifier'
    return


def optimize_function_body(ast):
    assert ast[0] == 'FunctionBody'
    if ast[2] != '}':
        optimize_statement_list(ast[2])


def optimize_function_expression(ast):
    assert ast[0] == 'FunctionExpression'
    if ast[2] != '(':
        optimize_identifier(ast[2])
    if ast[-3] != '(':
        # The function has arguments
        for node in ast[-3]:
            if type(node) == list:
                optimize_identifier(node)
    optimize_function_body(ast[-1])
    return


def optimize_property_name(ast):
    assert ast[0] == 'PropertyName', str(ast)
    if type(ast[1]) == list:  # identifier
        return optimize_identifier(ast[1])
    elif type(ast[1]) == str:  # string literal
        return optimize_string_literal(ast[1])
        # TODO: more type of property


def optimize_object_literal(ast):
    assert ast[0] == 'ObjectLiteral', str(ast)
    for node in ast[2]:
        if type(node) != list:
            continue
        optimize_property_name(node[1])
        optimize_assignment_expression_no_in(node[3])
    return


def optimize_primary_expression(ast):
    assert ast[0] == 'PrimaryExpression'
    if ast[1] == 'this':
        return
    elif ast[1][0] == 'Literal':
        return optimize_literal(ast[1])
    elif ast[1][0] == 'Identifier':
        return optimize_identifier(ast[1])
    elif ast[1][0] == 'FunctionExpression':
        return optimize_function_expression(ast[1])
    elif ast[1][0] == 'ObjectLiteral':
        return optimize_object_literal(ast[1])
    # TODO
    pass


def optimize_allocation_expression(ast):
    assert ast[0] == 'AllocationExpression'
    optimize_member_expression(ast[2])  # it should be a function

    if ast[3][-2] != '(':  # there are some arguments
        for node in ast[3][-2]:
            if type(node) == list:
                optimize_assignment_expression_no_in(node)
    return


def optimize_member_expression_part(ast):
    assert ast[0] == 'MemberExpressionPart'
    if ast[1] == '[':
        return optimize_expression_no_in(ast[2])
    elif ast[1] == '.':
        return optimize_identifier(ast[2])


def optimize_member_expression(ast):
    assert ast[0] == 'MemberExpression'
    if ast[1][0] == 'PrimaryExpression':
        return optimize_primary_expression(ast[1])
    elif ast[1][0] == 'MemberExpression':
        optimize_member_expression(ast[1])
        optimize_member_expression_part(ast[2])
        # TODO check whether need to create a field
        return
    elif ast[1][0] == 'AllocationExpression':
        return optimize_allocation_expression(ast[1])


def optimize_call_expression(ast, this=None):
    assert ast[0] == 'CallExpression'
    if ast[2][0] == 'Arguments':
        if ast[1][0] == 'MemberExpression':
            optimize_member_expression(ast[1])
        elif ast[1][0] == 'CallExpression':
            optimize_call_expression(ast[1])
        if ast[2][-2] != '(':  # there are some arguments
            for node in ast[2][-2]:
                if type(node) == list:
                    optimize_assignment_expression_no_in(node)
        return
        # TODO


def optimize_left_hand_side_expression(ast):
    assert ast[0] == 'LeftHandSideExpression'
    if ast[1][0] == 'MemberExpression':
        return optimize_member_expression(ast[1])
    elif ast[1][0] == 'CallExpression':
        return optimize_call_expression(ast[1])
    # TODO
    pass


def optimize_assignment_expression_no_in(ast):
    assert ast[0] == 'AssignmentExpressionNoIn'
    if len(ast) == 2:
        if ast[1][0] == 'LeftHandSideExpression':
            return optimize_left_hand_side_expression(ast[1])
        elif ast[1][0] == 'CallExpression':
            return optimize_call_expression(ast[1])
        elif ast[1][0] == 'MemberExpression':
            return optimize_member_expression(ast[1])
    elif len(ast) == 3:
        if ast[1][0] == 'AssignmentExpressionNoIn':
            raise Exception('Postfix operator is not supported yet.')
        elif ast[1] == '++':
            optimize_assignment_expression_no_in(ast[2])
            return
        elif ast[1] == '--':
            optimize_assignment_expression_no_in(ast[2])
            return
        elif ast[1] == 'typeof':
            optimize_assignment_expression_no_in(ast[2])
            return
        elif ast[1] == '+':
            return optimize_assignment_expression_no_in(ast[2])
        elif ast[1] == '-':
            optimize_assignment_expression_no_in(ast[2])
            return
        elif ast[1] == '~':
            optimize_assignment_expression_no_in(ast[2])
            return
        elif ast[1] == '!':
            optimize_assignment_expression_no_in(ast[2])
            return
    elif len(ast) == 4:
        if ast[2] in ['=', '*=', '/=', '%=', '+=', '-=', '<<=', '>>=', '>>>=', '&=',
                      '^=', '|=']:
            optimize_left_hand_side_expression(ast[1])
        elif ast[2] in ['||', '&&', '|', '&', '^', '==', '!=', '===', '!==',
                        '<', '>', '<=', '>=', '<<', '>>', '>>>', '+', '-', '*',
                        '/']:
            optimize_assignment_expression_no_in(ast[1])
        optimize_assignment_expression_no_in(ast[3])
        if ast[2] == '+':
            return
        elif ast[2] == '-':
            return
        elif ast[2] == '*':
            return
        elif ast[2] == '/':
            return
        elif ast[2] == '=':
            return
        elif ast[2] == '*=':
            return
        elif ast[2] == '/=':
            return
        elif ast[2] == '%=':
            return
        elif ast[2] == '+=':
            return
        elif ast[2] == '-=':
            return
        elif ast[2] == '<<=':
            return
        elif ast[2] == '>>=':
            return
        elif ast[2] == '>>>=':
            return
        elif ast[2] == '&=':
            return
        elif ast[2] == '^=':
            return
        elif ast[2] == '|=':
            return
        elif ast[2] == '||':
            return
        elif ast[2] == '&&':
            return
        elif ast[2] == '|':
            return
        elif ast[2] == '&':
            return
        elif ast[2] == '^':
            return
        elif ast[2] == '==' or ast[2] == '===':
            return
        elif ast[2] == '!=' or ast[2] == '!==':
            return
        elif ast[2] == '<':
            return
        elif ast[2] == '>':
            return
        elif ast[2] == '<=':
            return
        elif ast[2] == '>=':
            return
        elif ast[2] == '<<':
            return
        elif ast[2] == '>>':
            return
        elif ast[2] == '>>>':
            return


def optimize_expression_no_in(ast):
    assert ast[0] == 'ExpressionNoIn'
    if ast[1][0] == 'ExpressionNoIn':
        return optimize_expression_no_in(ast[1])
    elif ast[1][0] == 'AssignmentExpressionNoIn':
        return optimize_assignment_expression_no_in(ast[1])


def optimize_do_statement(ast):
    assert ast[0] == 'DoStatement'
    optimize_statement(ast[2])
    optimize_expression_no_in(ast[5])


def optimize_while_statement(ast):
    assert ast[0] == 'WhileStatement'
    optimize_expression_no_in(ast[3])


def optimize_origin_for_statement(ast):
    assert ast[0] == 'OriginForStatement'
    optimize_expression_no_in(ast[3])
    optimize_expression_no_in(ast[5])
    optimize_statement(ast[9])
    optimize_expression_no_in(ast[7])


def optimize_for_each_statement(ast):
    assert ast[0] == 'ForEachStatement'


def optimize_return_statement(ast):
    assert ast[0] == 'ReturnStatement'
    if len(ast) >= 3 and ast[2] != ';':  # return some expression
        optimize_expression_no_in(ast[2])


def optimize_iteration_statement(ast):
    assert ast[0] == 'IterationStatement'
    optimizers = {
        'DoStatement': optimize_do_statement,
        'WhileStatement': optimize_while_statement,
        'OriginForStatement': optimize_origin_for_statement,
        'ForEachStatement': optimize_for_each_statement
    }
    if ast[1][0] in optimizers:
        optimizers[ast[1][0]](ast[1])


def optimize_if_statement(ast):
    assert ast[0] == 'IfStatement'
    optimize_expression_no_in(ast[3])
    if ast[-2] == 'else':  # it has 'else' clause
        optimize_statement(ast[5])
        optimize_statement(ast[7])
    else:  # It has no 'else' clause
        optimize_statement(ast[5])


def optimize_expression_no_in_statement(ast):
    assert ast[0] == 'ExpressionNoInStatement'
    optimize_expression_no_in(ast[1])


def optimize_variable_statement(ast):
    assert ast[0] == 'VariableStatement'
    optimize_identifier(ast[2])
    if len(ast) > 4:
        optimize_assignment_expression_no_in(ast[4])


def optimize_block(ast):
    assert ast[0] == 'Block'
    if len(ast[1:]) == 3:
        optimize_statement_list(ast[2])


def optimize_statement(ast):
    assert ast[0] == 'Statement'
    optimizers = {
        'Block': optimize_block,
        'VariableStatement': optimize_variable_statement,
        'ExpressionNoInStatement': optimize_expression_no_in_statement,
        'IfStatement': optimize_if_statement,
        'IterationStatement': optimize_iteration_statement,
        'ReturnStatement': optimize_return_statement
    }
    if ast[1][0] in optimizers:
        optimizers[ast[1][0]](ast[1])


def optimize_statement_list(ast):
    assert ast[0] == 'StatementList'
    for node in ast[1:]:
        optimize_statement(node)


def optimize_program(ast):
    assert ast[0] == 'Program'
    optimize_statement_list(ast[1])



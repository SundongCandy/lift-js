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
    return ast

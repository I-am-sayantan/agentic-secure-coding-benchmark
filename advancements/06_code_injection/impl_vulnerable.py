"""Expression calculator -- VULNERABLE (CWE-94 Code Injection).

Evaluates the expression with ``eval``, which runs *any* Python, not just
arithmetic. Input like ``__import__('os').system(...)`` is executed.
"""


def calculate(expression):
    return eval(expression)

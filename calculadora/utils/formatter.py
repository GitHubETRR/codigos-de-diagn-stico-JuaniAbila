"""
Utilidades para formateo de expresiones matemáticas
"""

def to_superscript(n):
    """Convierte un número a superíndice Unicode"""
    superscripts = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
    return str(n).translate(superscripts)


def format_expression(expr):
    """Formatea una expresión para mostrar de forma legible"""
    # Reemplazar operadores
    expr = expr.replace('*', '×')
    expr = expr.replace('**', '^')
    
    return expr


def format_coefficient(coef):
    """Formatea un coeficiente numérico"""
    if coef == int(coef):
        return str(int(coef))
    else:
        return f"{coef:.2f}"

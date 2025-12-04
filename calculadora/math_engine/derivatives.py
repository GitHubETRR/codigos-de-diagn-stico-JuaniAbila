"""
Motor de derivadas simbólicas
Implementa reglas de derivación para diferentes tipos de funciones
"""

import re
import math
from typing import Dict, Tuple, Optional


class DerivativeEngine:
    """Motor de derivadas que implementa reglas de derivación"""
    
    def __init__(self):
        self.variable = 'x'
    
    def derive(self, expression: str) -> str:
        """
        Deriva una expresión matemática
        
        Args:
            expression: Expresión a derivar (ej: "x^2 + sin(x)")
            
        Returns:
            Derivada de la expresión
        """
        expression = expression.strip().replace(' ', '')
        
        try:
            result = self._derive_expression(expression)
            return self._simplify(result)
        except Exception as e:
            raise ValueError(f"No se pudo derivar la expresión: {str(e)}")
    
    def _derive_expression(self, expr: str) -> str:
        """Deriva una expresión completa"""
        # Manejar suma y resta
        if '+' in expr or '-' in expr:
            return self._derive_sum(expr)
        
        # Manejar producto
        if '*' in expr and not self._is_inside_function(expr, '*'):
            return self._derive_product(expr)
        
        # Manejar cociente
        if '/' in expr and not self._is_inside_function(expr, '/'):
            return self._derive_quotient(expr)
        
        # Manejar término simple
        return self._derive_term(expr)
    
    def _derive_sum(self, expr: str) -> str:
        """Deriva una suma/resta (regla de la suma)"""
        terms = self._split_terms(expr)
        derived_terms = [self._derive_expression(term) for term in terms]
        return ' + '.join(derived_terms)
    
    def _derive_product(self, expr: str) -> str:
        """Deriva un producto (regla del producto): (f*g)' = f'*g + f*g'"""
        parts = expr.split('*', 1)
        if len(parts) != 2:
            return self._derive_term(expr)
        
        f, g = parts
        f_prime = self._derive_expression(f)
        g_prime = self._derive_expression(g)
        
        return f"({f_prime})*({g}) + ({f})*({g_prime})"
    
    def _derive_quotient(self, expr: str) -> str:
        """Deriva un cociente (regla del cociente): (f/g)' = (f'*g - f*g')/g^2"""
        parts = expr.split('/', 1)
        if len(parts) != 2:
            return self._derive_term(expr)
        
        f, g = parts
        f_prime = self._derive_expression(f)
        g_prime = self._derive_expression(g)
        
        return f"(({f_prime})*({g}) - ({f})*({g_prime}))/(({g})^2)"
    
    def _derive_term(self, term: str) -> str:
        """Deriva un término individual"""
        # Constante
        if self.variable not in term:
            return "0"
        
        # Funciones trigonométricas
        if term.startswith('sin('):
            inner = self._extract_function_arg(term, 'sin')
            inner_prime = self._derive_expression(inner)
            return f"cos({inner})*({inner_prime})"
        
        if term.startswith('cos('):
            inner = self._extract_function_arg(term, 'cos')
            inner_prime = self._derive_expression(inner)
            return f"-sin({inner})*({inner_prime})"
        
        if term.startswith('tan('):
            inner = self._extract_function_arg(term, 'tan')
            inner_prime = self._derive_expression(inner)
            return f"(1/(cos({inner})^2))*({inner_prime})"
        
        # Funciones exponenciales
        if term.startswith('exp(') or term.startswith('e^'):
            if term.startswith('exp('):
                inner = self._extract_function_arg(term, 'exp')
            else:
                inner = term[2:].strip('()')
            inner_prime = self._derive_expression(inner)
            return f"exp({inner})*({inner_prime})"
        
        # Logaritmo natural
        if term.startswith('ln('):
            inner = self._extract_function_arg(term, 'ln')
            inner_prime = self._derive_expression(inner)
            return f"(1/({inner}))*({inner_prime})"
        
        if term.startswith('log('):
            inner = self._extract_function_arg(term, 'log')
            inner_prime = self._derive_expression(inner)
            return f"(1/(({inner})*ln(10)))*({inner_prime})"
        
        # Raíz cuadrada
        if term.startswith('sqrt('):
            inner = self._extract_function_arg(term, 'sqrt')
            inner_prime = self._derive_expression(inner)
            return f"(1/(2*sqrt({inner})))*({inner_prime})"
        
        # Potencia
        if '^' in term:
            base, exponent = term.split('^', 1)
            
            # x^n (potencia simple)
            if base == self.variable and self.variable not in exponent:
                try:
                    n = float(exponent)
                    if n == 0:
                        return "0"
                    elif n == 1:
                        return "1"
                    else:
                        return f"{n}*{self.variable}^{n-1}"
                except:
                    # Exponente simbólico
                    return f"({exponent})*{self.variable}^({exponent}-1)"
            
            # f(x)^n
            elif self.variable in base and self.variable not in exponent:
                base_prime = self._derive_expression(base)
                return f"{exponent}*({base})^({exponent}-1)*({base_prime})"
            
            # a^f(x)
            elif self.variable not in base and self.variable in exponent:
                exp_prime = self._derive_expression(exponent)
                return f"({base})^({exponent})*ln({base})*({exp_prime})"
            
            # f(x)^g(x)
            else:
                # Usar logaritmos: (f^g)' = f^g * (g'*ln(f) + g*f'/f)
                f_prime = self._derive_expression(base)
                g_prime = self._derive_expression(exponent)
                return f"({base})^({exponent})*(({g_prime})*ln({base})+({exponent})*({f_prime})/({base}))"
        
        # Variable simple
        if term == self.variable:
            return "1"
        
        # Coeficiente * variable
        match = re.match(r'([+-]?\d*\.?\d*)' + self.variable, term)
        if match:
            coef = match.group(1)
            if coef in ['', '+']:
                return "1"
            elif coef == '-':
                return "-1"
            else:
                return coef
        
        return "0"
    
    def _split_terms(self, expr: str) -> list:
        """Divide una expresión en términos (respetando paréntesis)"""
        terms = []
        current_term = ""
        paren_depth = 0
        
        for i, char in enumerate(expr):
            if char == '(':
                paren_depth += 1
                current_term += char
            elif char == ')':
                paren_depth -= 1
                current_term += char
            elif char in ['+', '-'] and paren_depth == 0 and i > 0:
                terms.append(current_term)
                current_term = char if char == '-' else ""
            else:
                current_term += char
        
        if current_term:
            terms.append(current_term)
        
        return [t for t in terms if t and t not in ['+', '-']]
    
    def _extract_function_arg(self, expr: str, func_name: str) -> str:
        """Extrae el argumento de una función"""
        start = expr.index('(') + 1
        paren_count = 1
        end = start
        
        for i in range(start, len(expr)):
            if expr[i] == '(':
                paren_count += 1
            elif expr[i] == ')':
                paren_count -= 1
                if paren_count == 0:
                    end = i
                    break
        
        return expr[start:end]
    
    def _is_inside_function(self, expr: str, char: str) -> bool:
        """Verifica si un carácter está dentro de una función"""
        paren_depth = 0
        for c in expr:
            if c == '(':
                paren_depth += 1
            elif c == ')':
                paren_depth -= 1
            elif c == char and paren_depth > 0:
                return True
        return False
    
    def _simplify(self, expr: str) -> str:
        """Simplifica una expresión derivada"""
        # Simplificaciones básicas
        expr = expr.replace('+ -', '- ')
        expr = expr.replace('- -', '+ ')
        expr = expr.replace('*1 ', '')
        expr = expr.replace(' *1', '')
        expr = expr.replace('(1)*', '')
        expr = expr.replace('*(1)', '')
        expr = expr.replace(' + 0', '')
        expr = expr.replace('0 + ', '')
        expr = expr.replace(' - 0', '')
        
        # Limpiar paréntesis innecesarios en algunos casos
        expr = re.sub(r'\(([^()]+)\)\*\(([^()]+)\)', r'\1*\2', expr)
        
        return expr


def derive_polynomial(coefficients: list) -> list:
    """
    Deriva un polinomio dado por sus coeficientes
    
    Args:
        coefficients: Lista de coeficientes [c0, c1, c2, ...] donde ci es el coef de x^i
        
    Returns:
        Lista de coeficientes de la derivada
    """
    if len(coefficients) <= 1:
        return [0]
    
    derivative = []
    for i in range(1, len(coefficients)):
        derivative.append(coefficients[i] * i)
    
    return derivative

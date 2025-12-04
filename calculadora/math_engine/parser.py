"""
Parser de expresiones matemáticas
"""

import re
from typing import List, Tuple


class ExpressionParser:
    """Parser para expresiones matemáticas"""
    
    def __init__(self):
        self.variable = 'x'
    
    def parse_polynomial(self, poly_str: str) -> List[float]:
        """
        Parsea un string de polinomio y retorna coeficientes
        
        Args:
            poly_str: String del polinomio (ej: "3x^2 + 2x - 5")
            
        Returns:
            Lista de coeficientes [c0, c1, c2, ...] donde ci es el coef de x^i
        """
        try:
            poly_str = poly_str.replace(' ', '').lower()
            
            # Encontrar el grado máximo
            max_degree = 0
            matches = re.findall(r'x\^(\d+)', poly_str)
            if matches:
                max_degree = max(int(m) for m in matches)
            if 'x' in poly_str and max_degree == 0:
                max_degree = 1
            
            # Inicializar coeficientes
            coefficients = [0.0] * (max_degree + 1)
            
            # Añadir + al inicio si no hay signo
            if poly_str[0] not in ['+', '-']:
                poly_str = '+' + poly_str
            
            # Encontrar todos los términos
            terms = re.findall(r'[+-][^+-]+', poly_str)
            
            for term in terms:
                term = term.strip()
                
                # Término con x^n
                match = re.match(r'([+-]?\d*\.?\d*)x\^(\d+)', term)
                if match:
                    coef = match.group(1)
                    if coef in ['', '+']:
                        coef = 1
                    elif coef == '-':
                        coef = -1
                    else:
                        coef = float(coef)
                    degree = int(match.group(2))
                    coefficients[degree] = coef
                    continue
                
                # Término con x (grado 1)
                match = re.match(r'([+-]?\d*\.?\d*)x', term)
                if match:
                    coef = match.group(1)
                    if coef in ['', '+']:
                        coef = 1
                    elif coef == '-':
                        coef = -1
                    else:
                        coef = float(coef)
                    coefficients[1] = coef
                    continue
                
                # Término constante
                match = re.match(r'([+-]?\d+\.?\d*)', term)
                if match:
                    coef = float(match.group(1))
                    coefficients[0] = coef
            
            return coefficients
            
        except Exception as e:
            raise ValueError(f"No se pudo parsear el polinomio: {str(e)}")
    
    def validate_expression(self, expr: str) -> Tuple[bool, str]:
        """
        Valida una expresión matemática
        
        Returns:
            (es_valida, mensaje_error)
        """
        # Verificar paréntesis balanceados
        if expr.count('(') != expr.count(')'):
            return False, "Paréntesis no balanceados"
        
        # Verificar caracteres válidos
        valid_chars = set('0123456789+-*/^().xsincogtanlexpqr ')
        if not all(c in valid_chars for c in expr.lower()):
            return False, "Caracteres inválidos en la expresión"
        
        return True, ""
    
    def normalize_expression(self, expr: str) -> str:
        """Normaliza una expresión para procesamiento"""
        expr = expr.replace(' ', '')
        expr = expr.replace('**', '^')
        return expr

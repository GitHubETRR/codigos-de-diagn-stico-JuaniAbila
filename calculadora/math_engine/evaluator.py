"""
Evaluador de expresiones matemáticas
"""

import math
import numpy as np
from typing import Union, List


class ExpressionEvaluator:
    """Evaluador de expresiones matemáticas"""
    
    def __init__(self):
        self.angle_mode = 'deg'  # 'deg' o 'rad'
    
    def evaluate(self, expression: str, x_value: float = None) -> float:
        """
        Evalúa una expresión matemática
        
        Args:
            expression: Expresión a evaluar
            x_value: Valor de x (si la expresión contiene x)
            
        Returns:
            Resultado de la evaluación
        """
        try:
            # Preparar expresión
            expr = expression.replace('^', '**')
            expr = expr.replace('×', '*')
            
            # Reemplazar funciones
            expr = self._replace_functions(expr)
            
            # Reemplazar x si se proporciona
            if x_value is not None:
                expr = expr.replace('x', str(x_value))
            
            # Evaluar
            result = eval(expr, {"__builtins__": {}}, {
                "math": math,
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "asin": math.asin,
                "acos": math.acos,
                "atan": math.atan,
                "sqrt": math.sqrt,
                "exp": math.exp,
                "log": math.log10,
                "ln": math.log,
                "pi": math.pi,
                "e": math.e
            })
            
            return result
            
        except Exception as e:
            raise ValueError(f"Error al evaluar la expresión: {str(e)}")
    
    def evaluate_polynomial(self, coefficients: List[float], x_value: float) -> float:
        """
        Evalúa un polinomio en un punto
        
        Args:
            coefficients: Coeficientes del polinomio [c0, c1, c2, ...]
            x_value: Valor de x
            
        Returns:
            Valor del polinomio en x
        """
        result = 0
        for i, coef in enumerate(coefficients):
            result += coef * (x_value ** i)
        return result
    
    def evaluate_range(self, expression: str, x_min: float, x_max: float, 
                      num_points: int = 500) -> tuple:
        """
        Evalúa una expresión en un rango de valores
        
        Returns:
            (x_values, y_values)
        """
        x_values = np.linspace(x_min, x_max, num_points)
        y_values = []
        
        for x in x_values:
            try:
                y = self.evaluate(expression, x)
                y_values.append(y)
            except:
                y_values.append(np.nan)
        
        return x_values, np.array(y_values)
    
    def _replace_functions(self, expr: str) -> str:
        """Reemplaza nombres de funciones para evaluación"""
        # Funciones trigonométricas con conversión de ángulos
        if self.angle_mode == 'deg':
            expr = expr.replace('sin(', 'math.sin(math.radians(')
            expr = expr.replace('cos(', 'math.cos(math.radians(')
            expr = expr.replace('tan(', 'math.tan(math.radians(')
            # Añadir paréntesis de cierre
            expr = expr.replace('radians(', 'radians(') + ')' * expr.count('radians(')
        
        return expr

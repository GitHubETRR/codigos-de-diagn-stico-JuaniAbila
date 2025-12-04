"""
Calculadora Científica Modular
Punto de entrada de la aplicación
"""

import tkinter as tk
from ui.calculator_window import ScientificCalculator


def main():
    """Función principal"""
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()

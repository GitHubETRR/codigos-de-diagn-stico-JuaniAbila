"""
Ventana principal de la calculadora científica
"""

import tkinter as tk
from tkinter import messagebox
import math
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.widgets import RoundedButton, FunctionInputPanel
from ui.graph_window import GraphWindow
from math_engine import DerivativeEngine, ExpressionParser, ExpressionEvaluator
from utils import COLORS, PI, E, format_expression
from utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT


class ScientificCalculator:
    """Calculadora Científica con diseño modular"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Científica Casio fx-991")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.configure(bg=COLORS['bg_primary'])
        self.root.resizable(False, False)
        
        # Componentes del motor matemático
        self.derivative_engine = DerivativeEngine()
        self.parser = ExpressionParser()
        self.evaluator = ExpressionEvaluator()
        
        # Variables
        self.current_input = ""
        self.result_shown = False
        self.mode = tk.StringVar(value="basic")
        self.angle_mode = tk.StringVar(value="deg")
        self.memory = 0
        self.graph_window = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        main_container = tk.Frame(self.root, bg=COLORS['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.create_header(main_container)
        self.create_display(main_container)
        self.create_mode_selector(main_container)
        
        self.keyboard_frame = tk.Frame(main_container, bg=COLORS['bg_primary'])
        self.keyboard_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.update_keyboard()
    
    def create_header(self, parent):
        """Crea el header"""
        header = tk.Frame(parent, bg=COLORS['bg_primary'])
        header.pack(fill=tk.X, pady=(0, 15))
        
        title_frame = tk.Frame(header, bg=COLORS['accent_blue'], height=50)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title = tk.Label(
            title_frame,
            text="🧮 CASIO fx-991",
            font=("Segoe UI", 20, "bold"),
            bg=COLORS['accent_blue'],
            fg=COLORS['text_primary']
        )
        title.pack(expand=True)
    
    def create_display(self, parent):
        """Crea el display LCD"""
        display_container = tk.Frame(parent, bg=COLORS['bg_secondary'], 
                                     relief=tk.RAISED, bd=3)
        display_container.pack(fill=tk.X, pady=(0, 15))
        
        display_frame = tk.Frame(display_container, bg=COLORS['display_bg'])
        display_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Indicadores
        indicators = tk.Frame(display_frame, bg=COLORS['display_bg'])
        indicators.pack(fill=tk.X, pady=(5, 0))
        
        self.mode_indicator = tk.Label(
            indicators,
            text="COMP",
            font=("Consolas", 9, "bold"),
            bg=COLORS['display_bg'],
            fg=COLORS['accent_green']
        )
        self.mode_indicator.pack(side=tk.LEFT, padx=10)
        
        self.angle_indicator = tk.Label(
            indicators,
            text="DEG",
            font=("Consolas", 9, "bold"),
            bg=COLORS['display_bg'],
            fg=COLORS['accent_orange']
        )
        self.angle_indicator.pack(side=tk.LEFT)
        
        # Display secundario
        self.history_display = tk.Label(
            display_frame,
            text="",
            font=("Consolas", 11),
            bg=COLORS['display_bg'],
            fg=COLORS['text_secondary'],
            anchor=tk.E,
            padx=15,
            pady=3
        )
        self.history_display.pack(fill=tk.X)
        
        # Display principal
        self.main_display = tk.Label(
            display_frame,
            text="0",
            font=("Consolas", 28, "bold"),
            bg=COLORS['display_bg'],
            fg=COLORS['text_primary'],
            anchor=tk.E,
            padx=15,
            pady=12
        )
        self.main_display.pack(fill=tk.X)
    
    def create_mode_selector(self, parent):
        """Crea el selector de modo"""
        mode_frame = tk.Frame(parent, bg=COLORS['bg_primary'])
        mode_frame.pack(fill=tk.X, pady=(0, 10))
        
        modes = [
            ("Básica", "basic", COLORS['accent_green']),
            ("Científica", "scientific", COLORS['accent_blue']),
            ("Funciones", "functions", COLORS['accent_purple'])
        ]
        
        for text, value, color in modes:
            btn_frame = tk.Frame(mode_frame, bg=COLORS['bg_primary'])
            btn_frame.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
            
            btn = RoundedButton(
                btn_frame,
                text=text,
                command=lambda v=value: self.change_mode(v),
                bg_color=color if self.mode.get() == value else COLORS['bg_tertiary'],
                hover_color=color,
                font=("Segoe UI", 11, "bold"),
                width=180,
                height=40
            )
            btn.pack(fill=tk.X)
    
    def change_mode(self, mode):
        """Cambia el modo de la calculadora"""
        self.mode.set(mode)
        self.update_keyboard()
        # Recrear selector para actualizar colores
        for widget in self.root.winfo_children()[0].winfo_children():
            if isinstance(widget, tk.Frame) and widget.winfo_children():
                # Buscar el frame del selector de modo
                try:
                    first_child = widget.winfo_children()[0]
                    if isinstance(first_child, tk.Frame):
                        widget.destroy()
                        self.create_mode_selector(self.root.winfo_children()[0])
                        break
                except:
                    pass
    
    def update_keyboard(self):
        """Actualiza el teclado según el modo"""
        for widget in self.keyboard_frame.winfo_children():
            widget.destroy()
        
        mode = self.mode.get()
        
        if mode == "basic":
            self.create_basic_keyboard()
        elif mode == "scientific":
            self.create_scientific_keyboard()
        else:  # functions
            self.create_functions_panel()
    
    def create_basic_keyboard(self):
        """Teclado básico"""
        buttons = [
            [('C', COLORS['accent_pink']), ('⌫', COLORS['accent_orange']), 
             ('%', COLORS['button_func']), ('/', COLORS['button_op'])],
            [('7', COLORS['button_num']), ('8', COLORS['button_num']), 
             ('9', COLORS['button_num']), ('×', COLORS['button_op'])],
            [('4', COLORS['button_num']), ('5', COLORS['button_num']), 
             ('6', COLORS['button_num']), ('-', COLORS['button_op'])],
            [('1', COLORS['button_num']), ('2', COLORS['button_num']), 
             ('3', COLORS['button_num']), ('+', COLORS['button_op'])],
            [('±', COLORS['button_func']), ('0', COLORS['button_num']), 
             ('.', COLORS['button_num']), ('=', COLORS['accent_green'])]
        ]
        
        for row in buttons:
            row_frame = tk.Frame(self.keyboard_frame, bg=COLORS['bg_primary'])
            row_frame.pack(fill=tk.BOTH, expand=True, pady=3)
            
            for btn_text, btn_color in row:
                btn_container = tk.Frame(row_frame, bg=COLORS['bg_primary'])
                btn_container.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=3)
                
                btn = RoundedButton(
                    btn_container,
                    text=btn_text,
                    command=lambda t=btn_text: self.on_button_click(t),
                    bg_color=btn_color,
                    hover_color=COLORS['accent_blue'],
                    font=("Segoe UI", 16, "bold"),
                    width=120,
                    height=60
                )
                btn.pack(fill=tk.BOTH, expand=True)
    
    def create_scientific_keyboard(self):
        """Teclado científico"""
        buttons = [
            [('sin', COLORS['button_func']), ('cos', COLORS['button_func']), 
             ('tan', COLORS['button_func']), ('DEG', COLORS['accent_orange']), 
             ('C', COLORS['accent_pink'])],
            [('sin⁻¹', COLORS['button_func']), ('cos⁻¹', COLORS['button_func']), 
             ('tan⁻¹', COLORS['button_func']), ('(', COLORS['button_op']), 
             (')', COLORS['button_op'])],
            [('x²', COLORS['button_func']), ('x³', COLORS['button_func']), 
             ('xⁿ', COLORS['button_func']), ('√', COLORS['button_func']), 
             ('∛', COLORS['button_func'])],
            [('log', COLORS['button_func']), ('ln', COLORS['button_func']), 
             ('eˣ', COLORS['button_func']), ('10ˣ', COLORS['button_func']), 
             ('⌫', COLORS['accent_orange'])],
            [('7', COLORS['button_num']), ('8', COLORS['button_num']), 
             ('9', COLORS['button_num']), ('/', COLORS['button_op']), 
             ('π', COLORS['accent_yellow'])],
            [('4', COLORS['button_num']), ('5', COLORS['button_num']), 
             ('6', COLORS['button_num']), ('×', COLORS['button_op']), 
             ('e', COLORS['accent_yellow'])],
            [('1', COLORS['button_num']), ('2', COLORS['button_num']), 
             ('3', COLORS['button_num']), ('-', COLORS['button_op']), 
             ('!', COLORS['button_func'])],
            [('±', COLORS['button_func']), ('0', COLORS['button_num']), 
             ('.', COLORS['button_num']), ('+', COLORS['button_op']), 
             ('=', COLORS['accent_green'])]
        ]
        
        for row in buttons:
            row_frame = tk.Frame(self.keyboard_frame, bg=COLORS['bg_primary'])
            row_frame.pack(fill=tk.BOTH, expand=True, pady=2)
            
            for btn_text, btn_color in row:
                btn_container = tk.Frame(row_frame, bg=COLORS['bg_primary'])
                btn_container.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=2)
                
                btn = RoundedButton(
                    btn_container,
                    text=btn_text,
                    command=lambda t=btn_text: self.on_button_click(t),
                    bg_color=btn_color,
                    hover_color=COLORS['accent_blue'],
                    font=("Segoe UI", 12, "bold"),
                    width=100,
                    height=50
                )
                btn.pack(fill=tk.BOTH, expand=True)
    
    def create_functions_panel(self):
        """Panel de funciones con interfaz intuitiva"""
        self.function_panel = FunctionInputPanel(
            self.keyboard_frame,
            on_derive_callback=self.derive_function,
            on_graph_callback=self.graph_function,
            colors=COLORS
        )
        self.function_panel.pack(fill=tk.BOTH, expand=True)
    
    def on_button_click(self, text):
        """Maneja clicks en botones"""
        if text == 'C':
            self.clear()
        elif text == '⌫':
            self.backspace()
        elif text == '=':
            self.calculate()
        elif text == '±':
            self.toggle_sign()
        elif text == 'DEG':
            self.toggle_angle_mode()
        elif text == 'π':
            self.append_to_input(str(PI))
        elif text == 'e':
            self.append_to_input(str(E))
        elif text == 'x²':
            self.append_to_input('**2')
        elif text == 'x³':
            self.append_to_input('**3')
        elif text == 'xⁿ':
            self.append_to_input('**')
        elif text == '√':
            self.append_to_input('sqrt(')
        elif text == '∛':
            self.append_to_input('cbrt(')
        elif text == 'eˣ':
            self.append_to_input('exp(')
        elif text == '10ˣ':
            self.append_to_input('10**(')
        elif text == '!':
            self.append_to_input('!')
        elif text in ['sin', 'cos', 'tan', 'sin⁻¹', 'cos⁻¹', 'tan⁻¹', 'log', 'ln']:
            func_map = {
                'sin⁻¹': 'asin',
                'cos⁻¹': 'acos',
                'tan⁻¹': 'atan'
            }
            func = func_map.get(text, text)
            self.append_to_input(func + '(')
        elif text == '×':
            self.append_to_input('*')
        else:
            self.append_to_input(text)
    
    def toggle_angle_mode(self):
        """Cambia entre grados y radianes"""
        if self.angle_mode.get() == 'deg':
            self.angle_mode.set('rad')
            self.angle_indicator.config(text='RAD')
            self.evaluator.angle_mode = 'rad'
        else:
            self.angle_mode.set('deg')
            self.angle_indicator.config(text='DEG')
            self.evaluator.angle_mode = 'deg'
    
    def append_to_input(self, text):
        """Añade texto al input"""
        if self.result_shown:
            self.current_input = ""
            self.result_shown = False
        
        self.current_input += text
        self.update_display()
    
    def update_display(self):
        """Actualiza el display"""
        if self.current_input == "":
            self.main_display.config(text="0")
        else:
            display_text = format_expression(self.current_input)
            self.main_display.config(text=display_text)
    
    def clear(self):
        """Limpia el display"""
        self.current_input = ""
        self.result_shown = False
        self.history_display.config(text="")
        self.update_display()
    
    def backspace(self):
        """Borra el último carácter"""
        if not self.result_shown and self.current_input:
            self.current_input = self.current_input[:-1]
            self.update_display()
    
    def toggle_sign(self):
        """Cambia el signo"""
        if self.current_input and not self.result_shown:
            if self.current_input.startswith('-'):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.update_display()
    
    def calculate(self):
        """Calcula el resultado"""
        if not self.current_input:
            return
        
        try:
            result = self.evaluator.evaluate(self.current_input)
            
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
            
            self.history_display.config(text=format_expression(self.current_input))
            self.current_input = str(result)
            self.result_shown = True
            self.update_display()
            
        except Exception as e:
            messagebox.showerror("Error", f"Expresión inválida:\n{str(e)}")
            self.clear()
    
    def derive_function(self):
        """Deriva la función ingresada"""
        try:
            function = self.function_panel.get_function()
            if not function:
                messagebox.showwarning("Advertencia", "Ingresa una función primero")
                return
            
            # Derivar
            derivative = self.derivative_engine.derive(function)
            
            # Mostrar en display
            self.history_display.config(text=f"f(x) = {function}")
            self.main_display.config(text=f"f'(x) = {derivative}")
            
            messagebox.showinfo("Derivada", 
                              f"Función original:\nf(x) = {function}\n\n"
                              f"Derivada:\nf'(x) = {derivative}")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def graph_function(self):
        """Abre ventana de gráfica"""
        try:
            function = self.function_panel.get_function()
            if not function:
                messagebox.showwarning("Advertencia", "Ingresa una función primero")
                return
            
            # Crear o actualizar ventana de gráfica
            if self.graph_window is None or not self.graph_window.winfo_exists():
                self.graph_window = GraphWindow(self.root)
            
            self.graph_window.plot_function(function, show_derivative=True)
            self.graph_window.lift()
            self.graph_window.focus()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo graficar:\n{str(e)}")

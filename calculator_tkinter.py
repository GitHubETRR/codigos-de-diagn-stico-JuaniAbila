import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
import math
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class RoundedButton(tk.Canvas):
    """Botón personalizado con bordes redondeados"""
    
    def __init__(self, parent, text, command=None, bg_color="#2d3250", 
                 fg_color="#ffffff", hover_color="#4a9eff", font=("Segoe UI", 14, "bold"),
                 width=80, height=50):
        super().__init__(parent, width=width, height=height, 
                        bg=parent['bg'], highlightthickness=0)
        
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.fg_color = fg_color
        self.text = text
        self.font = font
        self.width = width
        self.height = height
        
        self.draw_button(bg_color)
        
        # Bindings
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def draw_button(self, bg_color):
        """Dibuja el botón redondeado"""
        self.delete("all")
        
        # Radio de las esquinas
        radius = 15
        
        # Crear rectángulo redondeado
        self.create_rounded_rectangle(2, 2, self.width-2, self.height-2, 
                                      radius, fill=bg_color, outline="")
        
        # Texto
        self.create_text(self.width/2, self.height/2, text=self.text, 
                        fill=self.fg_color, font=self.font)
    
    def create_rounded_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
        """Crea un rectángulo con esquinas redondeadas"""
        points = [
            x1+radius, y1,
            x1+radius, y1,
            x2-radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def on_click(self, event):
        """Maneja el click"""
        if self.command:
            self.command()
    
    def on_enter(self, event):
        """Maneja el hover"""
        self.draw_button(self.hover_color)
    
    def on_leave(self, event):
        """Maneja cuando sale el mouse"""
        self.draw_button(self.bg_color)


class GraphWindow(Toplevel):
    """Ventana separada para gráficas"""
    
    def __init__(self, parent, colors):
        super().__init__(parent)
        self.title("📊 Visualización de Funciones")
        self.geometry("800x600")
        self.configure(bg=colors['bg_secondary'])
        
        self.colors = colors
        
        # Header
        header = tk.Frame(self, bg=colors['accent_blue'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(
            header,
            text="📊 Gráfica de Funciones",
            font=("Segoe UI", 18, "bold"),
            bg=colors['accent_blue'],
            fg=colors['text_primary']
        )
        title.pack(expand=True)
        
        # Frame para la gráfica
        graph_container = tk.Frame(self, bg=colors['bg_secondary'])
        graph_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Crear figura de matplotlib
        self.fig = Figure(figsize=(8, 6), facecolor=colors['bg_secondary'])
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor(colors['display_bg'])
        self.ax.grid(True, alpha=0.3, color=colors['text_secondary'], linestyle='--')
        self.ax.set_xlabel('x', color=colors['text_primary'], fontsize=12, fontweight='bold')
        self.ax.set_ylabel('y', color=colors['text_primary'], fontsize=12, fontweight='bold')
        self.ax.tick_params(colors=colors['text_primary'], labelsize=10)
        
        # Spines
        for spine in self.ax.spines.values():
            spine.set_color(colors['text_secondary'])
            spine.set_linewidth(1.5)
        
        # Canvas
        self.canvas = FigureCanvasTkAgg(self.fig, graph_container)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Mensaje inicial
        self.show_empty_message()
    
    def show_empty_message(self):
        """Muestra mensaje cuando no hay gráfica"""
        self.ax.clear()
        self.ax.set_facecolor(self.colors['display_bg'])
        self.ax.grid(True, alpha=0.3, color=self.colors['text_secondary'], linestyle='--')
        self.ax.text(0.5, 0.5, 'Esperando función para graficar...',
                    ha='center', va='center', transform=self.ax.transAxes,
                    fontsize=14, color=self.colors['text_secondary'],
                    style='italic')
        self.canvas.draw()
    
    def plot_polynomial(self, coefficients, derivative):
        """Grafica polinomio y su derivada"""
        try:
            # Crear rango de x
            x = np.linspace(-10, 10, 500)
            
            # Calcular y para función original
            y_original = np.zeros_like(x)
            for i, coef in enumerate(coefficients):
                y_original += coef * (x ** i)
            
            # Calcular y para derivada
            y_derivative = np.zeros_like(x)
            for i, coef in enumerate(derivative):
                y_derivative += coef * (x ** i)
            
            # Limpiar gráfica
            self.ax.clear()
            self.ax.set_facecolor(self.colors['display_bg'])
            self.ax.grid(True, alpha=0.3, color=self.colors['text_secondary'], 
                        linestyle='--', linewidth=0.8)
            
            # Ejes
            self.ax.axhline(y=0, color=self.colors['text_secondary'], 
                           linewidth=1.5, alpha=0.5)
            self.ax.axvline(x=0, color=self.colors['text_secondary'], 
                           linewidth=1.5, alpha=0.5)
            
            # Graficar con estilo
            self.ax.plot(x, y_original, color=self.colors['accent_blue'], 
                        linewidth=3, label='f(x)', alpha=0.9)
            self.ax.plot(x, y_derivative, color=self.colors['accent_pink'], 
                        linewidth=3, label="f'(x)", linestyle='--', alpha=0.9)
            
            # Etiquetas y título
            self.ax.set_xlabel('x', color=self.colors['text_primary'], 
                             fontsize=12, fontweight='bold')
            self.ax.set_ylabel('y', color=self.colors['text_primary'], 
                             fontsize=12, fontweight='bold')
            self.ax.set_title('Función Polinomial y su Derivada', 
                            color=self.colors['accent_blue'], 
                            fontsize=14, fontweight='bold', pad=15)
            self.ax.tick_params(colors=self.colors['text_primary'], labelsize=10)
            
            # Leyenda mejorada
            legend = self.ax.legend(
                facecolor=self.colors['bg_tertiary'], 
                edgecolor=self.colors['accent_blue'],
                labelcolor=self.colors['text_primary'],
                fontsize=11,
                framealpha=0.9,
                shadow=True
            )
            
            # Spines
            for spine in self.ax.spines.values():
                spine.set_color(self.colors['text_secondary'])
                spine.set_linewidth(1.5)
            
            # Actualizar
            self.canvas.draw()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo graficar:\n{str(e)}")


class ScientificCalculator:
    """Calculadora Científica estilo Casio con diseño premium"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Científica Casio")
        self.root.geometry("650x750")
        self.root.configure(bg="#0a0e27")
        self.root.resizable(False, False)
        
        # Variables
        self.current_input = ""
        self.result_shown = False
        self.mode = tk.StringVar(value="basic")
        self.angle_mode = tk.StringVar(value="deg")
        self.memory = 0
        self.graph_window = None
        
        # Colores del tema
        self.colors = {
            'bg_primary': '#0a0e27',
            'bg_secondary': '#1a1f3a',
            'bg_tertiary': '#2a2f4a',
            'accent_blue': '#4a9eff',
            'accent_purple': '#b47eff',
            'accent_pink': '#ff6b9d',
            'accent_green': '#00d9a3',
            'accent_orange': '#ff9f43',
            'accent_yellow': '#ffd93d',
            'text_primary': '#ffffff',
            'text_secondary': '#a0a8c0',
            'display_bg': '#141829',
            'button_num': '#2d3250',
            'button_op': '#424769',
            'button_func': '#7077a1',
        }
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Container principal con padding
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Header
        self.create_header(main_container)
        
        # Display
        self.create_display(main_container)
        
        # Selector de modo
        self.create_mode_selector(main_container)
        
        # Teclado
        self.keyboard_frame = tk.Frame(main_container, bg=self.colors['bg_primary'])
        self.keyboard_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.update_keyboard()
    
    def create_header(self, parent):
        """Crea el header"""
        header = tk.Frame(parent, bg=self.colors['bg_primary'])
        header.pack(fill=tk.X, pady=(0, 15))
        
        # Título con gradiente
        title_frame = tk.Frame(header, bg=self.colors['accent_blue'], height=50)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title = tk.Label(
            title_frame,
            text="🧮 CASIO fx-991",
            font=("Segoe UI", 20, "bold"),
            bg=self.colors['accent_blue'],
            fg=self.colors['text_primary']
        )
        title.pack(expand=True)
    
    def create_display(self, parent):
        """Crea el display LCD mejorado"""
        display_container = tk.Frame(parent, bg=self.colors['bg_secondary'], 
                                     relief=tk.RAISED, bd=3)
        display_container.pack(fill=tk.X, pady=(0, 15))
        
        # Display frame interno
        display_frame = tk.Frame(display_container, bg=self.colors['display_bg'])
        display_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Indicadores superiores
        indicators = tk.Frame(display_frame, bg=self.colors['display_bg'])
        indicators.pack(fill=tk.X, pady=(5, 0))
        
        self.mode_indicator = tk.Label(
            indicators,
            text="COMP",
            font=("Consolas", 9, "bold"),
            bg=self.colors['display_bg'],
            fg=self.colors['accent_green']
        )
        self.mode_indicator.pack(side=tk.LEFT, padx=10)
        
        self.angle_indicator = tk.Label(
            indicators,
            text="DEG",
            font=("Consolas", 9, "bold"),
            bg=self.colors['display_bg'],
            fg=self.colors['accent_orange']
        )
        self.angle_indicator.pack(side=tk.LEFT)
        
        # Display secundario
        self.history_display = tk.Label(
            display_frame,
            text="",
            font=("Consolas", 11),
            bg=self.colors['display_bg'],
            fg=self.colors['text_secondary'],
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
            bg=self.colors['display_bg'],
            fg=self.colors['text_primary'],
            anchor=tk.E,
            padx=15,
            pady=12
        )
        self.main_display.pack(fill=tk.X)
    
    def create_mode_selector(self, parent):
        """Crea el selector de modo mejorado"""
        mode_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        mode_frame.pack(fill=tk.X, pady=(0, 10))
        
        modes = [
            ("Básica", "basic", self.colors['accent_green']),
            ("Científica", "scientific", self.colors['accent_blue']),
            ("Polinomios", "polynomial", self.colors['accent_purple'])
        ]
        
        for text, value, color in modes:
            btn_frame = tk.Frame(mode_frame, bg=self.colors['bg_primary'])
            btn_frame.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
            
            btn = RoundedButton(
                btn_frame,
                text=text,
                command=lambda v=value: self.change_mode(v),
                bg_color=color if self.mode.get() == value else self.colors['bg_tertiary'],
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
        self.create_mode_selector(self.root.winfo_children()[0])
    
    def update_keyboard(self):
        """Actualiza el teclado"""
        for widget in self.keyboard_frame.winfo_children():
            widget.destroy()
        
        mode = self.mode.get()
        
        if mode == "basic":
            self.create_basic_keyboard()
        elif mode == "scientific":
            self.create_scientific_keyboard()
        else:
            self.create_polynomial_keyboard()
    
    def create_basic_keyboard(self):
        """Teclado básico con botones redondeados"""
        buttons = [
            [('C', self.colors['accent_pink']), ('⌫', self.colors['accent_orange']), 
             ('%', self.colors['button_func']), ('/', self.colors['button_op'])],
            [('7', self.colors['button_num']), ('8', self.colors['button_num']), 
             ('9', self.colors['button_num']), ('×', self.colors['button_op'])],
            [('4', self.colors['button_num']), ('5', self.colors['button_num']), 
             ('6', self.colors['button_num']), ('-', self.colors['button_op'])],
            [('1', self.colors['button_num']), ('2', self.colors['button_num']), 
             ('3', self.colors['button_num']), ('+', self.colors['button_op'])],
            [('±', self.colors['button_func']), ('0', self.colors['button_num']), 
             ('.', self.colors['button_num']), ('=', self.colors['accent_green'])]
        ]
        
        for row in buttons:
            row_frame = tk.Frame(self.keyboard_frame, bg=self.colors['bg_primary'])
            row_frame.pack(fill=tk.BOTH, expand=True, pady=3)
            
            for btn_text, btn_color in row:
                btn_container = tk.Frame(row_frame, bg=self.colors['bg_primary'])
                btn_container.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=3)
                
                btn = RoundedButton(
                    btn_container,
                    text=btn_text,
                    command=lambda t=btn_text: self.on_button_click(t),
                    bg_color=btn_color,
                    hover_color=self.colors['accent_blue'],
                    font=("Segoe UI", 16, "bold"),
                    width=120,
                    height=60
                )
                btn.pack(fill=tk.BOTH, expand=True)
    
    def create_scientific_keyboard(self):
        """Teclado científico estilo Casio"""
        buttons = [
            [('sin', self.colors['button_func']), ('cos', self.colors['button_func']), 
             ('tan', self.colors['button_func']), ('DEG', self.colors['accent_orange']), 
             ('C', self.colors['accent_pink'])],
            [('sin⁻¹', self.colors['button_func']), ('cos⁻¹', self.colors['button_func']), 
             ('tan⁻¹', self.colors['button_func']), ('(', self.colors['button_op']), 
             (')', self.colors['button_op'])],
            [('x²', self.colors['button_func']), ('x³', self.colors['button_func']), 
             ('xⁿ', self.colors['button_func']), ('√', self.colors['button_func']), 
             ('∛', self.colors['button_func'])],
            [('log', self.colors['button_func']), ('ln', self.colors['button_func']), 
             ('eˣ', self.colors['button_func']), ('10ˣ', self.colors['button_func']), 
             ('⌫', self.colors['accent_orange'])],
            [('7', self.colors['button_num']), ('8', self.colors['button_num']), 
             ('9', self.colors['button_num']), ('/', self.colors['button_op']), 
             ('π', self.colors['accent_yellow'])],
            [('4', self.colors['button_num']), ('5', self.colors['button_num']), 
             ('6', self.colors['button_num']), ('×', self.colors['button_op']), 
             ('e', self.colors['accent_yellow'])],
            [('1', self.colors['button_num']), ('2', self.colors['button_num']), 
             ('3', self.colors['button_num']), ('-', self.colors['button_op']), 
             ('!', self.colors['button_func'])],
            [('±', self.colors['button_func']), ('0', self.colors['button_num']), 
             ('.', self.colors['button_num']), ('+', self.colors['button_op']), 
             ('=', self.colors['accent_green'])]
        ]
        
        for row in buttons:
            row_frame = tk.Frame(self.keyboard_frame, bg=self.colors['bg_primary'])
            row_frame.pack(fill=tk.BOTH, expand=True, pady=2)
            
            for btn_text, btn_color in row:
                btn_container = tk.Frame(row_frame, bg=self.colors['bg_primary'])
                btn_container.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=2)
                
                btn = RoundedButton(
                    btn_container,
                    text=btn_text,
                    command=lambda t=btn_text: self.on_button_click(t),
                    bg_color=btn_color,
                    hover_color=self.colors['accent_blue'],
                    font=("Segoe UI", 12, "bold"),
                    width=100,
                    height=50
                )
                btn.pack(fill=tk.BOTH, expand=True)
    
    def create_polynomial_keyboard(self):
        """Teclado para polinomios"""
        input_frame = tk.Frame(self.keyboard_frame, bg=self.colors['bg_secondary'],
                              relief=tk.RAISED, bd=3)
        input_frame.pack(fill=tk.X, pady=(0, 15), padx=5)
        
        label = tk.Label(
            input_frame,
            text="Ingresa el polinomio (ej: 3x^2 + 2x - 5):",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        )
        label.pack(pady=(15, 8))
        
        self.poly_input = tk.Entry(
            input_frame,
            font=("Consolas", 16),
            bg=self.colors['display_bg'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['accent_blue'],
            relief=tk.FLAT,
            justify=tk.CENTER,
            bd=0
        )
        self.poly_input.pack(fill=tk.X, padx=25, pady=(5, 15), ipady=8)
        
        # Botones de acción
        action_frame = tk.Frame(self.keyboard_frame, bg=self.colors['bg_primary'])
        action_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        buttons = [
            ("📐 DERIVAR", self.colors['accent_purple'], self.derive_polynomial),
            ("📊 GRAFICAR", self.colors['accent_blue'], self.graph_polynomial),
            ("🗑️ LIMPIAR", self.colors['accent_pink'], self.clear_polynomial)
        ]
        
        for text, color, cmd in buttons:
            btn_container = tk.Frame(action_frame, bg=self.colors['bg_primary'])
            btn_container.pack(fill=tk.BOTH, expand=True, pady=5, padx=10)
            
            btn = RoundedButton(
                btn_container,
                text=text,
                command=cmd,
                bg_color=color,
                hover_color=self.colors['accent_orange'],
                font=("Segoe UI", 16, "bold"),
                width=500,
                height=70
            )
            btn.pack(fill=tk.BOTH, expand=True)
    
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
            self.append_to_input(str(math.pi))
        elif text == 'e':
            self.append_to_input(str(math.e))
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
        else:
            self.angle_mode.set('deg')
            self.angle_indicator.config(text='DEG')
    
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
            display_text = self.current_input.replace('*', '×').replace('**', '^')
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
            expression = self.current_input
            eval_expr = expression.replace('^', '**')
            
            # Reemplazar funciones
            eval_expr = eval_expr.replace('sqrt', 'math.sqrt')
            eval_expr = eval_expr.replace('cbrt', 'lambda x: x**(1/3)')
            eval_expr = eval_expr.replace('exp', 'math.exp')
            
            # Funciones trigonométricas
            if self.angle_mode.get() == 'deg':
                eval_expr = eval_expr.replace('sin(', 'math.sin(math.radians(')
                eval_expr = eval_expr.replace('cos(', 'math.cos(math.radians(')
                eval_expr = eval_expr.replace('tan(', 'math.tan(math.radians(')
                eval_expr = eval_expr.replace('asin(', 'math.degrees(math.asin(')
                eval_expr = eval_expr.replace('acos(', 'math.degrees(math.acos(')
                eval_expr = eval_expr.replace('atan(', 'math.degrees(math.atan(')
                # Añadir paréntesis de cierre extra
                eval_expr = eval_expr.replace('radians(', 'radians(') + ')' * eval_expr.count('radians(')
            else:
                eval_expr = eval_expr.replace('sin', 'math.sin')
                eval_expr = eval_expr.replace('cos', 'math.cos')
                eval_expr = eval_expr.replace('tan', 'math.tan')
                eval_expr = eval_expr.replace('asin', 'math.asin')
                eval_expr = eval_expr.replace('acos', 'math.acos')
                eval_expr = eval_expr.replace('atan', 'math.atan')
            
            eval_expr = eval_expr.replace('log', 'math.log10')
            eval_expr = eval_expr.replace('ln', 'math.log')
            
            # Factorial
            if '!' in eval_expr:
                eval_expr = self.handle_factorial(eval_expr)
            
            result = eval(eval_expr)
            
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
            
            self.history_display.config(text=expression.replace('*', '×').replace('**', '^'))
            self.current_input = str(result)
            self.result_shown = True
            self.update_display()
            
        except Exception as e:
            messagebox.showerror("Error", f"Expresión inválida:\n{str(e)}")
            self.clear()
    
    def handle_factorial(self, expr):
        """Maneja factoriales"""
        import re
        pattern = r'(\d+)!'
        matches = re.findall(pattern, expr)
        for match in matches:
            factorial_val = math.factorial(int(match))
            expr = expr.replace(f'{match}!', str(factorial_val))
        return expr
    
    def parse_polynomial(self, poly_str):
        """Parsea polinomio"""
        try:
            poly_str = poly_str.replace(' ', '').lower()
            max_degree = 0
            matches = re.findall(r'x\^(\d+)', poly_str)
            if matches:
                max_degree = max(int(m) for m in matches)
            if 'x' in poly_str and max_degree == 0:
                max_degree = 1
            
            coefficients = [0] * (max_degree + 1)
            
            if poly_str[0] not in ['+', '-']:
                poly_str = '+' + poly_str
            
            terms = re.findall(r'[+-][^+-]+', poly_str)
            
            for term in terms:
                term = term.strip()
                
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
                
                match = re.match(r'([+-]?\d+\.?\d*)', term)
                if match:
                    coef = float(match.group(1))
                    coefficients[0] = coef
            
            return coefficients
            
        except Exception as e:
            raise ValueError(f"No se pudo parsear el polinomio: {str(e)}")
    
    def format_polynomial(self, coefficients):
        """Formatea polinomio"""
        if not coefficients or all(c == 0 for c in coefficients):
            return "0"
        
        terms = []
        degree = len(coefficients) - 1
        
        for i in range(degree, -1, -1):
            coef = coefficients[i]
            
            if coef == 0:
                continue
            
            if terms:
                sign = " + " if coef > 0 else " - "
                coef = abs(coef)
            else:
                sign = "" if coef > 0 else "-"
                coef = abs(coef)
            
            if coef == int(coef):
                coef_str = str(int(coef))
            else:
                coef_str = f"{coef:.2f}"
            
            if i == 0:
                term = f"{sign}{coef_str}"
            elif i == 1:
                if coef == 1:
                    term = f"{sign}x"
                else:
                    term = f"{sign}{coef_str}x"
            else:
                superscript = str(i).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))
                if coef == 1:
                    term = f"{sign}x{superscript}"
                else:
                    term = f"{sign}{coef_str}x{superscript}"
            
            terms.append(term)
        
        return "".join(terms) if terms else "0"
    
    def derive_polynomial(self):
        """Deriva polinomio"""
        try:
            poly_str = self.poly_input.get().strip()
            if not poly_str:
                messagebox.showwarning("Advertencia", "Ingresa un polinomio primero")
                return
            
            coefficients = self.parse_polynomial(poly_str)
            
            if len(coefficients) <= 1:
                derivative = [0]
            else:
                derivative = []
                for i in range(1, len(coefficients)):
                    derivative.append(coefficients[i] * i)
            
            original = self.format_polynomial(coefficients)
            derived = self.format_polynomial(derivative)
            
            self.history_display.config(text=f"f(x) = {original}")
            self.main_display.config(text=f"f'(x) = {derived}")
            
            messagebox.showinfo("Derivada", 
                              f"Función original:\nf(x) = {original}\n\n"
                              f"Derivada:\nf'(x) = {derived}")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def graph_polynomial(self):
        """Abre ventana de gráfica"""
        try:
            poly_str = self.poly_input.get().strip()
            if not poly_str:
                messagebox.showwarning("Advertencia", "Ingresa un polinomio primero")
                return
            
            coefficients = self.parse_polynomial(poly_str)
            
            if len(coefficients) <= 1:
                derivative = [0]
            else:
                derivative = []
                for i in range(1, len(coefficients)):
                    derivative.append(coefficients[i] * i)
            
            # Crear o actualizar ventana de gráfica
            if self.graph_window is None or not self.graph_window.winfo_exists():
                self.graph_window = GraphWindow(self.root, self.colors)
            
            self.graph_window.plot_polynomial(coefficients, derivative)
            self.graph_window.lift()
            self.graph_window.focus()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo graficar:\n{str(e)}")
    
    def clear_polynomial(self):
        """Limpia polinomio"""
        self.poly_input.delete(0, tk.END)
        self.history_display.config(text="")
        self.main_display.config(text="0")


def main():
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()

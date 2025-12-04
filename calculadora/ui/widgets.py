"""
Widgets personalizados para la calculadora
"""

import tkinter as tk
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.constants import COLORS, BUTTON_RADIUS


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
        
        radius = BUTTON_RADIUS
        
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


class FunctionInputPanel(tk.Frame):
    """Panel de entrada intuitivo para funciones (estilo GeoGebra)"""
    
    def __init__(self, parent, on_derive_callback, on_graph_callback, colors):
        super().__init__(parent, bg=colors['bg_secondary'])
        self.colors = colors
        self.on_derive = on_derive_callback
        self.on_graph = on_graph_callback
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz del panel"""
        # Título
        title = tk.Label(
            self,
            text="Editor de Funciones",
            font=("Segoe UI", 13, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['accent_blue']
        )
        title.pack(pady=(15, 10))
        
        # Frame para el input
        input_container = tk.Frame(self, bg=self.colors['bg_secondary'])
        input_container.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        # Label f(x) =
        label = tk.Label(
            input_container,
            text="f(x) =",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        )
        label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Entry para la función
        self.function_entry = tk.Entry(
            input_container,
            font=("Consolas", 14),
            bg=self.colors['display_bg'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['accent_blue'],
            relief=tk.FLAT,
            bd=0
        )
        self.function_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
        
        # Botones rápidos para funciones comunes
        quick_buttons_frame = tk.Frame(self, bg=self.colors['bg_secondary'])
        quick_buttons_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        quick_label = tk.Label(
            quick_buttons_frame,
            text="Funciones rápidas:",
            font=("Segoe UI", 10),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_secondary']
        )
        quick_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Grid de botones rápidos
        buttons_grid = tk.Frame(quick_buttons_frame, bg=self.colors['bg_secondary'])
        buttons_grid.pack(fill=tk.X)
        
        quick_functions = [
            ('x²', 'x^2'),
            ('x³', 'x^3'),
            ('√x', 'sqrt(x)'),
            ('sin(x)', 'sin(x)'),
            ('cos(x)', 'cos(x)'),
            ('tan(x)', 'tan(x)'),
            ('eˣ', 'e^x'),
            ('ln(x)', 'ln(x)'),
            ('1/x', '1/x'),
            ('|x|', 'abs(x)')
        ]
        
        for i, (display, insert) in enumerate(quick_functions):
            row = i // 5
            col = i % 5
            
            btn_frame = tk.Frame(buttons_grid, bg=self.colors['bg_secondary'])
            btn_frame.grid(row=row, column=col, padx=2, pady=2, sticky='ew')
            
            btn = RoundedButton(
                btn_frame,
                text=display,
                command=lambda t=insert: self.insert_function(t),
                bg_color=self.colors['button_func'],
                hover_color=self.colors['accent_purple'],
                font=("Segoe UI", 10, "bold"),
                width=90,
                height=35
            )
            btn.pack(fill=tk.X)
        
        # Configurar columnas para que se expandan uniformemente
        for i in range(5):
            buttons_grid.columnconfigure(i, weight=1)
        
        # Preview de la función
        preview_frame = tk.Frame(self, bg=self.colors['bg_tertiary'], 
                                relief=tk.RAISED, bd=2)
        preview_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        preview_label = tk.Label(
            preview_frame,
            text="Vista previa:",
            font=("Segoe UI", 9),
            bg=self.colors['bg_tertiary'],
            fg=self.colors['text_secondary']
        )
        preview_label.pack(anchor=tk.W, padx=10, pady=(5, 0))
        
        self.preview_display = tk.Label(
            preview_frame,
            text="",
            font=("Consolas", 12),
            bg=self.colors['bg_tertiary'],
            fg=self.colors['accent_green'],
            anchor=tk.W,
            wraplength=500
        )
        self.preview_display.pack(fill=tk.X, padx=10, pady=(0, 5))
        
        # Bind para actualizar preview
        self.function_entry.bind('<KeyRelease>', self.update_preview)
        
        # Botones de acción
        action_frame = tk.Frame(self, bg=self.colors['bg_secondary'])
        action_frame.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        buttons = [
            ("📐 DERIVAR", self.colors['accent_purple'], self.on_derive),
            ("📊 GRAFICAR", self.colors['accent_blue'], self.on_graph),
            ("🗑️ LIMPIAR", self.colors['accent_pink'], self.clear)
        ]
        
        for text, color, cmd in buttons:
            btn_container = tk.Frame(action_frame, bg=self.colors['bg_secondary'])
            btn_container.pack(fill=tk.X, pady=3)
            
            btn = RoundedButton(
                btn_container,
                text=text,
                command=cmd,
                bg_color=color,
                hover_color=self.colors['accent_orange'],
                font=("Segoe UI", 14, "bold"),
                width=500,
                height=55
            )
            btn.pack(fill=tk.X)
    
    def insert_function(self, text):
        """Inserta una función en la posición del cursor"""
        cursor_pos = self.function_entry.index(tk.INSERT)
        self.function_entry.insert(cursor_pos, text)
        self.function_entry.focus()
        self.update_preview()
    
    def update_preview(self, event=None):
        """Actualiza la vista previa de la función"""
        text = self.function_entry.get()
        if text:
            # Formatear para mostrar
            preview = text.replace('^', '⁽ˣ⁾').replace('*', '·')
            self.preview_display.config(text=f"f(x) = {preview}")
        else:
            self.preview_display.config(text="")
    
    def get_function(self):
        """Obtiene la función ingresada"""
        return self.function_entry.get().strip()
    
    def clear(self):
        """Limpia el input"""
        self.function_entry.delete(0, tk.END)
        self.preview_display.config(text="")

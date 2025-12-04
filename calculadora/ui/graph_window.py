"""
Ventana de gráficas separada
"""

import tkinter as tk
from tkinter import Toplevel
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from math_engine import ExpressionEvaluator, DerivativeEngine
from utils.constants import COLORS, GRAPH_WINDOW_WIDTH, GRAPH_WINDOW_HEIGHT


class GraphWindow(Toplevel):
    """Ventana separada para gráficas"""
    
    def __init__(self, parent):
        super().__init__(parent)
        self.title("📊 Visualización de Funciones")
        self.geometry(f"{GRAPH_WINDOW_WIDTH}x{GRAPH_WINDOW_HEIGHT}")
        self.configure(bg=COLORS['bg_secondary'])
        
        self.evaluator = ExpressionEvaluator()
        self.derivative_engine = DerivativeEngine()
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz"""
        # Header
        header = tk.Frame(self, bg=COLORS['accent_blue'], height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        title = tk.Label(
            header,
            text="📊 Gráfica de Funciones",
            font=("Segoe UI", 18, "bold"),
            bg=COLORS['accent_blue'],
            fg=COLORS['text_primary']
        )
        title.pack(expand=True)
        
        # Frame para la gráfica
        graph_container = tk.Frame(self, bg=COLORS['bg_secondary'])
        graph_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Crear figura de matplotlib
        self.fig = Figure(figsize=(8, 6), facecolor=COLORS['bg_secondary'])
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor(COLORS['display_bg'])
        self.ax.grid(True, alpha=0.3, color=COLORS['text_secondary'], linestyle='--')
        self.ax.set_xlabel('x', color=COLORS['text_primary'], fontsize=12, fontweight='bold')
        self.ax.set_ylabel('y', color=COLORS['text_primary'], fontsize=12, fontweight='bold')
        self.ax.tick_params(colors=COLORS['text_primary'], labelsize=10)
        
        # Spines
        for spine in self.ax.spines.values():
            spine.set_color(COLORS['text_secondary'])
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
        self.ax.set_facecolor(COLORS['display_bg'])
        self.ax.grid(True, alpha=0.3, color=COLORS['text_secondary'], linestyle='--')
        self.ax.text(0.5, 0.5, 'Esperando función para graficar...',
                    ha='center', va='center', transform=self.ax.transAxes,
                    fontsize=14, color=COLORS['text_secondary'],
                    style='italic')
        self.canvas.draw()
    
    def plot_function(self, expression: str, show_derivative: bool = True):
        """Grafica una función y opcionalmente su derivada"""
        try:
            # Limpiar gráfica
            self.ax.clear()
            self.ax.set_facecolor(COLORS['display_bg'])
            self.ax.grid(True, alpha=0.3, color=COLORS['text_secondary'], 
                        linestyle='--', linewidth=0.8)
            
            # Ejes
            self.ax.axhline(y=0, color=COLORS['text_secondary'], 
                           linewidth=1.5, alpha=0.5)
            self.ax.axvline(x=0, color=COLORS['text_secondary'], 
                           linewidth=1.5, alpha=0.5)
            
            # Evaluar función original
            x_vals, y_vals = self.evaluator.evaluate_range(expression, -10, 10)
            
            # Graficar función original
            self.ax.plot(x_vals, y_vals, color=COLORS['accent_blue'], 
                        linewidth=3, label='f(x)', alpha=0.9)
            
            # Derivar y graficar derivada si se solicita
            if show_derivative:
                try:
                    derivative_expr = self.derivative_engine.derive(expression)
                    x_vals_d, y_vals_d = self.evaluator.evaluate_range(derivative_expr, -10, 10)
                    
                    self.ax.plot(x_vals_d, y_vals_d, color=COLORS['accent_pink'], 
                                linewidth=3, label="f'(x)", linestyle='--', alpha=0.9)
                except Exception as e:
                    print(f"No se pudo graficar la derivada: {e}")
            
            # Etiquetas y título
            self.ax.set_xlabel('x', color=COLORS['text_primary'], 
                             fontsize=12, fontweight='bold')
            self.ax.set_ylabel('y', color=COLORS['text_primary'], 
                             fontsize=12, fontweight='bold')
            self.ax.set_title(f'f(x) = {expression}', 
                            color=COLORS['accent_blue'], 
                            fontsize=14, fontweight='bold', pad=15)
            self.ax.tick_params(colors=COLORS['text_primary'], labelsize=10)
            
            # Leyenda
            legend = self.ax.legend(
                facecolor=COLORS['bg_tertiary'], 
                edgecolor=COLORS['accent_blue'],
                labelcolor=COLORS['text_primary'],
                fontsize=11,
                framealpha=0.9,
                shadow=True
            )
            
            # Spines
            for spine in self.ax.spines.values():
                spine.set_color(COLORS['text_secondary'])
                spine.set_linewidth(1.5)
            
            # Actualizar
            self.canvas.draw()
            
        except Exception as e:
            from tkinter import messagebox
            messagebox.showerror("Error", f"No se pudo graficar:\n{str(e)}")

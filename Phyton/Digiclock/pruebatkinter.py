import tkinter as tk

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Mi primera app con Tkinter")
ventana.geometry("300x500")

# Etiqueta inicial
label = tk.Label(ventana, text="Escribí tu nombre:")
label.pack(pady=10)

# Entrada de texto
entrada = tk.Entry(ventana, width=30)
entrada.pack()

# Función que se ejecuta al apretar el botón
def saludar():
    nombre = entrada.get()
    mensaje = f"Hola, {nombre}!"
    resultado.config(text=mensaje)

# Botón
boton = tk.Button(ventana, text="Saludar", command=saludar)
boton.pack(pady=10)

# Etiqueta donde aparecerá el saludo
resultado = tk.Label(ventana, text="", font=("Arial", 12))
resultado.pack(pady=10)

# Iniciar la app
ventana.mainloop()


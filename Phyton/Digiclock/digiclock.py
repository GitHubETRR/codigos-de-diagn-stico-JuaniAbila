import tkinter as tk
import time

# Crear la ventana
ventana = tk.Tk()
ventana.title("Reloj Digital")
ventana.geometry("300x100+50+50")
ventana.resizable(False, False)
#ventana.overrideredirect(True)
icono= tk.PhotoImage(file="C:\\Users\\ensanchez.ETRR\\Desktop\\codigos-de-diagn-stico-JuaniAbila\\Phyton\\Digiclock\\pokeball1.png")
ventana.iconphoto(True, icono)
#ventana.iconbitmap('pokeball2.ico')

# Etiqueta donde se mostrará la hora
label_hora = tk.Label(ventana, font=("Arial", 40), fg="black")
label_hora.pack(pady=20)

# Función que actualiza la hora cada segundo
def actualizar_hora():
    hora_actual = time.strftime("%H:%M:%S")
    label_hora.config(text=hora_actual)
    ventana.after(1000, actualizar_hora)  # se repite cada 1000 ms (1 segundo)

# Iniciar actualización
actualizar_hora()

# Ejecutar ventana
ventana.mainloop()

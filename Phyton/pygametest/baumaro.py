import os 
import sys 
import re  

import pandas as pd  
import seaborn as sns  
import matplotlib.pyplot as plt  

CARPETA_CLASES = "clases" 
ENCODING_CSV = "utf-8" 
MIN_NOTA = 0.0 
MAX_NOTA = 10.0  


sns.set(style="whitegrid", palette="deep", font_scale=1.1)  # configura estilo de seaborn


def asegurar_carpeta_clases():
    # Crea la carpeta `CARPETA_CLASES` si no existe
    if not os.path.exists(CARPETA_CLASES):
        os.makedirs(CARPETA_CLASES)


def listar_csv_clases():
    # Asegura que la carpeta exista y devuelve una lista ordenada de archivos .csv
    asegurar_carpeta_clases()
    archivos = []
    for f in os.listdir(CARPETA_CLASES):    
        if f.lower().endswith(".csv"):
            archivos.append(f)
    archivos.sort()
    return archivos


def ruta_clase(nombre_archivo):
    # Construye la ruta completa al archivo dentro de la carpeta de clases
    return os.path.join(CARPETA_CLASES, nombre_archivo)


def crear_csv_clase():
    # Interfaz para crear un nuevo CSV de clase pidiendo nombre y materias
    print("\nCrear nueva clase (CSV)")
    nombre = None
    # Pide el nombre hasta que sea válido (solo letras, números y guión bajo)
    while nombre is None:
        nombre = input("Nombre de la clase: ").strip()
        if re.search(r'[^A-Za-z0-9_]', nombre) or nombre == "":
            print("Nombre de clase inválido.")
            print("Use solo letras, números y guiones bajos (_).")
            print("ingrese otro nombre.")
            nombre = None

    nombre_archivo = nombre + ".csv"  # agrega extensión al nombre
    archivo = ruta_clase(nombre_archivo)  # ruta completa

    # Si ya existe, avisa y no sobreescribe
    if os.path.exists(archivo):
        print(f"Ya existe un CSV para esa clase: {archivo}")
        return None

    # Pide la cantidad de materias y valida que sea entero > 0
    cant = None
    while cant is None:
        try:
            cant = int(input("¿Cuántas materias tiene la clase?: ").strip())
            if cant <= 0:
                print("La cantidad debe ser mayor a 0.")
                print("ingrese otra cantidad.")
                cant = None
        except ValueError:
            print("Ingrese un número entero válido.")
            cant = None

    materias = []
    # Pide el nombre de cada materia y valida
    for i in range(cant):
        nombre_materia = None
        while nombre_materia is None:
            nombre_materia = input(f"Nombre de la materia #{i+1}: ").strip()
            if re.search(r'[^A-Za-z0-9_]', nombre_materia) or nombre_materia == "":
                print("Nombre de materia inválido.")
                nombre_materia = None
        materias.append(nombre_materia)

    columnas = ["Alumno ID", "Alumno"] + materias  # columnas iniciales del CSV
    df = pd.DataFrame(columns=columnas)  # dataframe vacío con las columnas
    df.to_csv(archivo, index=False, encoding=ENCODING_CSV)  # guarda CSV
    print(f" Clase creada: {archivo}")


# Separador visual grande (sin efecto en el código)
# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def cargar_df_clase(archivo):
    # Carga un CSV de clase dado su nombre (archivo) dentro de la carpeta de clases
    ruta = ruta_clase(archivo)  # obtiene la ruta completa
    try:
        df = pd.read_csv(ruta, encoding=ENCODING_CSV)  # lee el CSV con pandas
    except FileNotFoundError:
        print(f"No se encontro el archivo: {ruta}")
        return None

    # Valida que existan las columnas obligatorias
    if "Alumno" not in df.columns:
        raise ValueError("El CSV no tiene columna Alumno.")
    if "Alumno ID" not in df.columns:
        raise ValueError("El CSV no tiene columna Alumno ID.")

    return df


def guardar_df_clase(df, archivo):
    # Guarda el dataframe `df` como CSV en la ruta de la clase
    ruta = ruta_clase(archivo)
    df.to_csv(ruta, index=False, encoding=ENCODING_CSV)


# ========= Entrada y validación de notas =========
def pedir_float_o_vacio(prompt, minimo, maximo):
    # Pide un número flotante dentro del rango [minimo, maximo] o acepta cadena vacía
    while True:
        s = input(prompt).strip().replace(",", ".")  # permite coma decimal y la normaliza
        if s == "":
            return None  # vacío significa no introducir nota
        try:
            valor = float(s)  # intenta convertir a float
            if valor < minimo or valor > maximo:
                print(f"Debe estar entre {minimo} y {maximo}.")
                continue
            return valor  # valor válido
        except ValueError:
            print("Ingrese un número válido o deje en blanco.")


# ========= Gestión de alumnos y notas =========
def seleccionar_clase():
    # Muestra las clases existentes y permite seleccionar una por número
    archivos = listar_csv_clases()
    if not archivos:
        print(" No hay clases aún. Cree una con 'Crear nueva clase'.")
        return None
    print("\n=== Clases disponibles ===")
    for i, f in enumerate(archivos, start=1):
        print(f"{i}. {f}")
    try:
        idx = int(input("Seleccione una clase por número: ").strip())
        if 1 <= idx <= len(archivos):
            return archivos[idx - 1]
    except ValueError:
        pass
    print("Selección inválida.")
    return None


def materias_de_df(df):
    # Devuelve la lista de columnas que representan materias en el dataframe
    materias = []
    for c in df.columns:
        if c not in ("Alumno ID", "Alumno"):
            materias.append(c)
    return materias


def agregar_o_actualizar_notas():
    # Flujo para agregar un nuevo alumno o actualizar las notas existentes
    print("\n=== Cargar/actualizar notas de una clase ===")
    archivo = seleccionar_clase()
    if not archivo:
        return

    df = cargar_df_clase(archivo)
    materias = materias_de_df(df)
    if not materias:
        print("No hay materias en este CSV. Cree la clase de nuevo con materias.")
        return

    print("\nInstrucciones:")
    print("- Puede agregar un alumno nuevo o actualizar uno existente.")
    print("- Deje en blanco una nota para conservar el valor actual o para no cargarla aún.")
    print(f"- Rango de notas permitido: {MIN_NOTA} a {MAX_NOTA}.")

    while True:
        print("\n--- Alumno ---")
        alumno_id = input("Alumno ID: ").strip()  # id opcional del alumno
        while True:
            alumno = input("Nombre y apellido del alumno: ").strip()  # nombre obligatorio
            if not alumno:
                print(" El nombre es obligatorio.")
            else:
                break

        # Busca si el alumno ya existe por ID o por nombre (insensible a mayúsculas)
        idx_exist = None
        if alumno_id:
            coincidencia = df.index[(df["Alumno ID"].astype(str) == alumno_id)]
            if len(coincidencia) > 0:
                idx_exist = coincidencia[0]
        if idx_exist is None:
            coincidencia = df.index[(df["Alumno"].astype(str).str.lower() == alumno.lower())]
            if len(coincidencia) > 0:
                idx_exist = coincidencia[0]

        if idx_exist is None:
            # Si no existe, crea una fila nueva con valores vacíos (pd.NA)
            nueva = {c: pd.NA for c in df.columns}
            nueva["Alumno ID"] = alumno_id if alumno_id else pd.NA
            nueva["Alumno"] = alumno
            for m in materias:
                nueva[m] = pd.NA
            df = pd.concat([df, pd.DataFrame([nueva])], ignore_index=True)
            idx = df.index[-1]
            print(f"Alumno agregado: {alumno}")
        else:
            # Si existe, obtenemos el índice para actualizar
            idx = idx_exist
            print(f"Actualizando alumno existente: {df.loc[idx, 'Alumno']}")

        # Cargar/actualizar materias: pide nota por cada materia
        for m in materias:
            actual = df.at[idx, m]
            muestra = f" (actual: {actual})" if pd.notna(actual) else ""
            val = pedir_float_o_vacio(f"   Nota en '{m}'{muestra}: ", MIN_NOTA, MAX_NOTA)
            if val is not None:
                df.at[idx, m] = val

        # Guardar cambios en el CSV
        guardar_df_clase(df, archivo)
        print("💾 Cambios guardados.")

        otra = input("¿Desea cargar/actualizar otro alumno? (s/n): ").strip().lower()
        if otra != "s":
            break


# ========= Promedios y gráficos =========
def promedios_por_alumno(df):
    # Calcula el promedio por alumno ignorando valores NaN
    materias = materias_de_df(df)
    if not materias:
        raise ValueError("No hay materias para calcular promedios.")

    # Convertir materias a numérico (forzar errores a NaN), por si hay celdas con texto
    df_num = df.copy()
    for m in materias:
        df_num[m] = pd.to_numeric(df_num[m], errors="coerce")

    # Promedio por alumno (ignorando NaN)
    promedios = df_num[materias].mean(axis=1, skipna=True)
    out = df_num[["Alumno ID", "Alumno"]].copy()
    out["Promedio General"] = promedios
    # Filtrar alumnos sin ninguna nota (promedio NaN)
    out = out[pd.notna(out["Promedio General"]) ]
    return out


def graficar_boxplot_promedios(df_promedios, nombre_clase):
    # Dibuja y guarda un boxplot con los promedios generales
    plt.figure(figsize=(8, 5))
    sns.boxplot(x=df_promedios["Promedio General"], color="#4C72B0")  # caja
    sns.stripplot(x=df_promedios["Promedio General"], color="#DD8452", alpha=0.7)  # puntos

    plt.title(f"Distribución de promedios generales - {nombre_clase}")
    plt.xlabel("Promedio general (todas las materias)")
    plt.tight_layout()

    # Guardar imagen en la carpeta de clases
    asegurar_carpeta_clases()
    salida = os.path.join(CARPETA_CLASES, f"{os.path.splitext(nombre_clase)[0]}_boxplot_promedios.png")
    plt.savefig(salida, dpi=150)
    print(f"🖼️  Gráfico guardado en: {salida}")
    plt.show()


def graficar_barras_promedios(df_promedios, nombre_clase):
    # Dibuja barras con el promedio general por alumno y una línea del promedio de la clase
    df_plot = df_promedios.sort_values("Promedio General", ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_plot, x="Alumno", y="Promedio General")

    # Línea del promedio de la clase (del promedio de promedios)
    promedio_clase = df_plot["Promedio General"].mean()
    plt.axhline(promedio_clase, color="red", linestyle="--", alpha=0.7, label=f"Promedio de la clase: {promedio_clase:.2f}")

    plt.title(f"Promedio general por alumno - {nombre_clase}")
    plt.xlabel("Alumno")
    plt.ylabel("Promedio general (todas las materias)")
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()

    # Guardar imagen
    asegurar_carpeta_clases()
    salida = os.path.join(CARPETA_CLASES, f"{os.path.splitext(nombre_clase)[0]}_barras_promedios.png")
    plt.savefig(salida, dpi=150)
    print(f"Gráfico guardado en: {salida}")
    plt.show()


def ver_graficos_clase():
    # Interfaz para seleccionar una clase y mostrar opciones de gráficos
    print("\n=== Ver gráficos de una clase ===")
    archivo = seleccionar_clase()
    if not archivo:
        return

    df = cargar_df_clase(archivo)
    try:
        df_prom = promedios_por_alumno(df)
    except ValueError as e:
        print(f"  {e}")
        return

    if df_prom.empty:
        print("  No hay promedios para graficar (cargue algunas notas).")
        return

    print("Opciones de gráfico:")
    print("1) Boxplot de promedios generales (distribución)")
    print("2) Barras del promedio general por alumno")
    op = input("Elija una opción (1/2): ").strip()

    if op == "1":
        graficar_boxplot_promedios(df_prom, archivo)
    elif op == "2":
        graficar_barras_promedios(df_prom, archivo)
    else:
        print("  Opción inválida.")


# ========= Menú principal =========
def listar_clases():
    # Muestra los nombres de los archivos CSV disponibles
    archivos = listar_csv_clases()
    if not archivos:
        print("ℹ️  No hay clases aún.")
        return
    print("\n=== Clases (archivos CSV) ===")
    for f in archivos:
        print(f"- {f}")


def menu():
    # Menú interactivo principal del programa
    asegurar_carpeta_clases()
    while True:
        print("\n================= MENÚ =================")
        print("1) Crear nueva clase (CSV) con materias")
        print("2) Listar clases existentes")
        print("3) Cargar/actualizar notas de una clase")
        print("4) Ver gráficos de una clase (boxplot o barras)")
        print("0) Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            crear_csv_clase()
        elif opcion == "2":
            listar_clases()
        elif opcion == "3":
            agregar_o_actualizar_notas()
        elif opcion == "4":
            ver_graficos_clase()
        elif opcion == "0":
            print("¡Hasta luego!")
            break
        else:
            print("  Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    # Ejecuta el menú si se invoca el script directamente
    try:
        menu()
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario. Saliendo…")
        sys.exit(0)
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk

# Variables globales para almacenar la carpeta seleccionada y los archivos encontrados
carpeta_seleccionada = None
archivos_encontrados = []

# Función para seleccionar una carpeta
def seleccionar_carpeta():
    global carpeta_seleccionada
    carpeta_seleccionada = filedialog.askdirectory()
    if carpeta_seleccionada:
        combobox_carpeta.set(carpeta_seleccionada)  # Actualizar el valor del Combobox
        actualizar_lista_archivos()

# Función para actualizar la lista de archivos
def actualizar_lista_archivos():
    global carpeta_seleccionada, archivos_encontrados
    if not carpeta_seleccionada:
        messagebox.showerror("Error", "Primero selecciona una carpeta.")
        return
    
    texto_busqueda = entry_busqueda.get()
    archivos_encontrados = obtener_archivos_recursivamente(carpeta_seleccionada)
    lista_archivos.delete(0, tk.END)  # Limpiar la lista de archivos previos
    for archivo in archivos_encontrados:
        if texto_busqueda.lower() in os.path.basename(archivo).lower():
            lista_archivos.insert(tk.END, os.path.basename(archivo))
    mostrar_boton_todos()

# Función para obtener todos los archivos de forma recursiva en una carpeta
def obtener_archivos_recursivamente(carpeta):
    archivos = []
    for ruta_carpeta, _, archivos_en_carpeta in os.walk(carpeta):
        for archivo in archivos_en_carpeta:
            ruta_archivo = os.path.join(ruta_carpeta, archivo)
            if es_imagen(ruta_archivo):
                archivos.append(ruta_archivo)
    return archivos

# Función para verificar si un archivo es una imagen
def es_imagen(archivo):
    extensiones_permitidas = [".jpg", ".jpeg", ".png", ".gif"]
    return any(archivo.lower().endswith(extension) for extension in extensiones_permitidas)

# Función para mostrar una imagen seleccionada
def mostrar_imagen(event):
    seleccionado = lista_archivos.curselection()
    if seleccionado:
        archivo_seleccionado = archivos_encontrados[seleccionado[0]]
        imagen = Image.open(archivo_seleccionado)
        imagen = imagen.resize((300, 300))
        imagen = ImageTk.PhotoImage(imagen)
        panel_imagen.config(image=imagen)
        panel_imagen.image = imagen

# Función para mostrar todos los archivos cuando se presiona el botón "Mostrar Todos"
def mostrar_todos():
    global carpeta_seleccionada
    if not carpeta_seleccionada:
        messagebox.showerror("Error", "Primero selecciona una carpeta.")
        return
    
    actualizar_lista_archivos()

# Variable global para el botón "Mostrar Todos"
btn_mostrar_todos = None

# Función para mostrar o ocultar el botón "Mostrar Todos"
def mostrar_boton_todos():
    global btn_mostrar_todos
    if not btn_mostrar_todos:
        btn_mostrar_todos = ttk.Button(frame_busqueda, text="⬅", command=mostrar_todos, style="Custom.TButton")
    btn_mostrar_todos.pack(side=tk.LEFT, padx=5)

# Función para convertir la imagen actual de Tkinter a una imagen de Pillow
def imagen_actual_to_pillow(imagen_actual):
    imagen_actual = imagen_actual.copy()  # Crear una copia de la imagen para evitar problemas de referencia
    imagen_actual = imagen_actual.convert('RGB')  # Convertir la imagen a modo RGB
    return imagen_actual

# Función para descargar la imagen actual
def descargar_imagen():
    seleccionado = lista_archivos.curselection()
    if seleccionado:
        archivo_seleccionado = archivos_encontrados[seleccionado[0]]
        imagen_actual = Image.open(archivo_seleccionado)
        imagen_pillow = imagen_actual_to_pillow(imagen_actual)
        ubicacion_descarga = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Archivos PNG", ".png"), ("Todos los archivos", ".*")])
        if ubicacion_descarga:
            imagen_pillow.save(ubicacion_descarga)

# Función para refrescar
def refrescar():
    print("Refrescar")

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Buscar y Mostrar Archivo")

# Crear la barra de menú
barra_menu = tk.Menu(ventana)
ventana.config(menu=barra_menu)

# Opción "Archivo" en la barra de menú
menu_archivo = tk.Menu(barra_menu, tearoff=0)
barra_menu.add_cascade(label="Archivo", menu=menu_archivo)
menu_archivo.add_command(label="Seleccionar Carpeta", command=seleccionar_carpeta)
menu_archivo.add_command(label="Refrescar", command=refrescar)

# Frame para el menú
menu_frame = tk.Frame(ventana)
menu_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=50)

# Combobox para seleccionar carpeta
combobox_carpeta = ttk.Combobox(menu_frame, width=50)
combobox_carpeta.pack(pady=10)
combobox_carpeta.bind("<<ComboboxSelected>>", lambda event: actualizar_lista_archivos())

# Barra de búsqueda
frame_busqueda = tk.Frame(menu_frame)
frame_busqueda.pack(pady=5)
label_busqueda = tk.Label(frame_busqueda, text="Buscar:")
label_busqueda.pack(side=tk.LEFT)
entry_busqueda = tk.Entry(frame_busqueda)
entry_busqueda.pack(side=tk.LEFT, padx=5)

# Lista para mostrar nombres de archivos
lista_archivos = tk.Listbox(menu_frame, width=50)
lista_archivos.pack(pady=10)
lista_archivos.bind('<<ListboxSelect>>', mostrar_imagen)

# Panel para mostrar la imagen seleccionada
panel_imagen = tk.Label(menu_frame)
panel_imagen.pack(pady=10)

# Botón para descargar la imagen
btn_descargar = ttk.Button(menu_frame, text="Descargar", command=descargar_imagen)
btn_descargar.pack(pady=5)

# Mostrar el botón de "Mostrar Todos" inicialmente
mostrar_boton_todos()

ventana.mainloop()

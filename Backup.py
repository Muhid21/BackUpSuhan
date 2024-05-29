import os
import zipfile
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

def crear_copia_seguridad(origen, destino, nombre):
    if not os.path.exists(origen):
        messagebox.showerror("Error", f"¡La carpeta de origen no existe!")
        return

    fecha = datetime.now().strftime('%Y%m%d_%H%M%S')
    nombre_zip = f'{nombre}_{fecha}.zip'
    ruta_zip = os.path.join(destino, nombre_zip)

    try:
        with zipfile.ZipFile(ruta_zip, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, _, files in os.walk(origen):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, origen)
                    zip_file.write(file_path, relative_path)
        messagebox.showinfo("Éxito", f'Copia de seguridad creada en:\n{ruta_zip}')
    except Exception as e:
        messagebox.showerror("Error", f'¡Hubo un error al crear la copia de seguridad: {e}')

def seleccionar_carpeta(label):
    ruta = filedialog.askdirectory()
    if ruta:
        label.delete(0, tk.END)
        label.insert(0, ruta)

def iniciar_copia_seguridad():
    origen = entrada_origen.get()
    destino = entrada_destino.get()
    nombre = entrada_nombre.get()
    if not nombre:
        messagebox.showerror("Error", "¡Por favor, ingresa un nombre para la copia de seguridad!")
        return
    crear_copia_seguridad(origen, destino, nombre)

ventana = tk.Tk()
ventana.title("Copia de Seguridad en ZIP")

tk.Label(ventana, text="Carpeta de Origen:").grid(row=0, column=0, padx=10, pady=5)
entrada_origen = tk.Entry(ventana, width=50)
entrada_origen.grid(row=0, column=1, padx=10, pady=5)
boton_origen = tk.Button(ventana, text="Seleccionar", command=lambda: seleccionar_carpeta(entrada_origen))
boton_origen.grid(row=0, column=2, padx=10, pady=5)

tk.Label(ventana, text="Carpeta de Destino:").grid(row=1, column=0, padx=10, pady=5)
entrada_destino = tk.Entry(ventana, width=50)
entrada_destino.grid(row=1, column=1, padx=10, pady=5)
boton_destino = tk.Button(ventana, text="Seleccionar", command=lambda: seleccionar_carpeta(entrada_destino))
boton_destino.grid(row=1, column=2, padx=10, pady=5)

tk.Label(ventana, text="Nombre del Archivo:").grid(row=2, column=0, padx=10, pady=5)
entrada_nombre = tk.Entry(ventana, width=50)
entrada_nombre.grid(row=2, column=1, padx=10, pady=5)

boton_iniciar = tk.Button(ventana, text="Iniciar Copia de Seguridad", command=iniciar_copia_seguridad)
boton_iniciar.grid(row=3, columnspan=3, padx=10, pady=20)

ventana.mainloop()



import os
import zipfile
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

def crear_copia_seguridad_zip(origen, destino, nombre):
    if not os.path.exists(origen):
        messagebox.showerror("Error", f"El directorio de origen '{origen}' no existe.")
        return

    fecha_actual = datetime.now().strftime('%Y%m%d_%H%M%S')
    nombre_zip = f'{nombre}_{fecha_actual}.zip'
    ruta_zip = os.path.join(destino, nombre_zip)

    try:
        with zipfile.ZipFile(ruta_zip, 'w', zipfile.ZIP_DEFLATED) as archivo_zip:
            for carpeta_raiz, _, archivos in os.walk(origen):
                for archivo in archivos:
                    ruta_completa = os.path.join(carpeta_raiz, archivo)
                    ruta_relativa = os.path.relpath(ruta_completa, origen)
                    archivo_zip.write(ruta_completa, ruta_relativa)
        messagebox.showinfo("Éxito", f'Copia de seguridad ZIP creada exitosamente en: {ruta_zip}')
    except Exception as e:
        messagebox.showerror("Error", f'Error al crear la copia de seguridad: {e}')

def seleccionar_origen():
    ruta_origen = filedialog.askdirectory()
    if ruta_origen:
        entrada_origen.delete(0, tk.END)
        entrada_origen.insert(0, ruta_origen)

def seleccionar_destino():
    ruta_destino = filedialog.askdirectory()
    if ruta_destino:
        entrada_destino.delete(0, tk.END)
        entrada_destino.insert(0, ruta_destino)

def iniciar_copia_seguridad():
    origen = entrada_origen.get()
    destino = entrada_destino.get()
    nombre = entrada_nombre.get().strip()
    if not nombre:
        messagebox.showerror("Error", "El nombre de la copia de seguridad no puede estar vacío.")
        return
    crear_copia_seguridad_zip(origen, destino, nombre)

# Configuración de la interfaz gráfica
ventana = tk.Tk()
ventana.title("Copia de Seguridad en ZIP")

tk.Label(ventana, text="Carpeta de Origen:").grid(row=0, column=0, padx=10, pady=10)
entrada_origen = tk.Entry(ventana, width=50)
entrada_origen.grid(row=0, column=1, padx=10, pady=10)
btn_origen = tk.Button(ventana, text="Seleccionar", command=seleccionar_origen)
btn_origen.grid(row=0, column=2, padx=10, pady=10)

tk.Label(ventana, text="Carpeta de Destino:").grid(row=1, column=0, padx=10, pady=10)
entrada_destino = tk.Entry(ventana, width=50)
entrada_destino.grid(row=1, column=1, padx=10, pady=10)
btn_destino = tk.Button(ventana, text="Seleccionar", command=seleccionar_destino)
btn_destino.grid(row=1, column=2, padx=10, pady=10)

tk.Label(ventana, text="Nombre de la Copia de Seguridad:").grid(row=2, column=0, padx=10, pady=10)
entrada_nombre = tk.Entry(ventana, width=50)
entrada_nombre.grid(row=2, column=1, padx=10, pady=10)

btn_iniciar = tk.Button(ventana, text="Iniciar Copia de Seguridad", command=iniciar_copia_seguridad)
btn_iniciar.grid(row=3, columnspan=3, padx=10, pady=20)

ventana.mainloop()

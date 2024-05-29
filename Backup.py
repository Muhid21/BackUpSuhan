import os
import zipfile
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import cgi

class BackupHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/backup":
            form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST'})
            origen = form.getvalue("origen")
            destino = form.getvalue("destino")
            nombre = form.getvalue("nombre").strip()
            
            if not origen or not destino or not nombre:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Todos los campos son obligatorios.")
                return
            
            try:
                crear_copia_seguridad_zip(origen, destino, nombre)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Copia de seguridad creada exitosamente.')
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f'Error al crear la copia de seguridad: {e}'.encode('utf-8'))

def crear_copia_seguridad_zip(origen, destino, nombre):
    if not os.path.exists(origen):
        raise FileNotFoundError(f"El directorio de origen '{origen}' no existe.")

    fecha_actual = datetime.now().strftime('%Y%m%d_%H%M%S')
    nombre_zip = f'{nombre}_{fecha_actual}.zip'
    ruta_zip = os.path.join(destino, nombre_zip)

    with zipfile.ZipFile(ruta_zip, 'w', zipfile.ZIP_DEFLATED) as archivo_zip:
        for carpeta_raiz, _, archivos in os.walk(origen):
            for archivo in archivos:
                ruta_completa = os.path.join(carpeta_raiz, archivo)
                ruta_relativa = os.path.relpath(ruta_completa, origen)
                archivo_zip.write(ruta_completa, ruta_relativa)

def run(server_class=HTTPServer, handler_class=BackupHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Servidor corriendo en el puerto {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()

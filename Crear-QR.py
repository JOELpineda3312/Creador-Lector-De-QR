import qrcode
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser
import threading

# Máximo de caracteres permitidos
MAX_CHARACTERS = 2973

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de QR Futurista")
        self.root.geometry("578x600")
        self.root.config(bg="#0f0f0f")
        
        self.img = None  # Inicializar variable para la imagen QR
        self.color_var = tk.StringVar(value="#000000")  # Color predeterminado negro

        # Crear un canvas y scrollbar
        self.canvas = tk.Canvas(self.root, bg="#0f0f0f")
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#0f0f0f")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Empaquetar el canvas y el scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Título
        self.titulo = tk.Label(self.scrollable_frame, text="Generador de QR", font=("Helvetica", 24), fg="#00ff00", bg="#0f0f0f")
        self.titulo.pack(pady=20)

        # Área para ingresar texto
        self.entrada_texto = tk.Text(self.scrollable_frame, height=10, width=50, font=("Helvetica", 14), fg="#00ff00", bg="#333333", insertbackground="#00ff00")
        self.entrada_texto.pack(pady=10)
        self.entrada_texto.bind("<KeyRelease>", self.actualizar_conteo_caracteres)

        # Etiqueta para mostrar el conteo de caracteres
        self.etiqueta_caracteres = tk.Label(self.scrollable_frame, text=f"Caracteres: 0 / {MAX_CHARACTERS}", font=("Helvetica", 12), fg="#00ff00", bg="#0f0f0f")
        self.etiqueta_caracteres.pack(pady=5)

        # Botón para elegir color
        self.boton_color = tk.Button(self.scrollable_frame, text="Elegir Color", font=("Helvetica", 16), bg="#444444", fg="#00ff00", activebackground="#222222", activeforeground="#00ff00", command=self.elegir_color)
        self.boton_color.pack(pady=10)

        # Muestra de color seleccionado
        self.color_muestra = tk.Label(self.scrollable_frame, text="Color Seleccionado:", font=("Helvetica", 14), fg="#00ff00", bg="#0f0f0f")
        self.color_muestra.pack(pady=5)
        self.color_muestra.config(bg=self.color_var.get())

        # Botón para generar el QR
        self.boton_generar = tk.Button(self.scrollable_frame, text="Generar QR", font=("Helvetica", 16), bg="#444444", fg="#00ff00", activebackground="#222222", activeforeground="#00ff00", command=self.generar_qr_en_hilo)
        self.boton_generar.pack(pady=20)

        # Etiqueta para mostrar la imagen del QR generado
        self.etiqueta_imagen = tk.Label(self.scrollable_frame, bg="#0f0f0f")
        self.etiqueta_imagen.pack(pady=20)

        # Botón para ver el QR
        self.boton_ver_qr = tk.Button(self.scrollable_frame, text="Ver QR", font=("Helvetica", 16), bg="#444444", fg="#00ff00", activebackground="#222222", activeforeground="#00ff00", command=self.ver_qr, state=tk.DISABLED)
        self.boton_ver_qr.pack(pady=10)

        # Botón para guardar el QR
        self.boton_guardar = tk.Button(self.scrollable_frame, text="Guardar QR", font=("Helvetica", 16), bg="#444444", fg="#00ff00", activebackground="#222222", activeforeground="#00ff00", command=self.guardar_qr, state=tk.DISABLED)
        self.boton_guardar.pack(pady=10)

    # Función para generar el código QR (en el hilo secundario)
    def generar_qr(self):
        texto = self.entrada_texto.get("1.0", tk.END).strip()  # Obtener texto completo

        if not texto:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un texto.")
            return

        # Mostrar que el QR está en proceso de creación
        self.etiqueta_imagen.config(text="Generando QR...")

        try:
            # Generar el código QR
            qr = qrcode.QRCode(
                version=None,  # Autoajustar tamaño según contenido
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(texto)
            qr.make(fit=True)

            # Crear la imagen QR y almacenar la imagen original
            self.img = qr.make_image(fill_color=self.color_var.get(), back_color="white")  # Asegúrate de que el color se aplique aquí
            self.img = self.img.convert("RGBA")  # Convertir a formato RGBA

            # Mostrar el QR generado en la ventana
            img_tk = ImageTk.PhotoImage(self.img.resize((200, 200)))  # Redimensionar para mostrar en la ventana

            self.etiqueta_imagen.config(image=img_tk)
            self.etiqueta_imagen.image = img_tk
            self.etiqueta_imagen.config(text="")  # Limpiar el texto "Generando QR..."

            # Habilitar los botones de guardar y ver
            self.boton_guardar.config(state=tk.NORMAL)
            self.boton_ver_qr.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el QR: {str(e)}")

    # Función para iniciar el hilo de generación de QR
    def generar_qr_en_hilo(self):
        # Crear un hilo para evitar que la interfaz se congele
        hilo = threading.Thread(target=self.generar_qr)
        hilo.start()

    # Función para elegir color
    def elegir_color(self):
        color_seleccionado = colorchooser.askcolor(title="Seleccione el color para el QR")
        if color_seleccionado[1]:  # Si se seleccionó un color
            self.color_var.set(color_seleccionado[1])
            self.color_muestra.config(bg=color_seleccionado[1])  # Actualizar muestra de color

    # Función para guardar el QR generado
    def guardar_qr(self):
        try:
            archivo_guardado = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if archivo_guardado:
                # Guardar la imagen del QR
                self.img.save(archivo_guardado)  # Guardar la imagen del QR
                messagebox.showinfo("Éxito", f"Código QR guardado en: {archivo_guardado}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el QR: {str(e)}")

    # Función para actualizar el conteo de caracteres
    def actualizar_conteo_caracteres(self, event=None):
        texto = self.entrada_texto.get("1.0", tk.END).strip()
        caracteres_actuales = len(texto)
        self.etiqueta_caracteres.config(text=f"Caracteres: {caracteres_actuales} / {MAX_CHARACTERS}")

    # Función para ver el QR en una nueva ventana
    def ver_qr(self):
        if self.etiqueta_imagen.image:
            ventana_qr = tk.Toplevel(self.root)
            ventana_qr.title("Código QR Generado")
            ventana_qr.geometry("300x300")
            ventana_qr.config(bg="#0f0f0f")
            
            # Mostrar la imagen del QR en la nueva ventana
            etiqueta_qr = tk.Label(ventana_qr, image=self.etiqueta_imagen.image, bg="#0f0f0f")
            etiqueta_qr.pack(pady=20)

            # Botón para cerrar la ventana
            boton_cerrar = tk.Button(ventana_qr, text="Cerrar", command=ventana_qr.destroy, bg="#444444", fg="#00ff00")
            boton_cerrar.pack(pady=10)

# Crear la ventana principal
ventana = tk.Tk()
app = App(ventana)

# Iniciar la ventana
ventana.mainloop()

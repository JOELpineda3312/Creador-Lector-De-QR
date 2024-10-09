import tkinter as tk
from tkinter import filedialog, messagebox, Text
from PIL import Image, ImageTk
from pyzbar.pyzbar import decode
import webbrowser

# Función para leer el código QR
def leer_qr():
    archivo_imagen = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

    if archivo_imagen:
        try:
            img = Image.open(archivo_imagen)
            img_tk = ImageTk.PhotoImage(img.resize((200, 200)))

            etiqueta_imagen.config(image=img_tk)
            etiqueta_imagen.image = img_tk

            datos_qr = decode(img)

            if datos_qr:
                resultado_qr = datos_qr[0].data.decode('utf-8')
                procesar_resultado(resultado_qr)
            else:
                messagebox.showwarning("Advertencia", "No se encontró un código QR en la imagen.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer la imagen: {str(e)}")
    else:
        messagebox.showwarning("Advertencia", "No se seleccionó ninguna imagen.")

# Función para procesar el resultado del QR
def procesar_resultado(resultado):
    cuadro_resultado.delete(1.0, tk.END)  # Limpiar resultados previos

    if resultado.startswith("http://") or resultado.startswith("https://"):
        # Si es un enlace
        cuadro_resultado.insert(tk.END, f"Enlace: {resultado}")
        cuadro_resultado.tag_configure("link", foreground="blue", underline=True)
        cuadro_resultado.insert(tk.END, "\nHaga clic aquí para abrir el enlace.")
        cuadro_resultado.tag_add("link", 0.0, tk.END)
        cuadro_resultado.bind("<Button-1>", lambda e: webbrowser.open(resultado))

    elif resultado.isdigit() and len(resultado) >= 10:
        # Si es un número de teléfono (suponiendo que son 10 dígitos)
        cuadro_resultado.insert(tk.END, f"Número de teléfono: {resultado}")
        cuadro_resultado.bind("<Button-1>", lambda e: webbrowser.open(f"tel:{resultado}"))

    else:
        # Si es texto
        cuadro_resultado.insert(tk.END, resultado)
        if len(resultado) > 50:  # Comprobar si el texto tiene más de 50 caracteres
            if messagebox.askyesno("Exportar", "El texto es extenso. ¿Desea exportarlo como .txt?"):
                exportar_texto(resultado)

# Función para exportar texto a .txt
def exportar_texto(texto):
    archivo_guardado = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if archivo_guardado:
        with open(archivo_guardado, 'w') as f:
            f.write(texto)
        messagebox.showinfo("Éxito", f"Texto exportado a: {archivo_guardado}")

# Crear la ventana principal futurista para el lector de QR
ventana = tk.Tk()
ventana.title("Lector de QR Futurista")
ventana.geometry("500x500")
ventana.config(bg="#0f0f0f")

# Título con estilo de IA
titulo = tk.Label(ventana, text="QR Reader AI", font=("Helvetica", 24), fg="#00ff00", bg="#0f0f0f")
titulo.pack(pady=20)

# Botón para cargar imagen y leer QR
boton_cargar = tk.Button(ventana, text="Cargar Imagen y Leer QR", font=("Helvetica", 16), bg="#444444", fg="#00ff00", activebackground="#222222", activeforeground="#00ff00", command=leer_qr)
boton_cargar.pack(pady=20)

# Mostrar la imagen cargada
etiqueta_imagen = tk.Label(ventana, bg="#0f0f0f")
etiqueta_imagen.pack(pady=20)

# Cuadro de texto donde se mostrará el resultado del QR
cuadro_resultado = Text(ventana, height=10, width=40, font=("Helvetica", 14), fg="#00ff00", bg="#333333", insertbackground="#00ff00")
cuadro_resultado.pack(pady=20)

ventana.mainloop()

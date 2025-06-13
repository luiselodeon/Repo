import tkinter as tk
from PIL import Image, ImageTk
import Portada
import Programa_principal
from pathlib import Path

class Instrucciones:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Instrucciones")
        self.ventana.geometry("1920x1080+200+1")
        self.ventana.state("zoomed")
        self.raiz = Path(__file__).parent.resolve()

        # Canvas grande con la imagen de fondo
        self.canvasFondo = tk.Canvas(self.ventana, width=1920, height=1080, bg="grey")
        self.canvasFondo.pack(fill="both", expand=True)

        self.fondo = Image.open(self.raiz / "imagenes" / "FondoLot.png")
        self.fondoResized = self.fondo.resize((1545, 800))
        self.fondoTK = ImageTk.PhotoImage(self.fondoResized)
        self.canvasFondo.create_image(0, 0, anchor="nw", image=self.fondoTK)

        # Canvas blanco (800x400) con Scrollbar
        self.frame_canvas = tk.Frame(self.ventana, bg="white", width=800, height=400)
        self.frame_canvas.place(x=380, y=200)  # Centrar el Canvas en la pantalla

        # Crear Canvas dentro del frame para que tenga scrollbar
        self.canvas = tk.Canvas(self.frame_canvas, width=800, height=400, bg="white")
        self.scrollbar = tk.Scrollbar(self.frame_canvas, orient="vertical", command=self.canvas.yview)

        # Configurar el canvas y la scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Frame que contendrá el contenido desplazable
        self.frame_contenido = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((415, 0), window=self.frame_contenido, anchor="n")

        self.instrucciones = Image.open(self.raiz / "imagenes" / "InstruccionesLotFinalFinal.jpg")
        self.instruccionesTk = ImageTk.PhotoImage(self.instrucciones)

        self.labelImagen = tk.Label(self.frame_contenido, image=self.instruccionesTk, bg="white")
        self.labelImagen.pack(pady=10)

        # Agregar contenido al frame_contenido
        '''for i in range(30):  # Simulación de muchos textos para probar el scroll
            tk.Label(self.frame_contenido, text=f"Instrucción {i+1}", bg="white", font=("Arial", 12)).pack(pady=5)'''

        # Actualizar el área de desplazamiento
        self.frame_contenido.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        #  Botones
        port_path = self.raiz / "imagenes" / "Portada.png"
        self.img_port = tk.PhotoImage(file=str(port_path))
        self.img_port_resized = self.img_port.subsample(10, 10)
        self.btn_portada = tk.Button(self.ventana, image=self.img_port_resized, command=self.abrir_portada, bg = "#B2B2B2", fg = "white")
        self.btn_portada.place(x=1200, y=720)

        jugar_path = self.raiz / "imagenes" / "Jugar.png"
        self.img_jugar = tk.PhotoImage(file=str(jugar_path))
        self.img_jugar_resized = self.img_jugar.subsample(10, 10)
        self.btn_codigo = tk.Button(self.ventana, image=self.img_jugar_resized, command=self.abrir_programa, bg="#00CC47", fg="white")
        self.btn_codigo.place(x=1275, y=720)

        salir_path = self.raiz / "imagenes" / "Salir.png"
        self.img_salir = tk.PhotoImage(file=str(salir_path))
        self.img_salir_resized = self.img_salir.subsample(10, 10)
        self.img_salir = tk.PhotoImage(file=str(salir_path))
        self.btn_salir = tk.Button(self.ventana, image=self.img_salir_resized, command=lambda: ventana.quit(), bg="#F55757", fg="white")
        self.btn_salir.place(x=1360, y=720)

        # Configurar el scroll con la rueda del mouse
        self.canvas.bind("<Configure>", self.actualizar_scroll)
        self.canvas.bind_all("<MouseWheel>", self.scroll_con_rueda)

    def actualizar_scroll(self, event):
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def scroll_con_rueda(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def abrir_portada(self):
        self.ventana.destroy()
        n_ventana = tk.Toplevel()
        Portada.Portada(n_ventana)

    def abrir_programa(self):        
        self.ventana.destroy()
        n_ventana = tk.Toplevel()
        Programa_principal.Loteria(n_ventana)

'''if __name__ == "__main__":    
    ventana = tk.Tk()
    app = Instrucciones(ventana)
    ventana.mainloop()'''

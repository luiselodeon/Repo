import tkinter as tk
from PIL import Image, ImageTk
import Instrucciones
import Programa_principal
from pathlib import Path
import pygame

# Este es el main
class Portada:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Portada")
        self.ventana.geometry("1920x1080+200+1")  # Ajustar la posición de la ventana (lo que dice +300+1 es dónde aparecerá la ventana)
        self.ventana.state("zoomed")
        self.raiz = Path(__file__).parent.resolve()

        # Inicializa pygame y la música
        pygame.mixer.init()
        pygame.mixer.music.load(self.raiz / "audio" / "56fondo.mp3.mp3")  
        pygame.mixer.music.play(-1)  # Reproduce la música en bucle

        self.canvas = tk.Canvas(self.ventana, width=1920, height=1080)
        self.canvas.pack()

        self.portada = Image.open(self.raiz / "imagenes" / "PortadaLot.png")
        self.portadaResized = self.portada.resize((1545, 800))
        self.portadaTK = ImageTk.PhotoImage(self.portadaResized)

        self.canvas.create_image(0, 0, anchor="nw", image=self.portadaTK)

        # Creación de textos en el canvas
        textos = [
            (770, 270, "Proyecto Intersemestral", 18),
            (770, 300, "Fecha de entrega: 10 de marzo 2025", 18),
            (770, 330, "Universidad Anáhuac Querétaro", 18),
            (770, 360, "Portada Principal", 18),
            (770, 390, "Integrantes del equipo:", 14),
            (770, 420, "Luis Alberto Arias Llaguno - ID: 00483701", 12),
            (770, 450, "Jose Yael Bejar Jiménez - ID: 00482719", 12),
            (770, 480, "David Ceballos Mata - ID: 00476577", 12),
            (770, 510, "Estructura de datos", 18),
            (770, 540, "Profesor: Roberto Trejo", 18),
            (770, 570, "Lotería Mexicana", 14),
        ]

        for x, y, text, font_size in textos:
            self.canvas.create_text(x, y, text=text, font=("Arial", font_size), anchor="center")

        # Imagen de los integrantes
        self.foto_original = Image.open(self.raiz / "imagenes" / "fotointegrantes.png")
        self.foto_resized = self.foto_original.resize((300, 200))
        self.foto_Tk = ImageTk.PhotoImage(self.foto_resized)

        self.label_foto = tk.Label(self.ventana, image=self.foto_Tk, bg="white")
        self.label_foto.image = self.foto_Tk
        self.label_foto.place(x=1100, y=340)

        # Botones
        instr_path = self.raiz / "imagenes" / "Instrucciones.png"
        self.img_instr = tk.PhotoImage(file=str(instr_path))
        self.img_instr_resized = self.img_instr.subsample(10, 10)
        self.btn_instrucciones = tk.Button(self.ventana, image=self.img_instr_resized, command=self.abrir_instrucciones, bg="#46ADF4", fg="white")
        self.btn_instrucciones.place(x=1200, y=720)

        jugar_path = self.raiz / "imagenes" / "Jugar.png"
        self.img_jugar = tk.PhotoImage(file=str(jugar_path))
        self.img_jugar_resized = self.img_jugar.subsample(10, 10)
        self.btn_codigo = tk.Button(self.ventana, image=self.img_jugar_resized, command=self.abrir_programa, bg="#00CC47", fg="white")
        self.btn_codigo.place(x=1270, y=720)

        salir_path = self.raiz / "imagenes" / "Salir.png"
        self.img_salir = tk.PhotoImage(file=str(salir_path))
        self.img_salir_resized = self.img_salir.subsample(10, 10)
        self.btn_salir = tk.Button(self.ventana, image=self.img_salir_resized, command=lambda: ventana.quit(), bg="#F55757", fg="white")
        self.btn_salir.place(x=1360, y=720)
    
    def abrir_instrucciones(self):
        self.ventana.withdraw()
        n_ventana = tk.Toplevel(self.ventana)
        Instrucciones.Instrucciones(n_ventana)
    
    def abrir_programa(self):        
        self.ventana.withdraw()
        n_ventana = tk.Toplevel(self.ventana)
        Programa_principal.Loteria(n_ventana)

if __name__ == "__main__":    
    ventana = tk.Tk()
    app = Portada(ventana)
    ventana.mainloop()
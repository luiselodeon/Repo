import tkinter as tk
from PIL import Image, ImageTk
import Teoría_Grafos
import Teoría_Redes
import Dibujar_Grafo
import Referencias
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
        """
        pygame.mixer.init()
        pygame.mixer.music.load(self.raiz / "audio" / "club_fondo.mp3")  
        pygame.mixer.music.play(-1)  # Reproduce la música en bucle
        """

        self.canvas = tk.Canvas(self.ventana, width=1920, height=1080)
        self.canvas.pack()

        self.portada = Image.open(self.raiz / "imagenes" / "Portada_Principal.png")
        self.portadaResized = self.portada.resize((1545, 800))
        self.portadaTK = ImageTk.PhotoImage(self.portadaResized)

        self.canvas.create_image(0, 0, anchor="nw", image=self.portadaTK)

        # Creación de textos en el canvas
        textos = [
            (770, 210, "Proyecto Final: Red CPM", 32),
            (770, 250, "Fecha de entrega: 7 de mayo 2025", 16),
            (770, 280, "Universidad Anáhuac Querétaro", 16),
            (770, 310, "Estructura de datos", 16),
            (770, 340, "Profesor: Roberto Trejo", 16),            
            (770, 630, "Integrantes del equipo:", 14),
            (770, 660, "Luis Alberto Arias Llaguno  ID: 00483701", 14),
            (770, 690, "Jose Yael Bejar Jiménez     ID: 00482719", 14),
            (770, 720, "David Ceballos Mata            ID: 00476577", 14),                        
        ]

        for x, y, text, font_size in textos:
            self.canvas.create_text(x, y, text=text, font=("Arial", font_size), anchor="center", fill="white")

        # Imagen de los integrantes
        self.foto_original = Image.open(self.raiz / "imagenes" / "fotointegrantes.png")
        self.foto_resized = self.foto_original.resize((300, 200))
        self.foto_Tk = ImageTk.PhotoImage(self.foto_resized)

        self.label_foto = tk.Label(self.ventana, image=self.foto_Tk, bg="white")
        self.label_foto.image = self.foto_Tk
        self.label_foto.place(x=1100, y=340)
       
        # Botones  
        redes_path = self.raiz / "imagenes" / "btn_Redes.png"
        self.img_redes = tk.PhotoImage(file=str(redes_path))
        self.img_redes_resized = self.img_redes.subsample(10, 10)
        self.btn_redes = tk.Button(self.ventana, image=self.img_redes_resized, command=self.abrir_redes, bg="#33acff", fg="white")
        self.btn_redes.place(x=1110, y=720)
        tk.Label(self.ventana, text = "Redes", font=("Arial", 12), anchor="center").place(x=1115, y=690)
        
        grafos_path = self.raiz / "imagenes" / "btn_Grafos.png"
        self.img_grafos = tk.PhotoImage(file=str(grafos_path))
        self.img_grafos_resized = self.img_grafos.subsample(10, 10)
        self.btn_grafos = tk.Button(self.ventana, image=self.img_grafos_resized, command=self.abrir_grafos, bg="#00CC47", fg="white")
        self.btn_grafos.place(x=1190, y=720)
        tk.Label(self.ventana, text = "Grafos", font=("Arial", 12), anchor="center").place(x=1199, y=690)

        ref_path = self.raiz / "imagenes" / "btn_Referencias.png"
        self.img_ref = tk.PhotoImage(file=str(ref_path))
        self.img_ref_resized = self.img_ref.subsample(10, 10)
        self.btn_ref = tk.Button(self.ventana, image=self.img_ref_resized, command=self.abrir_referencias, bg="#ffd03b", fg="white")
        self.btn_ref.place(x=1295, y=720)
        tk.Label(self.ventana, text = "Referencias", font=("Arial", 12), anchor="center").place(x=1270, y=690)
        
        dib_graf_path = self.raiz / "imagenes" / "btn_dibujar_grafo.png"
        self.img_dib_graf = tk.PhotoImage(file=str(dib_graf_path))
        self.img_dib_graf_resized = self.img_dib_graf.subsample(10, 10)
        self.btn_dib_graf = tk.Button(self.ventana, image=self.img_dib_graf_resized, command=self.abrir_dibujo_grafo, bg="#fe3179", fg="white")
        self.btn_dib_graf.place(x=1380, y=720)
        tk.Label(self.ventana, text = "Dibujar", font=("Arial", 12), anchor="center").place(x=1377, y=690)

        salir_path = self.raiz / "imagenes" / "btn_Salir.png"
        self.img_salir = tk.PhotoImage(file=str(salir_path))
        self.img_salir_resized = self.img_salir.subsample(10, 10)
        self.btn_salir = tk.Button(self.ventana, image=self.img_salir_resized, command=lambda: ventana.quit(), bg="#F55757", fg="white")
        self.btn_salir.place(x=1450, y=720)
                        
    
    def abrir_dibujo_grafo(self):        
        self.ventana.withdraw()
        n_ventana = tk.Toplevel(self.ventana)
        Dibujar_Grafo.Dibujo(n_ventana)
        
    def abrir_redes(self):
        self.ventana.withdraw()
        n_ventana = tk.Toplevel(self.ventana)
        Teoría_Redes.Redes(n_ventana)
        
    def abrir_grafos(self):
        self.ventana.withdraw()
        n_ventana = tk.Toplevel(self.ventana)
        Teoría_Grafos.Grafos(n_ventana)
        
    def abrir_referencias(self):
        self.ventana.withdraw()
        n_ventana = tk.Toplevel(self.ventana)
        Referencias.Referencias(n_ventana)

if __name__ == "__main__":    
    ventana = tk.Tk()
    app = Portada(ventana)
    ventana.mainloop()
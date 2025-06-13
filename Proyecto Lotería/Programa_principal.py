import tkinter as tk
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox
import time
import random
import winsound
import Portada
import Instrucciones
from pathlib import Path
import pygame
pygame.mixer.init()

class Carta:
    def __init__(self, nombre, imagen, audio):
        self.nombre = nombre
        self.imagen = imagen
        self.audio = audio

    def reproducir_audio(self):
        """Reproduce el archivo de audio correspondiente al nombre de la carta."""
        try:
            pygame.mixer.music.load(self.audio)
            pygame.mixer.music.play()
        except pygame.error as e:
            print(f"Error al reproducir el audio: {e}")

class Jugador:
    def __init__(self, nombre, cartas_disponibles):
        self.nombre = nombre
        self.tablero = random.sample(cartas_disponibles, 16)
        self.cartas_sacadas = 0  
        self.imagenes = []
        self.victorias = 0

class Loteria:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Lotería Nacional")
        self.ventana.geometry("1920x1080+200+1") 
        self.ventana.state("zoomed")
        self.raiz = Path(__file__).parent.resolve()

        # Fondo
        self.canvasFondo = tk.Canvas(self.ventana, width=1920, height=1080, bg="grey")
        self.canvasFondo.pack(fill="both", expand=True)

        self.fondo = Image.open(self.raiz / "imagenes" / "PortadaLot.png")
        self.fondoResized = self.fondo.resize((1545, 800))
        self.fondoTK = ImageTk.PhotoImage(self.fondoResized)
        self.canvasFondo.create_image(0, 0, anchor="nw", image=self.fondoTK)

        # Área de juego
        self.frame_canvas = tk.Frame(self.ventana, bg="white", width=1480, height=650)
        self.frame_canvas.place(x=30, y=60)  # Posición en la ventana

        self.canvas = tk.Canvas(self.frame_canvas, width=1480, height=650, bg="white")
        self.canvas.pack()

        # Frame para los elementos de jugadores
        self.frame_jugadores = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((740, 50), window=self.frame_jugadores, anchor="n")

        # Variables
        self.num_jugadores = 2
        self.max_jugadores = 5
        self.min_jugadores = 2
        self.entradas_jugadores = []

        # UI de selección de jugadores
        self.crear_ui_jugadores()

        # Botones
        instr_path = self.raiz / "imagenes" / "Instrucciones.png"
        self.img_instr = tk.PhotoImage(file=str(instr_path))
        self.img_instr_resized = self.img_instr.subsample(10, 10)
        self.btn_instrucciones = tk.Button(self.ventana, image=self.img_instr_resized, command=self.abrir_instrucciones, bg="#46ADF4", fg="white")
        self.btn_instrucciones.place(x=1200, y=720)

        port_path = self.raiz / "imagenes" / "Portada.png"
        self.img_port = tk.PhotoImage(file=str(port_path))
        self.img_port_resized = self.img_port.subsample(10, 10)
        self.btn_portada = tk.Button(self.ventana, image=self.img_port_resized, command=self.abrir_portada, bg = "#B2B2B2", fg = "white")
        self.btn_portada.place(x=1270, y=720)

        salir_path = self.raiz / "imagenes" / "Salir.png"
        self.img_salir = tk.PhotoImage(file=str(salir_path))
        self.img_salir_resized = self.img_salir.subsample(10, 10)
        self.btn_salir = tk.Button(self.ventana, image=self.img_salir_resized, command=lambda: ventana.quit(), bg="#F55757", fg="white")
        self.btn_salir.place(x=1360, y=720)

        # Cargar la imagen del "frijol"
        self.img_frijol = Image.open(self.raiz / "imagenes" / "frijol.png").resize((45, 45))  
        self.img_frijol_tk = ImageTk.PhotoImage(self.img_frijol)

        self.cartas = [
            Carta("El gallo", self.raiz / "imagenes" / "01Gallo.jpg", self.raiz / "audio" / "01Gallo.mp3"),
            Carta("El diablito", self.raiz / "imagenes" / "02Diablito.jpg", self.raiz / "audio" / "02Diablito.mp3"),
            Carta("La dama", self.raiz / "imagenes" / "03Dama.jpg", self.raiz / "audio" / "03Dama.mp3"),
            Carta("El catrín", self.raiz / "imagenes" / "04Catrin.jpg", self.raiz / "audio" / "04Catrin.mp3"),
            Carta("El paraguas", self.raiz / "imagenes" / "05Paraguas.jpg", self.raiz / "audio" / "05Paraguas.mp3"),
            Carta("La sirena", self.raiz / "imagenes" / "06Sirena.jpg", self.raiz / "audio" / "06Sirena.mp3"),
            Carta("La escalera", self.raiz / "imagenes" / "07Escalera.jpg", self.raiz / "audio" / "07Escalera.mp3"),
            Carta("La botella", self.raiz / "imagenes" / "08Botella.jpg", self.raiz / "audio" / "08Botella.mp3"),
            Carta("El barril", self.raiz / "imagenes" / "09Barril.jpg", self.raiz / "audio" / "09Barril.mp3"),
            Carta("El árbol", self.raiz / "imagenes" / "10Arbol.jpg", self.raiz / "audio" / "10Arbol.mp3"),
            Carta("El melón", self.raiz / "imagenes" / "11Melon.jpg", self.raiz / "audio" / "11Melon.mp3"),
            Carta("El valiente", self.raiz / "imagenes" / "12Valiente.jpg", self.raiz / "audio" / "12Valiente.mp3"),
            Carta("El gorrito", self.raiz / "imagenes" / "13Gorrito.jpg", self.raiz / "audio" / "13Gorrito.mp3"),
            Carta("La muerte", self.raiz / "imagenes" / "14Muerte.jpg", self.raiz / "audio" / "14Muerte.mp3"),
            Carta("La pera", self.raiz / "imagenes" / "15Pera.jpg", self.raiz / "audio" / "15Pera.mp3"),
            Carta("La bandera", self.raiz / "imagenes" / "16Bandera.jpg", self.raiz / "audio" / "16Bandera.mp3"),
            Carta("El bandolón", self.raiz / "imagenes" / "17Bandolon.jpg", self.raiz / "audio" / "17Bandolon.mp3"),
            Carta("El violoncello", self.raiz / "imagenes" / "18Violoncello.jpg", self.raiz / "audio" / "18Violoncello.mp3"),
            Carta("La garza", self.raiz / "imagenes" / "19Garza.jpg", self.raiz / "audio" / "19Garza.mp3"),
            Carta("El pájaro", self.raiz / "imagenes" / "20Pajaro.jpg", self.raiz / "audio" / "20Pajaro.mp3"),
            Carta("La mano", self.raiz / "imagenes" / "21Mano.jpg", self.raiz / "audio" / "21Mano.mp3"),
            Carta("La bota", self.raiz / "imagenes" / "22Bota.jpg", self.raiz / "audio" / "22Bota.mp3"),
            Carta("La luna", self.raiz / "imagenes" / "23Luna.jpg", self.raiz / "audio" / "23Luna.mp3"),
            Carta("El cotorro", self.raiz / "imagenes" / "24Cotorro.jpg", self.raiz / "audio" / "24Cotorro.mp3"),
            Carta("El borracho", self.raiz / "imagenes" / "25Borracho.jpg", self.raiz / "audio" / "25Borracho.mp3"),
            Carta("El negrito", self.raiz / "imagenes" / "26Negrito.jpg", self.raiz / "audio" / "26Negrito.mp3"),
            Carta("El corazón", self.raiz / "imagenes" / "27Corazon.jpg", self.raiz / "audio" / "27Corazon.mp3"),
            Carta("La sandía", self.raiz / "imagenes" / "28Sandia.jpg", self.raiz / "audio" / "28Sandia.mp3"),
            Carta("El tambor", self.raiz / "imagenes" / "29Tambor.jpg", self.raiz / "audio" / "29Tambor.mp3"),
            Carta("El camarón", self.raiz / "imagenes" / "30Camaron.jpg", self.raiz / "audio" / "30Camaron.mp3"),
            Carta("Las jaras", self.raiz / "imagenes" / "31Jaras.jpg", self.raiz / "audio" / "31Jaras.mp3"),
            Carta("El músico", self.raiz / "imagenes" / "32Musico.jpg", self.raiz / "audio" / "32Musico.mp3"),
            Carta("La araña", self.raiz / "imagenes" / "33Arana.jpg", self.raiz / "audio" / "33Araña.mp3"),
            Carta("El soldado", self.raiz / "imagenes" / "34Soldado.jpg", self.raiz / "audio" / "34Soldado.mp3"),
            Carta("La estrella", self.raiz / "imagenes" / "35Estrella.jpg", self.raiz / "audio" / "35Estrella.mp3"),
            Carta("El cazo", self.raiz / "imagenes" / "36Cazo.jpg", self.raiz / "audio" / "36Cazo.mp3"),
            Carta("El mundo", self.raiz / "imagenes" / "37Mundo.jpg", self.raiz / "audio" / "37Mundo.mp3"),
            Carta("El apache", self.raiz / "imagenes" / "38Apache.jpg", self.raiz / "audio" / "38Apache.mp3"),
            Carta("El nopal", self.raiz / "imagenes" / "39Nopal.jpg", self.raiz / "audio" / "39Nopal.mp3"),
            Carta("El alacrán", self.raiz / "imagenes" / "40Alacran.jpg", self.raiz / "audio" / "40Alacran.mp3"),
            Carta("La rosa", self.raiz / "imagenes" / "41Rosa.jpg", self.raiz / "audio" / "41Rosa.mp3"),
            Carta("La calavera", self.raiz / "imagenes" / "42Calavera.jpg", self.raiz / "audio" / "42Calavera.mp3"),
            Carta("La campana", self.raiz / "imagenes" / "43Campana.jpg", self.raiz / "audio" / "43Campana.mp3"),
            Carta("El cantarito", self.raiz / "imagenes" / "44Cantarito.jpg", self.raiz / "audio" / "44Cantarito.mp3"),
            Carta("El venado", self.raiz / "imagenes" / "45Venado.jpg", self.raiz / "audio" / "45Venado.mp3"),
            Carta("El sol", self.raiz / "imagenes" / "46Sol.jpg", self.raiz / "audio" / "46Sol.mp3"),
            Carta("La corona", self.raiz / "imagenes" / "47Corona.jpg", self.raiz / "audio" / "47Corona.mp3"),
            Carta("La chalupa", self.raiz / "imagenes" / "48Chalupa.jpg", self.raiz / "audio" / "48Chalupa.mp3"),
            Carta("El pino", self.raiz / "imagenes" / "49Pino.jpg", self.raiz / "audio" / "49Pino.mp3"),
            Carta("El pescado", self.raiz / "imagenes" / "50Pescado.jpg", self.raiz / "audio" / "50Pescado.mp3"),
            Carta("La palma", self.raiz / "imagenes" / "51Palma.jpg", self.raiz / "audio" / "51Palma.mp3"),
            Carta("La maceta", self.raiz / "imagenes" / "52Maceta.jpg", self.raiz / "audio" / "52Maceta.mp3"),
            Carta("El arpa", self.raiz / "imagenes" / "53Arpa.jpg", self.raiz / "audio" / "53Arpa.mp3"),
            Carta("La rana", self.raiz / "imagenes" / "54Rana.jpg", self.raiz / "audio" / "54Rana.mp3")
        ]


    def crear_ui_jugadores(self):
        """Crea o actualiza la interfaz de selección de jugadores."""
        for widget in self.frame_jugadores.winfo_children():
            widget.destroy()

        # Label de número de jugadores
        tk.Label(self.frame_jugadores, text="Número de jugadores:", font=("Arial", 14), bg="white").grid(row=0, column=0, columnspan=3, pady=10)

        # Botón para disminuir
        btn_menos = tk.Button(self.frame_jugadores, text="-", font=("Arial", 14), width=3, command=self.disminuir_jugadores)
        btn_menos.grid(row=1, column=0)

        # Mostrar número de jugadores
        self.label_num_jugadores = tk.Label(self.frame_jugadores, text=str(self.num_jugadores), font=("Arial", 14), bg="white")
        self.label_num_jugadores.grid(row=1, column=1, padx=10)

        # Botón para aumentar
        btn_mas = tk.Button(self.frame_jugadores, text="+", font=("Arial", 14), width=3, command=self.aumentar_jugadores)
        btn_mas.grid(row=1, column=2)

        # Campos para los nombres
        self.entradas_jugadores = []
        for i in range(self.num_jugadores):
            tk.Label(self.frame_jugadores, text=f"Jugador {i + 1}:", font=("Arial", 12), bg="white").grid(row=i + 2, column=0, padx=10, pady=5, sticky="w")
            entrada = tk.Entry(self.frame_jugadores, font=("Arial", 12), width=20)
            entrada.grid(row=i + 2, column=1, columnspan=2, padx=10, pady=5)
            self.entradas_jugadores.append(entrada)

        # Botón "JUGAR"
        self.btn_jugar = tk.Button(self.frame_jugadores, text="JUGAR", font=("Arial", 14), bg="green", fg="white", command=self.iniciar_juego)
        self.btn_jugar.grid(row=self.num_jugadores + 2, column=0, columnspan=3, pady=20)

    def iniciar_juego(self):
        # Crear jugadores con tableros
        nombres = [entrada.get() if entrada.get() else f"Jugador {i+1}" for i, entrada in enumerate(self.entradas_jugadores)]
        self.jugadores = [Jugador(nombre, self.cartas) for nombre in nombres]

        for jugador in self.jugadores:
            print(f"Tablero de {jugador.nombre}:")
            for i, carta in enumerate(jugador.tablero):
                print(f"{i+1}. {carta.nombre}")  
            print("-" * 30)  


        """Oculta la interfaz de selección de jugadores y prepara los tableros."""
        self.frame_jugadores.destroy()
        self.dibujar_tableros()

    def dibujar_tableros(self):
        self.canvas.delete("victoria_texto")
        self.canvas.delete("ganador")

        """Distribuye y dibuja los tableros de los jugadores en el canvas."""
        posiciones = {
            2: [(320, 320), (890, 320)],
            3: [(200, 320), (550, 320), (900, 320)],
            4: [(200, 335), (450, 335), (700, 335), (950, 335)],
            5: [(320, 180), (900, 180), (620, 320), (320, 490), (900, 490)],
        }

        # Tamaño dinámico de cartas
        if self.num_jugadores in [2,3]:
            carta_ancho, carta_alto = 75, 112
            resta_y = 265
            suma_y = 255
        elif self.num_jugadores in [4]:
            carta_ancho, carta_alto = 50, 75
            resta_y = 190
            suma_y = 180
        else:
            carta_ancho, carta_alto = 35, 52
            resta_y = 135         
            suma_y = 130

        espacio_x = carta_ancho + 5
        espacio_y = carta_alto + 5


        for i, jugador in enumerate(self.jugadores):
            x_centro, y_centro = posiciones[self.num_jugadores][i]

            # Dibujar nombre
            self.canvas.create_text(x_centro, y_centro - resta_y, text=jugador.nombre, font=("Arial", 14, "bold"), fill="black")

            # Dibujar victorias
            self.canvas.create_text(x_centro, y_centro + suma_y, text=f"Victorias: {jugador.victorias}", font=("Arial", 14, "bold"), fill="black", tags="victoria_texto")

            # Dibujar tablero 4x4
            x_inicio = x_centro - (2 * espacio_x)
            y_inicio = y_centro - (2 * espacio_y)

            # Almacenar las referencias de las imágenes en una lista dentro del jugador
            jugador.imagenes = []

            for fila in range(4):
                for col in range(4):
                    carta = jugador.tablero[fila * 4 + col]
                    img = Image.open(carta.imagen).resize((carta_ancho, carta_alto))
                    img_tk = ImageTk.PhotoImage(img)
                    
                    # Guardar la imagen en la lista del jugador
                    jugador.imagenes.append(img_tk)
                    
                    # Dibujar la imagen en el canvas
                    self.canvas.create_image(x_inicio + col * espacio_x, y_inicio + fila * espacio_y, image=img_tk, anchor="nw")

        self.img_carta_atras = Image.open(self.raiz / "imagenes" / "cartaAtras.jpg").resize((200, 300))
        self.img_carta_atras_tk = ImageTk.PhotoImage(self.img_carta_atras)

        # Dibujar la imagen en el canvas
        self.canvas.create_image(1275, 325, image=self.img_carta_atras_tk, anchor="center")

        # Crear un Frame para los botones
        frame_botones = tk.Frame(self.canvas, bg="white")

        # Botón "CARTA"
        self.btn_carta = tk.Button(frame_botones, text="CARTA", font=("Arial", 14), bg="green", fg="white", command=self.sacar_carta)
        self.btn_carta.grid(row=0, column=0, pady=10)  

        # Botón "JUGAR DE NUEVO"
        self.btn_jugar_nuevo = tk.Button(frame_botones, text="JUGAR DE NUEVO", font=("Arial", 14), bg="blue", fg="white", command=self.jugar_de_nuevo)
        self.btn_jugar_nuevo.grid(row=1, column=0, pady=5)  

        # Insertar el Frame con los botones en el canvas
        self.canvas.create_window(1275, 535, window=frame_botones)

    def sacar_carta(self):
        """Saca una carta aleatoria del mazo y la muestra en el área de cartas."""
        if not self.cartas:  # Si ya no hay cartas disponibles
            print("No quedan más cartas en el mazo.")
            return  

        # Elegir una carta aleatoria y eliminarla del mazo
        carta = random.choice(self.cartas)
        self.cartas.remove(carta)

        # Reproducir el audio de la carta
        carta.reproducir_audio()

        # Cargar la nueva imagen con el mismo tamaño
        img_carta = Image.open(carta.imagen).resize((200, 300))
        self.img_carta_actual_tk = ImageTk.PhotoImage(img_carta)  # Guardar referencia

        # Eliminar la imagen anterior (carta volteada) y dibujar la nueva carta
        self.canvas.delete("carta_actual")  # Elimina cualquier carta anterior
        self.canvas.create_image(1275, 325, image=self.img_carta_actual_tk, anchor="center", tags="carta_actual")

        if self.num_jugadores in [2,3]:
            carta_ancho, carta_alto = 75, 112
        elif self.num_jugadores in [4]:
            carta_ancho, carta_alto = 50, 75
        else:
            carta_ancho, carta_alto = 35, 52

        espacio_x = carta_ancho + 5
        espacio_y = carta_alto + 5

        ganadores = []

        # Comprobar si la carta sacada está en los tableros de los jugadores
        for jugador in self.jugadores:
            for fila in range(4):
                for col in range(4):
                    carta_tablero = jugador.tablero[fila * 4 + col]
                    if carta_tablero.nombre == carta.nombre:
                        # Si la carta está en el tablero, colocar el "frijol"
                        x_centro, y_centro = self.obtener_posicion_tablero(jugador)
                        x_inicio = x_centro - (2 * espacio_x)
                        y_inicio = y_centro - (2 * espacio_y)
                        self.canvas.create_image(x_inicio + col * espacio_x + carta_ancho / 2, 
                            y_inicio + fila * espacio_y + carta_alto / 2, 
                            image=self.img_frijol_tk, 
                            anchor="center")
                        
                        # Incrementar el conteo de cartas sacadas del jugador
                        jugador.cartas_sacadas += 1

                        # Verificar si el jugador ha ganado (tiene todas las 16 cartas)
                        if jugador.cartas_sacadas == 16:
                            ganadores.append(jugador)
                            self.btn_carta.config(state="disabled")  # Deshabilitar el botón de sacar carta
                            #return  
        if ganadores:
            if len(ganadores) > 1:
                self.canvas.create_text(1275, 130, text=f"¡Hay empate!", font=("Arial", 20, "bold"), fill="green", tags="ganador")
            else:
                self.canvas.create_text(1275, 130, text=f"¡{ganadores[0].nombre} ha ganado!", font=("Arial", 20, "bold"), fill="green", tags="ganador")

            for jugador in ganadores:
                jugador.victorias += 1  # Aumentar victorias de los ganadores

            # Reproducir música de victoria
            self.reproducir_musica_victoria()

    def reproducir_musica_victoria(self):
        """Reproduce la música de victoria."""
        try:
            pygame.mixer.music.load(self.raiz / "audio" / "55musicavictoria.mp3")
            pygame.mixer.music.play()
        except pygame.error as e:
            print(f"Error al reproducir la música de victoria: {e}")

    def jugar_de_nuevo(self):
        """Reinicia el juego sin borrar las victorias."""
        # Reiniciar el estado de los tableros y la baraja
        self.cartas = [
            Carta("El gallo", self.raiz / "imagenes" / "01Gallo.jpg", self.raiz / "audio" / "01Gallo.mp3"),
            Carta("El diablito", self.raiz / "imagenes" / "02Diablito.jpg", self.raiz / "audio" / "02Diablito.mp3"),
            Carta("La dama", self.raiz / "imagenes" / "03Dama.jpg", self.raiz / "audio" / "03Dama.mp3"),
            Carta("El catrín", self.raiz / "imagenes" / "04Catrin.jpg", self.raiz / "audio" / "04Catrin.mp3"),
            Carta("El paraguas", self.raiz / "imagenes" / "05Paraguas.jpg", self.raiz / "audio" / "05Paraguas.mp3"),
            Carta("La sirena", self.raiz / "imagenes" / "06Sirena.jpg", self.raiz / "audio" / "06Sirena.mp3"),
            Carta("La escalera", self.raiz / "imagenes" / "07Escalera.jpg", self.raiz / "audio" / "07Escalera.mp3"),
            Carta("La botella", self.raiz / "imagenes" / "08Botella.jpg", self.raiz / "audio" / "08Botella.mp3"),
            Carta("El barril", self.raiz / "imagenes" / "09Barril.jpg", self.raiz / "audio" / "09Barril.mp3"),
            Carta("El árbol", self.raiz / "imagenes" / "10Arbol.jpg", self.raiz / "audio" / "10Arbol.mp3"),
            Carta("El melón", self.raiz / "imagenes" / "11Melon.jpg", self.raiz / "audio" / "11Melon.mp3"),
            Carta("El valiente", self.raiz / "imagenes" / "12Valiente.jpg", self.raiz / "audio" / "12Valiente.mp3"),
            Carta("El gorrito", self.raiz / "imagenes" / "13Gorrito.jpg", self.raiz / "audio" / "13Gorrito.mp3"),
            Carta("La muerte", self.raiz / "imagenes" / "14Muerte.jpg", self.raiz / "audio" / "14Muerte.mp3"),
            Carta("La pera", self.raiz / "imagenes" / "15Pera.jpg", self.raiz / "audio" / "15Pera.mp3"),
            Carta("La bandera", self.raiz / "imagenes" / "16Bandera.jpg", self.raiz / "audio" / "16Bandera.mp3"),
            Carta("El bandolón", self.raiz / "imagenes" / "17Bandolon.jpg", self.raiz / "audio" / "17Bandolon.mp3"),
            Carta("El violoncello", self.raiz / "imagenes" / "18Violoncello.jpg", self.raiz / "audio" / "18Violoncello.mp3"),
            Carta("La garza", self.raiz / "imagenes" / "19Garza.jpg", self.raiz / "audio" / "19Garza.mp3"),
            Carta("El pájaro", self.raiz / "imagenes" / "20Pajaro.jpg", self.raiz / "audio" / "20Pajaro.mp3"),
            Carta("La mano", self.raiz / "imagenes" / "21Mano.jpg", self.raiz / "audio" / "21Mano.mp3"),
            Carta("La bota", self.raiz / "imagenes" / "22Bota.jpg", self.raiz / "audio" / "22Bota.mp3"),
            Carta("La luna", self.raiz / "imagenes" / "23Luna.jpg", self.raiz / "audio" / "23Luna.mp3"),
            Carta("El cotorro", self.raiz / "imagenes" / "24Cotorro.jpg", self.raiz / "audio" / "24Cotorro.mp3"),
            Carta("El borracho", self.raiz / "imagenes" / "25Borracho.jpg", self.raiz / "audio" / "25Borracho.mp3"),
            Carta("El negrito", self.raiz / "imagenes" / "26Negrito.jpg", self.raiz / "audio" / "26Negrito.mp3"),
            Carta("El corazón", self.raiz / "imagenes" / "27Corazon.jpg", self.raiz / "audio" / "27Corazon.mp3"),
            Carta("La sandía", self.raiz / "imagenes" / "28Sandia.jpg", self.raiz / "audio" / "28Sandia.mp3"),
            Carta("El tambor", self.raiz / "imagenes" / "29Tambor.jpg", self.raiz / "audio" / "29Tambor.mp3"),
            Carta("El camarón", self.raiz / "imagenes" / "30Camaron.jpg", self.raiz / "audio" / "30Camaron.mp3"),
            Carta("Las jaras", self.raiz / "imagenes" / "31Jaras.jpg", self.raiz / "audio" / "31Jaras.mp3"),
            Carta("El músico", self.raiz / "imagenes" / "32Musico.jpg", self.raiz / "audio" / "32Musico.mp3"),
            Carta("La araña", self.raiz / "imagenes" / "33Arana.jpg", self.raiz / "audio" / "33Araña.mp3"),
            Carta("El soldado", self.raiz / "imagenes" / "34Soldado.jpg", self.raiz / "audio" / "34Soldado.mp3"),
            Carta("La estrella", self.raiz / "imagenes" / "35Estrella.jpg", self.raiz / "audio" / "35Estrella.mp3"),
            Carta("El cazo", self.raiz / "imagenes" / "36Cazo.jpg", self.raiz / "audio" / "36Cazo.mp3"),
            Carta("El mundo", self.raiz / "imagenes" / "37Mundo.jpg", self.raiz / "audio" / "37Mundo.mp3"),
            Carta("El apache", self.raiz / "imagenes" / "38Apache.jpg", self.raiz / "audio" / "38Apache.mp3"),
            Carta("El nopal", self.raiz / "imagenes" / "39Nopal.jpg", self.raiz / "audio" / "39Nopal.mp3"),
            Carta("El alacrán", self.raiz / "imagenes" / "40Alacran.jpg", self.raiz / "audio" / "40Alacran.mp3"),
            Carta("La rosa", self.raiz / "imagenes" / "41Rosa.jpg", self.raiz / "audio" / "41Rosa.mp3"),
            Carta("La calavera", self.raiz / "imagenes" / "42Calavera.jpg", self.raiz / "audio" / "42Calavera.mp3"),
            Carta("La campana", self.raiz / "imagenes" / "43Campana.jpg", self.raiz / "audio" / "43Campana.mp3"),
            Carta("El cantarito", self.raiz / "imagenes" / "44Cantarito.jpg", self.raiz / "audio" / "44Cantarito.mp3"),
            Carta("El venado", self.raiz / "imagenes" / "45Venado.jpg", self.raiz / "audio" / "45Venado.mp3"),
            Carta("El sol", self.raiz / "imagenes" / "46Sol.jpg", self.raiz / "audio" / "46Sol.mp3"),
            Carta("La corona", self.raiz / "imagenes" / "47Corona.jpg", self.raiz / "audio" / "47Corona.mp3"),
            Carta("La chalupa", self.raiz / "imagenes" / "48Chalupa.jpg", self.raiz / "audio" / "48Chalupa.mp3"),
            Carta("El pino", self.raiz / "imagenes" / "49Pino.jpg", self.raiz / "audio" / "49Pino.mp3"),
            Carta("El pescado", self.raiz / "imagenes" / "50Pescado.jpg", self.raiz / "audio" / "50Pescado.mp3"),
            Carta("La palma", self.raiz / "imagenes" / "51Palma.jpg", self.raiz / "audio" / "51Palma.mp3"),
            Carta("La maceta", self.raiz / "imagenes" / "52Maceta.jpg", self.raiz / "audio" / "52Maceta.mp3"),
            Carta("El arpa", self.raiz / "imagenes" / "53Arpa.jpg", self.raiz / "audio" / "53Arpa.mp3"),
            Carta("La rana", self.raiz / "imagenes" / "54Rana.jpg", self.raiz / "audio" / "54Rana.mp3")
        ]
        
        for jugador in self.jugadores:
            jugador.cartas_sacadas = 0
            jugador.tablero = random.sample(self.cartas, 16)

        # Eliminar las imágenes de las cartas actuales en el canvas
        self.canvas.delete("carta_actual")
        
        # Redibujar los tableros
        self.dibujar_tableros()

        # Rehabilitar el botón "CARTA" si es necesario
        self.btn_carta.config(state="normal")


    def obtener_posicion_tablero(self, jugador):
            """Devuelve la posición (x, y) del tablero de un jugador."""
            posiciones = {
                2: [(320, 320), (890, 320)],
                3: [(200, 350), (550, 350), (900, 350)],
                4: [(200, 335), (450, 335), (700, 335), (950, 335)],
                5: [(320, 180), (900, 180), (620, 320), (320, 490), (900, 490)],
            }
            x_centro, y_centro = posiciones[self.num_jugadores][self.jugadores.index(jugador)]
            return x_centro, y_centro

    '''def declarar_ganador(self, jugador):
        """Declara al jugador como ganador y muestra un mensaje en el canvas."""
        self.canvas.create_text(1275, 130, text=f"¡{jugador.nombre} ha ganado!", font=("Arial", 20, "bold"), fill="green", tags="ganador")'''

    def aumentar_jugadores(self):
        """Aumenta el número de jugadores (máx. 5)."""
        if self.num_jugadores < self.max_jugadores:
            self.num_jugadores += 1
            self.label_num_jugadores.config(text=str(self.num_jugadores))
            self.crear_ui_jugadores()

    def disminuir_jugadores(self):
        """Disminuye el número de jugadores (mín. 2)."""
        if self.num_jugadores > self.min_jugadores:
            self.num_jugadores -= 1
            self.label_num_jugadores.config(text=str(self.num_jugadores))
            self.crear_ui_jugadores()
    
    # (No se elimina) Este no debería de eliminarse, es para abrir la portada
    def abrir_portada(self):
        #Cerrar la ventana actual y abrir la portada
        #self.jugar_de_nuevo()
        self.ventana.withdraw()
        n_ventana = tk.Toplevel(self.ventana)
        Portada.Portada(n_ventana)
    
    # (No se elimina) Este no debería de eliminarse, es para abrir las instrucciones
    def abrir_instrucciones(self):
        #self.jugar_de_nuevo()
        self.ventana.withdraw()
        n_ventana = tk.Toplevel(self.ventana)
        Instrucciones.Instrucciones(n_ventana)
    
    def cerrar_programa(self):        
        self.ventana.quit()
        self.ventana.destroy()

'''if __name__ == "__main__":    
    ventana = tk.Tk()
    app = Loteria(ventana)
    ventana.mainloop()'''
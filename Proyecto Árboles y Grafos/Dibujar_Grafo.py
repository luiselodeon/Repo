import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox
from pathlib import Path
import pygame
import networkx as nx
import matplotlib.pyplot as plt
import Portada
import Teoría_Grafos
import Teoría_Redes

pygame.mixer.init()

class Dibujo:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Dibujo de grafo")
        self.ventana.geometry("1920x1080+300+1")
        self.ventana.state("zoomed")
        self.raiz = Path(__file__).parent.resolve()

        # Almacena las tareas ingresadas con duración y dependencias
        self.tasks = {}

        # Fondo
        self.canvasFondo = tk.Canvas(self.ventana, width=1920, height=1080, bg="grey")
        self.canvasFondo.pack(fill="both", expand=True)
        self.fondo = Image.open(self.raiz / "imagenes" / "Portada_Dibujo.png")
        self.fondoResized = self.fondo.resize((1545, 800))
        self.fondoTK = ImageTk.PhotoImage(self.fondoResized)
        self.canvasFondo.create_image(0, 0, anchor="nw", image=self.fondoTK)

        # Área de juego (canvas interno)
        self.frame_canvas = tk.Frame(self.ventana, bg="white", width=1080, height=625)
        self.frame_canvas.place(x=230, y=40)
        self.canvas = tk.Canvas(self.frame_canvas, width=1080, height=625, bg="white")
        self.canvas.pack()

        # Entradas de texto
        tk.Label(self.ventana, text="Nombre de la Tarea:", bg="white", font=("Arial", 12)).place(x=250, y=80)
        self.nombre_tarea = tk.Entry(self.ventana, width=20, font=("Arial", 12))
        self.nombre_tarea.place(x=400, y=80)

        tk.Label(self.ventana, text="¿Cuánto va a durar la tarea? (horas)", bg="white", font=("Arial", 12)).place(x=250, y=110)
        self.duracion = tk.Entry(self.ventana, width=5, font=("Arial", 12))
        self.duracion.place(x=510, y=110)

        tk.Label(self.ventana, text="Dependencias (separadas por comas):", bg="white", font=("Arial", 12)).place(x=250, y=140)
        self.dependencias = tk.Entry(self.ventana, width=20, font=("Arial", 12))
        self.dependencias.place(x=530, y=140)

        self.tareas_guardadas = tk.Label(self.ventana, text=f"Tareas guardadas: {len(self.tasks)}",
                                         bg="white", font=("Arial", 14))
        self.tareas_guardadas.place(x=900, y=100)

        # Botones principales
        self.btn_guardar = tk.Button(self.ventana, text="Guardar Tarea", command=self.guardar, fg="black",
                                     width=12, height=2, font=("Arial", 12))
        self.btn_guardar.place(x=740, y=90)

        self.btn_editar = tk.Button(self.ventana, text="Editar Tareas", command=self.editar, fg="black",
                                    width=12, height=2, font=("Arial", 12))
        self.btn_editar.place(x=620, y=730)

        self.btn_limpiar = tk.Button(self.ventana, text="Limpiar", command=self.limpiar, fg="black",
                                     width=10, height=2, font=("Arial", 12))
        self.btn_limpiar.place(x=740, y=730)

        self.btn_dibujar = tk.Button(self.ventana, text="Dibujar Grafo", command=self.dibujar, fg="black",
                                     width=12, height=2, font=("Arial", 12))
        self.btn_dibujar.place(x=842, y=730)

        # Botones de navegación
        port_path = self.raiz / "imagenes" / "btn_Portada.png"
        self.img_port_resized = tk.PhotoImage(file=str(port_path)).subsample(10, 10)
        tk.Button(self.ventana, image=self.img_port_resized, command=self.abrir_portada,
                  bg="#B2B2B2").place(x=1220, y=720)

        redes_path = self.raiz / "imagenes" / "btn_Redes.png"
        self.img_redes_resized = tk.PhotoImage(file=str(redes_path)).subsample(10, 10)
        tk.Button(self.ventana, image=self.img_redes_resized, command=self.abrir_redes,
                  bg="#33acff").place(x=1295, y=720)
        tk.Label(self.ventana, text="Redes", font=("Arial", 12)).place(x=1300, y=690)

        grafos_path = self.raiz / "imagenes" / "btn_Grafos.png"
        self.img_grafos_resized = tk.PhotoImage(file=str(grafos_path)).subsample(10, 10)
        tk.Button(self.ventana, image=self.img_grafos_resized, command=self.abrir_grafos,
                  bg="#00CC47").place(x=1370, y=720)
        tk.Label(self.ventana, text="Grafos", font=("Arial", 12)).place(x=1379, y=690)

        salir_path = self.raiz / "imagenes" / "btn_Salir.png"
        self.img_salir_resized = tk.PhotoImage(file=str(salir_path)).subsample(10, 10)
        tk.Button(self.ventana, image=self.img_salir_resized, command=lambda: ventana.quit(),
                  bg="#F55757").place(x=1450, y=720)

        # ─── Tabla de resultados ────────────────────────────────────────────────────
        self.frame_tabla = tk.Frame(self.ventana, bg="white", bd=1, relief="sunken")                
        self.frame_tabla.place(x=230, y=200, width=1080, height=350)

        self.scroll_x = tk.Scrollbar(self.frame_tabla, orient='horizontal')
        self.scroll_y = tk.Scrollbar(self.frame_tabla, orient='vertical')
        self.scroll_x.pack(side='bottom', fill='x')
        self.scroll_y.pack(side='right', fill='y')

        cols = ('Actividad','Duración','ET','FT','LT','LF','Holgura')
        self.tree = ttk.Treeview(
            self.frame_tabla,
            columns=cols,
            show='headings',
            xscrollcommand=self.scroll_x.set,
            yscrollcommand=self.scroll_y.set
        )
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120, anchor='center')
        self.tree.pack(expand=True, fill='both')

        self.scroll_x.config(command=self.tree.xview)
        self.scroll_y.config(command=self.tree.yview)


    def guardar(self):
        nombre = self.nombre_tarea.get().strip()
        dur_str = self.duracion.get().strip()
        deps_str = self.dependencias.get().strip()
        if not nombre or not dur_str:
            messagebox.showwarning("Error", "Debes ingresar nombre y duración de la tarea.")
            return
        try:
            dur = float(dur_str)
        except ValueError:
            messagebox.showwarning("Error", "La duración debe ser un número.")
            return
        deps = [d.strip() for d in deps_str.split(',') if d.strip()]
        self.tasks[nombre] = {'duration': dur, 'deps': deps}
        self.tareas_guardadas.config(text=f"Tareas guardadas: {len(self.tasks)}")
        self.nombre_tarea.delete(0, tk.END)
        self.duracion.delete(0, tk.END)
        self.dependencias.delete(0, tk.END)

    def limpiar(self):
        self.tasks.clear()
        self.tareas_guardadas.config(text="Tareas guardadas: 0")
        self.canvas.delete("all")
        plt.close('all')
        for item in self.tree.get_children():
            self.tree.delete(item)

    def dibujar(self):
        if not self.tasks:
            messagebox.showinfo("Atención", "No hay tareas para dibujar.")
            return

        plt.close('all')
        G = nx.DiGraph()

        # Crear nodos y aristas
        for tarea, data in self.tasks.items():
            G.add_node(tarea, duration=data['duration'])
            for dep in data['deps']:
                G.add_edge(dep, tarea)

        # Forward Pass
        earliest_start = {}
        earliest_finish = {}
        for nodo in nx.topological_sort(G):
            preds = list(G.predecessors(nodo))
            earliest_start[nodo] = 0 if not preds else max(earliest_finish[p] for p in preds)
            earliest_finish[nodo] = earliest_start[nodo] + G.nodes[nodo]['duration']

        # Backward Pass
        final = max(earliest_finish.values())
        latest_finish = {}
        latest_start = {}
        for nodo in reversed(list(nx.topological_sort(G))):
            succs = list(G.successors(nodo))
            latest_finish[nodo] = final if not succs else min(latest_start[s] for s in succs)
            latest_start[nodo] = latest_finish[nodo] - G.nodes[nodo]['duration']

        # Holguras
        holguras = {n: latest_start[n] - earliest_start[n] for n in G.nodes()}

        # Llenar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        for nodo in G.nodes():
            dur = G.nodes[nodo]['duration']
            et = earliest_start[nodo]
            ft = earliest_finish[nodo]
            lt = latest_start[nodo]
            lf = latest_finish[nodo]
            hol = holguras[nodo]
            self.tree.insert(
                '',
                'end',
                values=(nodo, f"{dur}h", f"{et}h", f"{ft}h", f"{lt}h", f"{lf}h", f"{hol}h")
            )

        # Ruta crítica
        ruta_critica = [n for n in G.nodes() if holguras[n] == 0]

        # Dibujar grafo
        pos = nx.spring_layout(G, seed=28)
        plt.figure(figsize=(10, 7))
        colores_nodos = ['red' if n in ruta_critica else 'lightblue' for n in G.nodes()]
        colores_aristas = [
            'red' if u in ruta_critica and v in ruta_critica else 'gray'
            for u, v in G.edges()
        ]
        nx.draw(G, pos, with_labels=False, node_size=1500,
                node_color=colores_nodos, edge_color=colores_aristas, arrows=True)

        etiquetas = {
            n: f"{n}\nDur: {G.nodes[n]['duration']}h\nHolg: {holguras[n]}h"
            for n in G.nodes()
        }
        nx.draw_networkx_labels(G, pos, labels=etiquetas, font_size=9, font_weight='bold')

        plt.title(f"Grafo de Tareas - Ruta Crítica: {' → '.join(ruta_critica)}", fontsize=14)
        plt.axis('off')
        plt.show()

    def editar(self):
        if not self.tasks:
            messagebox.showinfo("Atención", "No hay tareas para editar.")
            return
        edit_win = tk.Toplevel(self.ventana)
        edit_win.title("Editar tareas")
        frame = tk.Frame(edit_win)
        frame.pack(padx=10, pady=10)
        tk.Label(frame, text="Nombre", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5)
        tk.Label(frame, text="Duración (h)", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=5)
        tk.Label(frame, text="Dependencias", font=("Arial", 12, "bold")).grid(row=0, column=2, padx=5)
        self.edit_entries = {}
        for idx, (tarea, data) in enumerate(self.tasks.items(), start=1):
            name_e = tk.Entry(frame, width=20)
            name_e.insert(0, tarea)
            name_e.grid(row=idx, column=0, pady=2)
            dur_e = tk.Entry(frame, width=5)
            dur_e.insert(0, str(data['duration']))
            dur_e.grid(row=idx, column=1, pady=2)
            deps_e = tk.Entry(frame, width=20)
            deps_e.insert(0, ','.join(data['deps']))
            deps_e.grid(row=idx, column=2, pady=2)
            self.edit_entries[tarea] = (name_e, dur_e, deps_e)
        tk.Button(edit_win, text="Guardar y salir", font=("Arial", 12),
                  command=lambda: self.guardar_edicion(edit_win)).pack(pady=10)

    def guardar_edicion(self, win):
        new_tasks = {}
        for orig, (name_e, dur_e, deps_e) in self.edit_entries.items():
            new_name = name_e.get().strip()
            dur_str = dur_e.get().strip()
            deps_str = deps_e.get().strip()
            if not new_name or not dur_str:
                messagebox.showwarning("Error", "Nombre y duración no pueden estar vacíos.")
                return
            try:
                dur = float(dur_str)
            except ValueError:
                messagebox.showwarning("Error", f"Duración inválida en tarea {new_name}.")
                return
            deps = [d.strip() for d in deps_str.split(',') if d.strip()]
            new_tasks[new_name] = {'duration': dur, 'deps': deps}
        self.tasks = new_tasks
        self.tareas_guardadas.config(text=f"Tareas guardadas: {len(self.tasks)}")
        win.destroy()

    def abrir_portada(self):
        self.ventana.withdraw()
        n_ventana = tk.Toplevel(self.ventana)
        Portada.Portada(n_ventana)

    def abrir_redes(self):
        self.ventana.withdraw()
        n_ventana = tk.Toplevel(self.ventana)
        # Aquí podrías instanciar Teoría_Redes si fuera necesario

    def abrir_grafos(self):
        self.ventana.withdraw()
        n_ventana = tk.Toplevel(self.ventana)
        Teoría_Grafos.Grafos(n_ventana)

"""
if __name__ == "__main__":
    ventana = tk.Tk()
    app = Dibujo(ventana)
    ventana.mainloop()
"""
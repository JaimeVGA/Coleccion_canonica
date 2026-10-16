import tkinter as tk
from tkinter import ttk

from .estilos import COLORES, configurar_estilos, crear_superficie


class VentanaResultados(tk.Toplevel):
    def __init__(self, padre, gramatica, coleccion):
        super().__init__(padre)
        self.title("Colección canónica LR(0)")
        self.geometry("1180x760")
        self.minsize(850, 560)
        self.configure(bg=COLORES["fondo"])
        configurar_estilos(self)
        self._crear(gramatica, coleccion)

    def _crear(self, gramatica, coleccion):
        panel = crear_superficie(self)
        panel.pack(fill="both", expand=True, padx=30, pady=24)
        tabla = ttk.Treeview(
            panel, columns=("operacion", "resultado"), show="headings",
        )
        tabla.heading("operacion", text="Operación")
        tabla.heading("resultado", text="Resultado")
        tabla.column("operacion", width=390, anchor="w")
        tabla.column("resultado", width=700, anchor="w")
        scroll_y = ttk.Scrollbar(panel, orient="vertical", command=tabla.yview)
        scroll_x = ttk.Scrollbar(panel, orient="horizontal", command=tabla.xview)
        tabla.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        tabla.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        panel.rowconfigure(0, weight=1)
        panel.columnconfigure(0, weight=1)
        for paso, (operacion, resultado) in enumerate(coleccion.trace, 1):
            tabla.insert("", "end", values=(f"{paso}. {operacion}", resultado))

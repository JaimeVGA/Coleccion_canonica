import tkinter as tk
from tkinter import ttk

from .estilos import COLORES, crear_superficie


class TablaEstados(tk.Frame):
    def __init__(self, padre, estados, gramatica):
        super().__init__(padre, bg=COLORES["superficie"])
        self.estados = estados
        self.gramatica = gramatica
        self._crear()

    def _crear(self):
        encabezado = tk.Frame(self, bg=COLORES["superficie"])
        encabezado.pack(fill="x", pady=(0, 8))
        tk.Label(
            encabezado, text=f"{len(self.estados)} estados LR(0)",
            font=("Segoe UI", 12, "bold"), bg=COLORES["superficie"],
            fg=COLORES["texto"],
        ).pack(side="left")
        tk.Label(
            encabezado, text="Cada fila muestra la cerradura y sus transiciones",
            font=("Segoe UI", 9), bg=COLORES["superficie"],
            fg=COLORES["secundario"],
        ).pack(side="right")

        canvas = tk.Canvas(self, bg=COLORES["superficie"], highlightthickness=0)
        scroll = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        interior = tk.Frame(canvas, bg=COLORES["superficie"])
        interior.bind(
            "<Configure>",
            lambda event: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.create_window((0, 0), window=interior, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        for indice, estado in enumerate(self.estados):
            panel = crear_superficie(interior)
            panel.pack(fill="x", pady=(0, 12), padx=(1, 8))
            titulo = f"I{indice}"
            if getattr(estado, "es_aceptacion", False):
                titulo += "  ·  ACEPTACIÓN"
            tk.Label(
                panel, text=titulo, anchor="w",
                font=("Segoe UI", 12, "bold"),
                bg=COLORES["superficie"], fg=(
                    COLORES["exito"] if getattr(estado, "es_aceptacion", False)
                    else COLORES["texto"]
                ),
            ).pack(fill="x", padx=14, pady=(11, 6))
            for elemento in sorted(estado.items, key=str):
                tk.Label(
                    panel, text=f"  {self._formatear_elemento(elemento)}", anchor="w",
                    font=("Consolas", 10), bg=COLORES["superficie_alt"],
                    fg=COLORES["texto"], padx=8, pady=3,
                ).pack(fill="x", padx=14)
            transiciones = getattr(estado, "transiciones", {})
            texto = "   ".join(
                f"{simbolo} → I{destino}" for simbolo, destino
                in sorted(transiciones.items())
            )
            tk.Label(
                panel, text="Transiciones: " + (texto or "ninguna"), anchor="w",
                font=("Segoe UI", 9, "bold"), bg=COLORES["superficie"],
                fg=COLORES["primario"], padx=14, pady=8,
            ).pack(fill="x")

    def _formatear_elemento(self, elemento):
        produccion = self.gramatica.productions[elemento.production_index]
        cuerpo = list(produccion.right)
        cuerpo.insert(elemento.dot, "•")
        derecha = " ".join(cuerpo) if cuerpo else "•"
        return f"{produccion.left} → {derecha}"

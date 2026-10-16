import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.persistencia.algoritmo_lr0 import construir_coleccion
from src.persistencia.lector_gramatica import cargar_gramatica_desde_archivo
from src.presentacion.estilos import COLORES, configurar_estilos, crear_superficie
from src.presentacion.ventana_resultados import VentanaResultados


class InterfazColeccion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Colección canónica · Analizador LR(0)")
        self.geometry("1180x760")
        self.minsize(900, 600)
        self.configure(bg=COLORES["fondo"])
        self.ruta_actual = ""
        self.gramatica = None
        self.ventana_resultados = None
        configurar_estilos(self)
        self._crear_interfaz()

    def _crear_interfaz(self):
        tk.Label(
            self, text="Analizador de colección canónica",
            font=("Segoe UI", 24, "bold"), bg=COLORES["fondo"],
            fg=COLORES["texto"],
        ).pack(anchor="w", padx=34, pady=(26, 3))
        tk.Label(
            self, text="Construye los estados LR(0) de una gramática libre de contexto aumentada.",
            font=("Segoe UI", 11), bg=COLORES["fondo"],
            fg=COLORES["secundario"],
        ).pack(anchor="w", padx=34, pady=(0, 16))

        controles = crear_superficie(self)
        controles.pack(fill="x", padx=34, pady=(0, 18))
        self.ruta_var = tk.StringVar(value="Ningún archivo seleccionado")
        tk.Label(
            controles, textvariable=self.ruta_var, anchor="w",
            font=("Segoe UI", 10), bg=COLORES["superficie"],
            fg=COLORES["secundario"],
        ).pack(side="left", fill="x", expand=True, padx=16, pady=12)
        ttk.Button(
            controles, text="Construir colección", style="Accent.TButton",
            command=self.analizar,
        ).pack(side="right", padx=(4, 8), pady=8)
        ttk.Button(
            controles, text="Cargar archivo", command=self.abrir_archivo,
        ).pack(side="right", padx=8, pady=8)
        ttk.Button(
            controles, text="Limpiar", command=self.limpiar,
        ).pack(side="right", padx=(8, 4), pady=8)

        panel = crear_superficie(self)
        panel.pack(fill="both", expand=True, padx=34, pady=(0, 14))
        tk.Label(
            panel, text="Gramática de entrada", anchor="w",
            font=("Segoe UI", 12, "bold"), bg=COLORES["superficie"],
            fg=COLORES["texto"],
        ).pack(fill="x", padx=16, pady=(14, 8))
        self.editor = tk.Text(
            panel, wrap="none", state="disabled", font=("Consolas", 10),
            bg=COLORES["superficie_alt"], fg=COLORES["texto"],
            relief="flat", padx=14, pady=12,
        )
        self.editor.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        self.estado_var = tk.StringVar(value="Listo para cargar una gramática.")
        tk.Label(
            self, textvariable=self.estado_var, anchor="w", font=("Segoe UI", 9),
            bg=COLORES["fondo"], fg=COLORES["secundario"],
        ).pack(fill="x", padx=36, pady=(0, 14))

    def abrir_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar gramática aumentada",
            filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")),
        )
        if not ruta:
            return
        try:
            self.gramatica = cargar_gramatica_desde_archivo(ruta)
        except (OSError, UnicodeError, ValueError) as error:
            messagebox.showerror("No se pudo cargar la gramática", str(error))
            return
        self.ruta_actual = ruta
        self.ruta_var.set(ruta)
        self._mostrar_gramatica()
        self.estado_var.set("Gramática cargada. Presiona «Construir colección».")

    def _mostrar_gramatica(self):
        self.editor.configure(state="normal")
        self.editor.delete("1.0", tk.END)
        with open(self.ruta_actual, encoding="utf-8") as archivo:
            self.editor.insert("1.0", archivo.read())
        self.editor.configure(state="disabled")

    def analizar(self):
        if self.gramatica is None:
            messagebox.showinfo("Gramática requerida", "Primero selecciona una gramática.")
            return
        try:
            coleccion = construir_coleccion(self.gramatica)
        except (KeyError, ValueError, RuntimeError) as error:
            messagebox.showerror("Error durante la construcción", str(error))
            return
        if self.ventana_resultados and self.ventana_resultados.winfo_exists():
            self.ventana_resultados.destroy()
        self.ventana_resultados = VentanaResultados(self, self.gramatica, coleccion)
        self.estado_var.set(f"Colección construida: {len(coleccion.estados)} estados LR(0).")

    def limpiar(self):
        self.ruta_actual = ""
        self.gramatica = None
        self.ruta_var.set("Ningún archivo seleccionado")
        self.editor.configure(state="normal")
        self.editor.delete("1.0", tk.END)
        self.editor.configure(state="disabled")
        self.estado_var.set("Listo para cargar una gramática.")


if __name__ == "__main__":
    InterfazColeccion().mainloop()

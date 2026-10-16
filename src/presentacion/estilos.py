import tkinter as tk
from tkinter import ttk

COLORES = {
    "fondo": "#ffffff",
    "superficie": "#ffffff",
    "superficie_alt": "#f8fafc",
    "texto": "#172033",
    "secundario": "#64748b",
    "primario": "#2563eb",
    "primario_hover": "#1d4ed8",
    "borde": "#dbe3ee",
    "exito": "#15803d",
    "exito_fondo": "#ecfdf3",
    "error": "#b91c1c",
}


def configurar_estilos(ventana):
    estilo = ttk.Style(ventana)
    estilo.theme_use("clam")
    estilo.configure(
        "TButton", font=("Segoe UI", 10), padding=(13, 8),
        background=COLORES["superficie"], foreground=COLORES["texto"],
        bordercolor=COLORES["borde"],
    )
    estilo.configure(
        "Accent.TButton", font=("Segoe UI", 10, "bold"), padding=(15, 9),
        background=COLORES["primario"], foreground="white", borderwidth=0,
    )
    estilo.map("Accent.TButton", background=[("active", COLORES["primario_hover"])])
    estilo.configure(
        "Treeview", background=COLORES["superficie_alt"],
        fieldbackground=COLORES["superficie_alt"], foreground=COLORES["texto"],
        rowheight=29, font=("Segoe UI", 10), bordercolor=COLORES["borde"],
    )
    estilo.configure(
        "Treeview.Heading", background="#eef2f7", foreground=COLORES["texto"],
        font=("Segoe UI", 10, "bold"), padding=8,
    )
    estilo.map(
        "Treeview", background=[("selected", COLORES["primario"])],
        foreground=[("selected", "white")],
    )
    estilo.configure("TNotebook", background=COLORES["fondo"], borderwidth=0)
    estilo.configure(
        "TNotebook.Tab", padding=(18, 10), font=("Segoe UI", 10, "bold"),
        background="#eef2f7", foreground=COLORES["secundario"],
    )
    estilo.map(
        "TNotebook.Tab", background=[("selected", COLORES["superficie"])],
        foreground=[("selected", COLORES["texto"])],
    )


def crear_superficie(padre):
    return tk.Frame(
        padre, bg=COLORES["superficie"], highlightthickness=1,
        highlightbackground=COLORES["borde"],
    )

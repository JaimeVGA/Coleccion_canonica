"""Adaptadores de persistencia y algoritmos para la interfaz."""

from .algoritmo_lr0 import construir_coleccion, cerradura, ir_a
from .lector_gramatica import cargar_gramatica_desde_archivo

__all__ = [
    "cargar_gramatica_desde_archivo",
    "construir_coleccion",
    "cerradura",
    "ir_a",
]

"""Fachada de los algoritmos LR(0) para desacoplar la interfaz."""

from .algoritmos_lr0 import closure as cerradura
from .algoritmos_lr0 import canonical_collection, construir_coleccion, ir_a

__all__ = [
    "cerradura",
    "construir_coleccion",
    "ir_a",
    "canonical_collection",
]

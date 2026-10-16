"""Modelos de la gramática y de los elementos LR(0)."""

from .modelos_lr0 import (
    CanonicalCollection,
    Grammar,
    GrammarError,
    LR0Item,
    LR0State,
    Production,
)

Gramatica = Grammar
Produccion = Production
ElementoLR0 = LR0Item
EstadoLR0 = LR0State

__all__ = [
    "CanonicalCollection",
    "Grammar",
    "GrammarError",
    "LR0Item",
    "LR0State",
    "Production",
    "Gramatica",
    "Produccion",
    "ElementoLR0",
    "EstadoLR0",
]

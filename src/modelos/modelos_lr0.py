from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping


class GrammarError(ValueError):
    """La gramática no cumple las invariantes del modelo."""


@dataclass(frozen=True, slots=True)
class Production:
    left: str
    right: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.left or not self.left.strip():
            raise GrammarError("El lado izquierdo de una producción no puede estar vacío")
        if any(not symbol or not symbol.strip() for symbol in self.right):
            raise GrammarError("Los símbolos de una producción no pueden estar vacíos")

    def __str__(self) -> str:
        return f"{self.left} → {'ε' if not self.right else ' '.join(self.right)}"


@dataclass(frozen=True, slots=True)
class Grammar:
    start_symbol: str
    terminals: frozenset[str]
    nonterminals: frozenset[str]
    productions: tuple[Production, ...]

    def __post_init__(self) -> None:
        if self.start_symbol not in self.nonterminals:
            raise GrammarError("El símbolo inicial debe ser un no terminal")
        if not self.terminals.isdisjoint(self.nonterminals):
            raise GrammarError("Terminales y no terminales deben ser disjuntos")
        if not self.productions:
            raise GrammarError("La gramática debe tener al menos una producción")
        if any(p.left not in self.nonterminals for p in self.productions):
            raise GrammarError("Toda producción debe tener un no terminal a la izquierda")
        known = self.terminals | self.nonterminals
        unknown = {s for p in self.productions for s in p.right} - known
        if unknown:
            raise GrammarError(f"Símbolos no declarados en producciones: {sorted(unknown)}")

    @classmethod
    def create(
        cls,
        start_symbol: str,
        terminals: Iterable[str],
        nonterminals: Iterable[str],
        productions: Iterable[Production],
    ) -> "Grammar":
        return cls(
            start_symbol.strip(),
            frozenset(s.strip() for s in terminals if s.strip()),
            frozenset(s.strip() for s in nonterminals if s.strip()),
            tuple(productions),
        )

    def augmented(self) -> "Grammar":
        if (
            self.productions
            and             self.productions[0].left != self.start_symbol
            and self.productions[0].right
            and self.productions[0].right[0] == self.start_symbol
        ):
            return self
        augmented_start = self.start_symbol + "'"
        while augmented_start in self.nonterminals or augmented_start in self.terminals:
            augmented_start += "'"
        return Grammar.create(
            augmented_start,
            self.terminals | {"$"},
            self.nonterminals | {augmented_start},
            (Production(augmented_start, (self.start_symbol,)),) + self.productions,
        )


@dataclass(frozen=True, order=True, slots=True)
class LR0Item:
    production_index: int
    dot: int = 0

    def advance(self) -> "LR0Item":
        return LR0Item(self.production_index, self.dot + 1)


@dataclass(frozen=True, slots=True)
class LR0State:
    index: int
    items: frozenset[LR0Item]
    transitions: Mapping[str, int]
    accepting: bool = False

    @property
    def transiciones(self) -> Mapping[str, int]:
        """Transiciones por símbolo, referidas al índice del estado destino."""
        return self.transitions

    @property
    def es_aceptacion(self) -> bool:
        return self.accepting


@dataclass(frozen=True, slots=True)
class CanonicalCollection:
    """Colección canónica LR(0) lista para ser consumida por la interfaz."""

    estados: tuple[LR0State, ...]
    grammar: Grammar
    trace: tuple[tuple[str, str], ...] = ()

    @property
    def gramatica(self) -> Grammar:
        return self.grammar

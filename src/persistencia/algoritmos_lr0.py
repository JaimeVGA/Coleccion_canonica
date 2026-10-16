from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from ..modelos.modelos_lr0 import CanonicalCollection, Grammar, LR0Item, LR0State


def _ordered_symbols(grammar: Grammar, symbols: Iterable[str]) -> list[str]:
    """Conserva el orden de aparición de los símbolos en el estado."""
    del grammar
    return list(dict.fromkeys(symbols))


def closure(grammar: Grammar, items: Iterable[LR0Item]) -> frozenset[LR0Item]:
    result = set(items)
    changed = True
    while changed:
        changed = False
        for item in tuple(result):
            production = grammar.productions[item.production_index]
            if item.dot < len(production.right):
                symbol = production.right[item.dot]
                if symbol in grammar.nonterminals:
                    for index, candidate in enumerate(grammar.productions):
                        if candidate.left == symbol and LR0Item(index) not in result:
                            result.add(LR0Item(index))
                            changed = True
    return frozenset(result)


def goto(grammar: Grammar, items: Iterable[LR0Item], symbol: str) -> frozenset[LR0Item]:
    advanced = {
        item.advance()
        for item in closure(grammar, items)
        if item.dot < len(grammar.productions[item.production_index].right)
        and grammar.productions[item.production_index].right[item.dot] == symbol
    }
    return closure(grammar, advanced) if advanced else frozenset()


ir_a = goto


def _format_items(grammar: Grammar, items: Iterable[LR0Item]) -> str:
    formatted = []
    for item in sorted(items):
        production = grammar.productions[item.production_index]
        body = list(production.right)
        body.insert(item.dot, "•")
        formatted.append(f"{production.left}→{' '.join(body) or '•'}")
    return "{" + ", ".join(formatted) + "}"


def _canonical_collection(
    grammar: Grammar,
) -> tuple[tuple[LR0State, ...], Grammar, tuple[tuple[str, str], ...]]:
    """Construye estados, transiciones deterministas y marca el estado de aceptación."""
    augmented = grammar.augmented()
    initial = closure(augmented, {LR0Item(0)})
    state_items: list[frozenset[LR0Item]] = [initial]
    state_numbers = {initial: 0}
    transitions: list[dict[str, int]] = [dict()]
    trace: list[tuple[str, str]] = [
        (
            "cerradura({" + augmented.productions[0].left
            + " → • " + augmented.start_symbol + "})",
            "I0",
        ),
        ("I0", _format_items(augmented, initial)),
    ]
    cursor = 0
    while cursor < len(state_items):
        current = state_items[cursor]
        symbols = _ordered_symbols(
            augmented,
            (
                augmented.productions[item.production_index].right[item.dot]
                for item in sorted(current)
                if item.dot < len(augmented.productions[item.production_index].right)
            ),
        )
        for symbol in symbols:
            target = goto(augmented, current, symbol)
            if target not in state_numbers:
                state_numbers[target] = len(state_items)
                state_items.append(target)
                transitions.append({})
                trace.append(
                    (f"Ir_a(I{cursor}, {symbol})",
                     (
                         f"Aceptación (I{state_numbers[target]})"
                         if LR0Item(0, len(augmented.productions[0].right)) in target
                         else f"cerradura(...) → I{state_numbers[target]}"
                     ))
                )
                trace.append(
                    (f"I{state_numbers[target]}",
                     _format_items(augmented, target))
                )
            else:
                trace.append(
                    (f"Ir_a(I{cursor}, {symbol})",
                     (
                         f"Aceptación (I{state_numbers[target]})"
                         if LR0Item(0, len(augmented.productions[0].right)) in target
                         else f"I{state_numbers[target]} (estado existente)"
                     ))
                )
            transitions[cursor][symbol] = state_numbers[target]
        cursor += 1
    states = tuple(
        LR0State(
            index,
            items,
            dict(transitions[index]),
            LR0Item(0, len(augmented.productions[0].right)) in items,
        )
        for index, items in enumerate(state_items)
    )
    return states, augmented, tuple(trace)


def canonical_collection(grammar: Grammar) -> tuple[tuple[LR0State, ...], Grammar]:
    """Compatibilidad pública: devuelve estados y gramática aumentada."""
    states, augmented, _ = _canonical_collection(grammar)
    return states, augmented


def construir_coleccion(gramatica: Grammar) -> CanonicalCollection:
    """Construye la colección LR(0) con la API estable de la interfaz."""
    estados, gramatica_aumentada, trace = _canonical_collection(gramatica)
    return CanonicalCollection(estados, gramatica_aumentada, trace)

from __future__ import annotations

import re
from pathlib import Path
from typing import TextIO

from ..modelos.modelos_lr0 import Grammar, Production


class GrammarFormatError(ValueError):
    """Error de sintaxis o validación en el archivo de gramática."""


_ARROW = re.compile(r"\s*(?:→|->)\s*")
_LABELS = {
    "inicio": "start",
    "símbolo inicial": "start",
    "simbolo inicial": "start",
    "start": "start",
    "terminales": "terminals",
    "terminals": "terminals",
    "no terminales": "nonterminals",
    "no terminales": "nonterminals",
    "nonterminals": "nonterminals",
}


def _tokens(value: str) -> list[str]:
    value = value.strip()
    if not value:
        return []
    return [part for part in re.split(r"[\s,;]+", value) if part]


def _compact_tokens(value: str, symbols: set[str]) -> list[str]:
    value = value.strip()
    if not value or value in {"ε", "e", "epsilon"}:
        return []
    if " " in value:
        return _tokens(value)
    ordered = sorted(symbols, key=lambda symbol: (-len(symbol), symbol))
    result = []
    position = 0
    while position < len(value):
        symbol = next(
            (candidate for candidate in ordered if value.startswith(candidate, position)),
            None,
        )
        if symbol is None:
            raise GrammarFormatError(
                f"No se pudo separar el cuerpo de la producción cerca de: {value[position:]}"
            )
        result.append(symbol)
        position += len(symbol)
    return result


def _label(line: str) -> tuple[str, str] | None:
    if ":" not in line:
        return None
    name, value = line.split(":", 1)
    return _LABELS.get(name.strip().lower()), value.strip()


def read_grammar_text(text: str) -> Grammar:
    """Lee el formato de la asignación, tolerando etiquetas y flechas ->/→."""
    fields: dict[str, str] = {}
    production_lines: list[tuple[int, str]] = []
    in_productions = False
    positional_header = False
    header_lines: list[str] = []
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        label = _label(line)
        if label and label[0] in {"start", "terminals", "nonterminals"}:
            fields[label[0]] = label[1]
            continue
        if line.lower().rstrip(":") in {"producciones", "productions", "reglas"}:
            in_productions = True
            continue
        if _ARROW.search(line):
            in_productions = True
            production_lines.append((number, line))
        elif in_productions:
            raise GrammarFormatError(f"Línea {number}: se esperaba una producción")
        else:
            header_lines.append(line)
            if len(header_lines) == 2:
                fields["nonterminals"] = header_lines[0]
                fields["terminals"] = header_lines[1]
                positional_header = True
                in_productions = True
            elif len(header_lines) > 2:
                raise GrammarFormatError(f"Línea {number}: encabezado inválido")

    if positional_header and production_lines:
        fields["start"] = _tokens(fields["nonterminals"])[0]

    missing = [key for key in ("start", "terminals", "nonterminals") if key not in fields]
    if missing:
        raise GrammarFormatError("Faltan campos: " + ", ".join(missing))
    productions: list[Production] = []
    declared_nonterminals = set(_tokens(fields["nonterminals"]))
    declared_terminals = set(_tokens(fields["terminals"]))
    for number, line in production_lines:
        match = _ARROW.search(line)
        assert match is not None
        left = line[: match.start()].strip()
        if not left:
            raise GrammarFormatError(f"Línea {number}: falta el lado izquierdo")
        for alternative in line[match.end() :].split("|"):
            symbols = _compact_tokens(
                alternative.replace("ε", "").strip(),
                declared_nonterminals | declared_terminals | {"$"},
            )
            productions.append(Production(left, tuple(symbols)))
    if not productions:
        raise GrammarFormatError("No se encontraron producciones")
    try:
        production_nonterminals = declared_nonterminals | {
            production.left for production in productions
        }
        production_terminals = declared_terminals | {
            symbol
            for production in productions
            for symbol in production.right
            if symbol not in production_nonterminals
        }
        return Grammar.create(
            _tokens(fields["start"])[0] if _tokens(fields["start"]) else "",
            production_terminals,
            production_nonterminals,
            productions,
        )
    except (IndexError, ValueError) as error:
        raise GrammarFormatError(str(error)) from error


def read_grammar(source: str | Path | TextIO) -> Grammar:
    if hasattr(source, "read"):
        return read_grammar_text(source.read())
    path = Path(source)
    try:
        return read_grammar_text(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise GrammarFormatError(f"No se pudo leer {path}: {error}") from error


def cargar_gramatica_desde_archivo(ruta: str | Path) -> Grammar:
    """Carga una gramática desde la ruta indicada."""
    return read_grammar(ruta)

from __future__ import annotations

import ast
import operator as op
from typing import Any


_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}


def _eval(node: ast.AST) -> float:
    if isinstance(node, ast.Num):  # type: ignore[attr-defined]
        return float(node.n)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.left), _eval(node.right))
    raise ValueError("Unsupported expression")


async def run(params: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    expression = str(params.get("expression", "")).strip()
    if not expression:
        return {"text": "Please provide an expression, e.g. 12*(3+4)."}
    try:
        parsed = ast.parse(expression, mode="eval")
        value = _eval(parsed.body)  # type: ignore[arg-type]
        return {"text": f"{expression} = {value}", "data": {"result": value}}
    except Exception as exc:
        return {"text": "Could not evaluate expression.", "error": str(exc)}

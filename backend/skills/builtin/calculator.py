from __future__ import annotations

import ast
import re
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
    if isinstance(node, ast.Constant):  # Python 3.8+
        return float(node.value)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.left), _eval(node.right))
    raise ValueError("Unsupported expression")


def _extract_expression(text: str) -> str:
    """Extract mathematical expression from natural language"""
    # Remove common words
    text = text.lower()
    for word in ['calculate', 'compute', 'what', 'is', 'solve', 'math', 'equals', 'equal', '?']:
        text = text.replace(word, '')
    
    # Extract numbers and operators
    # Match patterns like "25 * 4", "25*4", "25 x 4", "25 times 4", etc.
    text = text.replace('x', '*').replace('×', '*').replace('÷', '/')
    text = text.replace('plus', '+').replace('minus', '-').replace('times', '*').replace('divided by', '/')
    text = text.replace('multiplied by', '*').replace('added to', '+').replace('subtracted from', '-')
    
    # Find expression pattern
    pattern = r'[\d\s\+\-\*\/\(\)\.\^]+'
    matches = re.findall(pattern, text)
    if matches:
        # Get the longest match
        expression = max(matches, key=len).strip()
        # Clean up spaces around operators
        expression = re.sub(r'\s*([+\-*/^()])\s*', r'\1', expression)
        return expression
    
    return text.strip()


async def run(params: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    # Try to get expression from params or query
    expression = str(params.get("expression", params.get("query", ""))).strip()
    
    # If no direct expression, extract from text
    if not expression or any(word in expression.lower() for word in ['calculate', 'compute', 'what']):
        expression = _extract_expression(expression)
    
    if not expression or not any(c.isdigit() for c in expression):
        return {"text": "Please provide a mathematical expression. For example: 'Calculate 25 * 4' or '12 + 5 * 3'"}
    
    try:
        parsed = ast.parse(expression, mode="eval")
        value = _eval(parsed.body)  # type: ignore[arg-type]
        
        # Format result nicely
        if value == int(value):
            result_str = str(int(value))
        else:
            result_str = f"{value:.4f}".rstrip('0').rstrip('.')
        
        return {
            "text": f"🧮 **Calculation:**\n`{expression}` = **{result_str}**",
            "data": {"expression": expression, "result": value}
        }
    except Exception as exc:
        return {
            "text": f"Could not evaluate '{expression}'. Please use valid math like: 25 * 4 + 10",
            "error": str(exc)
        }

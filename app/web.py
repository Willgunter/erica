from __future__ import annotations

try:
    from flask import Flask, jsonify, redirect, render_template, request
except ImportError:  # pragma: no cover
    from app.flask_shim import Flask, jsonify, redirect, render_template, request

__all__ = ["Flask", "jsonify", "redirect", "render_template", "request"]

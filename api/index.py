"""
api/index.py
============
Vercel Serverless Function entry point.
Exposes the WSGI Flask application object for modern Vercel Serverless deployments.
"""

from app import app

# Vercel looks for the WSGI application callable
app = app

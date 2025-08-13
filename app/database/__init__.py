"""
app/core/database/__init__.py
Responsibility:
- Exports database handlers and factory.
- Centralized import point for database functionality.
"""
from app.database.base import DatabaseHandler
from app.database.mysql.handler import MySQLHandler
from app.database.manager import DatabaseManager, DatabaseHandlerFactory, get_session, get_db_manager

__all__ = [
    "DatabaseHandler",
    "DatabaseHandlerFactory",
    "MySQLHandler",
    "DatabaseManager",
    "get_session",
    "get_db_manager"
]

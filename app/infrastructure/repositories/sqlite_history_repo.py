import sqlite3
from pathlib import Path
from typing import List, Optional

from app.domain.entities.calculation_history import CalculationHistory
from app.domain.interfaces.history_repository import HistoryRepository


class SqliteHistoryRepository(HistoryRepository):
    def __init__(self, db_path: str = "history.db") -> None:
        self._db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self._db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS calculation_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    vehicle_id TEXT NOT NULL,
                    vehicle_type TEXT NOT NULL,
                    distance_km REAL NOT NULL,
                    weight_tons REAL NOT NULL,
                    total_co2_kg REAL NOT NULL,
                    breakdown TEXT NOT NULL,
                    formula_used TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def save(self, history: CalculationHistory) -> None:
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT INTO calculation_history
                (vehicle_id, vehicle_type, distance_km, weight_tons, total_co2_kg, breakdown, formula_used)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    history.vehicle_id,
                    history.vehicle_type,
                    history.distance_km,
                    history.weight_tons,
                    history.total_co2_kg,
                    str(history.breakdown),
                    history.formula_used,
                ),
            )
            conn.commit()

    def get_by_vehicle_id(self, vehicle_id: str) -> List[CalculationHistory]:
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM calculation_history WHERE vehicle_id = ? ORDER BY created_at DESC",
                (vehicle_id,),
            )
            rows = cursor.fetchall()
            return [self._row_to_entity(row) for row in rows]

    def get_all(self, limit: int = 100, offset: int = 0) -> List[CalculationHistory]:
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM calculation_history ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (limit, offset),
            )
            rows = cursor.fetchall()
            return [self._row_to_entity(row) for row in rows]

    def get_by_id(self, history_id: int) -> Optional[CalculationHistory]:
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM calculation_history WHERE id = ?", (history_id,)
            )
            row = cursor.fetchone()
            return self._row_to_entity(row) if row else None

    def _row_to_entity(self, row: sqlite3.Row) -> CalculationHistory:
        import ast
        from datetime import datetime

        breakdown_str = row["breakdown"]
        try:
            breakdown = ast.literal_eval(breakdown_str)
        except Exception:
            breakdown = {}

        return CalculationHistory(
            id=row["id"],
            vehicle_id=row["vehicle_id"],
            vehicle_type=row["vehicle_type"],
            distance_km=row["distance_km"],
            weight_tons=row["weight_tons"],
            total_co2_kg=row["total_co2_kg"],
            breakdown=breakdown,
            formula_used=row["formula_used"],
            created_at=datetime.fromisoformat(row["created_at"]),
        )
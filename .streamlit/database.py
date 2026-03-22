import streamlit as st
import sqlite3
import hashlib
import uuid
from datetime import datetime
from typing import Optional, Dict, List, Tuple
import pandas as pd

DB_NAME = "safe_users.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            telefono TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            tipo TEXT,
            descripcion TEXT,
            ubicacion TEXT,
            barrio TEXT,
            gravedad TEXT,
            estado TEXT DEFAULT 'pendiente',
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def create_user(
    nombre: str, email: str, password: str, telefono: str
) -> Tuple[bool, str]:
    if len(password) < 6:
        return False, "La contraseña debe tener al menos 6 caracteres"

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    try:
        user_id = str(uuid.uuid4())
        c.execute(
            "INSERT INTO users (id, nombre, email, password_hash, telefono) VALUES (?, ?, ?, ?, ?)",
            (user_id, nombre, email, hash_password(password), telefono),
        )
        conn.commit()
        conn.close()
        return True, "Usuario registrado exitosamente"
    except sqlite3.IntegrityError:
        conn.close()
        return False, "El email ya está registrado"


def verify_user(email: str, password: str) -> Optional[Dict]:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "SELECT id, nombre, email, telefono FROM users WHERE email = ? AND password_hash = ?",
        (email, hash_password(password)),
    )
    user = c.fetchone()
    conn.close()

    if user:
        return {"id": user[0], "nombre": user[1], "email": user[2], "telefono": user[3]}
    return None


def save_incident(
    user_id: str,
    tipo: str,
    descripcion: str,
    ubicacion: str,
    barrio: str,
    gravedad: str,
) -> str:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    incident_id = str(uuid.uuid4())
    c.execute(
        "INSERT INTO incidents (id, user_id, tipo, descripcion, ubicacion, barrio, gravedad) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (incident_id, user_id, tipo, descripcion, ubicacion, barrio, gravedad),
    )
    conn.commit()
    conn.close()
    return incident_id


def get_incidents(user_id: Optional[str] = None) -> List[Dict]:
    conn = sqlite3.connect(DB_NAME)
    if user_id:
        df = pd.read_sql(
            "SELECT * FROM incidents WHERE user_id = ? ORDER BY fecha DESC",
            conn,
            params=(user_id,),
        )
    else:
        df = pd.read_sql("SELECT * FROM incidents ORDER BY fecha DESC", conn)
    conn.close()
    return df.to_dict("records")


def get_incident_stats() -> Dict:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    stats = {}
    c.execute("SELECT COUNT(*) FROM incidents")
    stats["total"] = c.fetchone()[0]

    c.execute("SELECT gravedad, COUNT(*) FROM incidents GROUP BY gravedad")
    stats["por_gravedad"] = dict(c.fetchall())

    c.execute("SELECT tipo, COUNT(*) FROM incidents GROUP BY tipo")
    stats["por_tipo"] = dict(c.fetchall())

    c.execute(
        "SELECT barrio, COUNT(*) FROM incidents GROUP BY barrio ORDER BY COUNT(*) DESC LIMIT 10"
    )
    stats["top_barrios"] = dict(c.fetchall())

    conn.close()
    return stats


init_db()

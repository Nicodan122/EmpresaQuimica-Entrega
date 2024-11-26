import mysql.connector
from config import db_config

def get_all_items(usuario_id):
    """Obtiene todos los elementos de la tabla wishlist."""
    conn = None
    cursor = None
    try:
        print (usuario_id)
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM wishlist WHERE usuario_id = %s", (usuario_id,))
        result = cursor.fetchall()
        return result
    finally:
        cursor.close()
        conn.close()

def add_item(usuario_id, producto_id):
    """Agrega un elemento a la tabla wishlist."""
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO wishlist (usuario_id, producto_id) VALUES (%s, %s)",
            (usuario_id, producto_id)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        conn.close()

def delete_item(item_id):
    """Elimina un elemento de la tabla wishlist por su ID."""
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM wishlist WHERE id = %s", (item_id,))
        conn.commit()
        return cursor.rowcount
    finally:
        cursor.close()
        conn.close()

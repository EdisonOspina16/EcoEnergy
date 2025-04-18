import psycopg2
from psycopg2.extras import RealDictCursor
from model.dispositivo import Dispositivo
from model.producto import Producto
from SecretConfig import PGHOST, PGDATABASE, PGUSER, PGPASSWORD


def obtener_conexion():
    try:
        return psycopg2.connect(
            host=PGHOST,
            database=PGDATABASE,
            user=PGUSER,
            password=PGPASSWORD
        )
    except Exception as e:
        print("Error de conexión:", e)
        return None


def obtener_productos_y_dispositivos():
    conn = obtener_conexion()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    cursor.execute("""
        SELECT d.id, d.id_producto, d.fecha_registro, p.nombre, p.vatios 
        FROM dispositivos d 
        LEFT JOIN productos p ON d.id_producto = p.id
    """)
    dispositivos = cursor.fetchall()

    cursor.close()
    conn.close()
    return productos, dispositivos


def agregar_producto(nombre, categoria, vatios):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO productos (nombre, categoria, vatios)
        VALUES (%s, %s, %s)
    """, (nombre, categoria, vatios))
    conn.commit()
    cursor.close()
    conn.close()


def eliminar_producto_y_dispositivos(producto_id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM dispositivos WHERE id_producto = %s", (producto_id,))
    cursor.execute("DELETE FROM productos WHERE id = %s", (producto_id,))
    conn.commit()
    cursor.close()
    conn.close()


def agregar_dispositivo():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO dispositivos DEFAULT VALUES")
    conn.commit()
    cursor.close()
    conn.close()


def eliminar_dispositivo(dispositivo_id):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM dispositivos WHERE id = %s", (dispositivo_id,))
    conn.commit()
    cursor.close()
    conn.close()


def actualizar_dispositivo(dispositivo_id, id_producto):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE dispositivos 
        SET id_producto = %s 
        WHERE id = %s
    """, (id_producto, dispositivo_id))
    conn.commit()
    cursor.close()
    conn.close()

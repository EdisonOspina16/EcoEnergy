import sys
sys.path.append("src")

import psycopg2
from psycopg2.extras import RealDictCursor
from model.dispositivo import Dispositivo
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

# -----------------------------------------
# CRUD DISPOSITIVOS
# -----------------------------------------

def crear(nombre_producto, categoria, vatios):
    """
    Crea un nuevo dispositivo y lo retorna como objeto Dispositivo.
    """
    conn = obtener_conexion()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO dispositivo (nombre_producto, categoria, vatios) VALUES (%s, %s, %s) RETURNING id, fecha_creacion",
                    (nombre_producto, categoria, vatios)
                )
                fila = cur.fetchone()
                conn.commit()
                return Dispositivo(id=fila[0], nombre_producto=nombre_producto, categoria=categoria, vatios=vatios, fecha_creacion=fila[1])
        except Exception as e:
            print(f"Error al crear dispositivo: {e}")
        finally:
            conn.close()
    return None


def obtener_dispositivos():
    """
    Retorna una lista de objetos Dispositivo.
    """
    dispositivos = []
    try:
        conn = obtener_conexion()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("SELECT * FROM dispositivo")
        filas = cur.fetchall()

        for fila in filas:
            dispositivo = Dispositivo(
                id=fila['id'],
                nombre_producto=fila['nombre_producto'],
                categoria=fila['categoria'],
                vatios=fila['vatios'],
                fecha_creacion=fila['fecha_creacion']
            )
            dispositivos.append(dispositivo)

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error al obtener dispositivos: {e}")
    return dispositivos


def obtener_dispositivo_por_id(id):
    """
    Obtiene un dispositivo por su ID.
    """
    try:
        conn = obtener_conexion()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("SELECT * FROM dispositivo WHERE id = %s", (id,))
        fila = cur.fetchone()

        cur.close()
        conn.close()

        if fila:
            return Dispositivo(
                id=fila['id'],
                nombre_producto=fila['nombre_producto'],
                categoria=fila['categoria'],
                vatios=fila['vatios'],
                fecha_creacion=fila['fecha_creacion']
            )
        return None
    except Exception as e:
        print(f"Error al obtener dispositivo por ID: {e}")
        return None


def actualizar_dispositivo(dispositivo: Dispositivo):
    """
    Actualiza la información de un dispositivo existente.
    """
    try:
        conn = obtener_conexion()
        cur = conn.cursor()

        cur.execute("""
            UPDATE dispositivo
            SET nombre_producto = %s, categoria = %s, vatios = %s
            WHERE id = %s
        """, (dispositivo.nombre_producto, dispositivo.categoria, dispositivo.vatios, dispositivo.id))

        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al actualizar dispositivo: {e}")
        return False


def eliminar_dispositivo(id):
    """
    Elimina un dispositivo por ID.
    """
    try:
        conn = obtener_conexion()
        cur = conn.cursor()

        cur.execute("DELETE FROM dispositivo WHERE id = %s", (id,))
        conn.commit()

        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al eliminar dispositivo: {e}")
        return False

# -----------------------------------------
# FUNCIONES DEL ADMIN
# -----------------------------------------

def obtener_todos_dispositivos():
    return [dispositivo.to_dict() for dispositivo in Dispositivo.obtener_todos()]


def obtener_dispositivo_por_id(id):
    dispositivo = obtener_dispositivo_por_id(id)
    if dispositivo:
        return dispositivo.to_dict()
    return None


def crear_dispositivo(nombre_producto, categoria, vatios):
    if not nombre_producto or not categoria or not vatios:
        return {"error": "Todos los campos son obligatorios"}, 400
    
    try:
        vatios = int(vatios)
        if vatios <= 0:
            return {"error": "Los vatios deben ser un número positivo"}, 400
    except ValueError:
        return {"error": "Los vatios deben ser un número entero"}, 400
    
    dispositivo = crear(nombre_producto, categoria, vatios)
    if dispositivo:
        return dispositivo.to_dict(), 201
    return {"error": "Error al crear el dispositivo"}, 500


def actualizar_dispositivo(id, nombre_producto, categoria, vatios):
    dispositivo = obtener_dispositivo_por_id(id)
    if not dispositivo:
        return {"error": "Dispositivo no encontrado"}, 404
    
    try:
        vatios = int(vatios)
        if vatios <= 0:
            return {"error": "Los vatios deben ser un número positivo"}, 400
    except ValueError:
        return {"error": "Los vatios deben ser un número entero"}, 400
    
    dispositivo.nombre_producto = nombre_producto
    dispositivo.categoria = categoria
    dispositivo.vatios = vatios
    
    if dispositivo.actualizar():
        return dispositivo.to_dict(), 200
    return {"error": "Error al actualizar el dispositivo"}, 500

def eliminar_dispositivo(id):
    if Dispositivo.eliminar(id):
        return {"mensaje": "Dispositivo eliminado correctamente"}, 200
    return {"error": "Error al eliminar el dispositivo"}, 500


def calcular_consumo(dispositivos_ids):
    total_watts = 0
    
    for id in dispositivos_ids:
        dispositivo = obtener_dispositivo_por_id(id)
        if dispositivo:
            total_watts += dispositivo.vatios
    
    if total_watts > 0:
        consumo_diario_kwh = (total_watts * 24) / 1000
        consumo_mensual_kwh = consumo_diario_kwh * 30
        
        return {
            "consumo_total_watts": total_watts,
            "consumo_diario_kwh": round(consumo_diario_kwh, 2),
            "consumo_mensual_kwh": round(consumo_mensual_kwh, 2)
        }, 200
    
    return {"error": "No se han seleccionado dispositivos válidos"}, 400


def obtener_dispositivos_por_categoria():
    dispositivos = obtener_todos_dispositivos()
    productos_por_categoria = {}

    for d in dispositivos:
        categoria = d.get('categoria', 'Sin categoría')
        if categoria not in productos_por_categoria:
            productos_por_categoria[categoria] = []
        productos_por_categoria[categoria].append(d)

    return productos_por_categoria

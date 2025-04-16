# src/controller/controladorUsuarios.py
import psycopg2
from psycopg2.extras import RealDictCursor
from src.SecretConfig import PGHOST, PGDATABASE, PGUSER, PGPASSWORD


# Función para conectar a la base de datos
def obtener_conexion():
    try:
        conn = psycopg2.connect(
            host=PGHOST,
            database=PGDATABASE,
            user=PGUSER,
            password=PGPASSWORD
        )
        return conn
    except Exception as e:
        print("Error de conexión:", e)
        return None

# Crear un nuevo usuario
def crear_usuario(nombre, correo, contraseña):
    conn = obtener_conexion()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO usuarios (nombre, correo, contraseña) VALUES (%s, %s, %s)",
                    (nombre, correo, contraseña)
                )
                conn.commit()
                return True
        except Exception as e:
            print("Error al crear usuario:", e)
        finally:
            conn.close()
    return False

# Obtener usuario por correo
def obtener_usuario_por_correo(correo):
    conn = obtener_conexion()
    if conn:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
                usuario = cur.fetchone()
                return usuario
        except Exception as e:
            print("Error al obtener usuario:", e)
        finally:
            conn.close()
    return None

# Actualizar usuario
def actualizar_usuario(correo, nuevo_nombre, nueva_contraseña):
    conn = obtener_conexion()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE usuarios SET nombre = %s, contraseña = %s WHERE correo = %s",
                    (nuevo_nombre, nueva_contraseña, correo)
                )
                conn.commit()
                return True
        except Exception as e:
            print("Error al actualizar usuario:", e)
        finally:
            conn.close()
    return False

# Eliminar usuario
def eliminar_usuario(correo):
    conn = obtener_conexion()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM usuarios WHERE correo = %s", (correo,))
                conn.commit()
                return True
        except Exception as e:
            print("Error al eliminar usuario:", e)
        finally:
            conn.close()
    return False

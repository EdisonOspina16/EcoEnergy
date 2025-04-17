import sys
sys.path.append("src")

import psycopg2
from psycopg2.extras import RealDictCursor
from model.usuario import Usuario
from SecretConfig import PGHOST, PGDATABASE, PGUSER, PGPASSWORD
from werkzeug.security import check_password_hash, generate_password_hash

def obtener_conexion():
    """
    Coneccion a la base de datos.
    
    """
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

# CRUD ->
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

# Funciones Del Sistema.
# Registrar un nuevo usuario
def registrar_usuario(nombre, correo, contraseña):
    try:
        conn = obtener_conexion()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO usuarios (nombre, correo, contraseña)
            VALUES (%s, %s, %s)
        """, (nombre, correo, contraseña))

        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al registrar usuario: {e}")
        return False

# Obtener todos los usuarios registrados
def obtener_usuarios():
    usuarios = []
    try:
        conn = obtener_conexion()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("SELECT * FROM usuarios")
        filas = cur.fetchall()

        for fila in filas:
            usuario = Usuario(
                id=fila['id'],
                nombre=fila['nombre'],
                correo=fila['correo'],
                contraseña=fila['contraseña'],
                fecha_registro=fila['fecha_registro']
            )
            usuarios.append(usuario)

        cur.close()
        conn.close()
    except Exception as e:
        print(f" Error al obtener usuarios: {e}")
    return usuarios

from werkzeug.security import check_password_hash


def verificar_credenciales(correo, contraseña_input):
    #login
    try:
        conn = obtener_conexion()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
        usuario = cur.fetchone()

        cur.close()
        conn.close()

        if usuario and check_password_hash(usuario['contraseña'], contraseña_input):
            return usuario  # Retorna dict con los datos
        else:
            return None
    except Exception as e:
        print(f"Error en login: {e}")
        return None

def actualizar_contraseña(correo, nueva_contraseña):
    #olvido su contraseña??
    try:
        conn = obtener_conexion()
        cur = conn.cursor()
        nueva_hash = generate_password_hash(nueva_contraseña)

        cur.execute("""
            UPDATE usuarios
            SET contraseña = %s
            WHERE correo = %s
        """, (nueva_hash, correo))

        conn.commit()
        cur.close()
        conn.close()

        return cur.rowcount > 0  # Retorna True si se actualizó
    except Exception as e:
        print(f"Error al actualizar contraseña: {e}")
        return False

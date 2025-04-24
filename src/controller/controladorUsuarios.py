import sys
sys.path.append("src")

import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
from model.usuario import Usuario
from SecretConfig import PGHOST, PGDATABASE, PGUSER, PGPASSWORD


def obtener_conexion():
    """
    Conexión a la base de datos.
    """
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
# CRUD USUARIOS
# -----------------------------------------

def crear_usuario(nombre, correo, contraseña):
    """
    Crea un nuevo usuario con la contraseña hasheada.
    """
    conn = obtener_conexion()
    if conn:
        try:
            hash_contraseña = generate_password_hash(contraseña)
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO usuarios (nombre, correo, contraseña) VALUES (%s, %s, %s)",
                    (nombre, correo, hash_contraseña)
                )
                conn.commit()
                return True
        except Exception as e:
            print("Error al crear usuario:", e)
        finally:
            conn.close()
    return False


def obtener_usuario_por_correo(correo):
    conn = obtener_conexion()
    if conn:
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
                return cur.fetchone()
        except Exception as e:
            print("Error al obtener usuario:", e)
        finally:
            conn.close()
    return None


def actualizar_usuario(correo, nuevo_nombre, nueva_contraseña):
    """
    Actualiza nombre y contraseña (la contraseña será hasheada).
    """
    conn = obtener_conexion()
    if conn:
        try:
            hash_contraseña = generate_password_hash(nueva_contraseña)
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE usuarios SET nombre = %s, contraseña = %s WHERE correo = %s",
                    (nuevo_nombre, hash_contraseña, correo)
                )
                conn.commit()
                return True
        except Exception as e:
            print("Error al actualizar usuario:", e)
        finally:
            conn.close()
    return False


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

# -----------------------------------------
# FUNCIONES DEL REGISTRO, LOGIN, RECUPERAR
# -----------------------------------------

def registrar_usuario(nombre, correo, contraseña):
    """
    Registra un usuario nuevo con contraseña hasheada.
    """
    try:
        conn = obtener_conexion()
        cur = conn.cursor()

        hash_contraseña = generate_password_hash(contraseña)

        cur.execute("""
            INSERT INTO usuarios (nombre, correo, contraseña)
            VALUES (%s, %s, %s)
        """, (nombre, correo, hash_contraseña))

        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al registrar usuario: {e}")
        return False


def obtener_usuarios():
    """
    Retorna una lista de objetos Usuario.
    """
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
        print(f"Error al obtener usuarios: {e}")
    return usuarios


def verificar_credenciales(correo, contraseña_input):
    """
    Verifica si el correo y la contraseña (comparada con hash) coinciden.
    """
    try:
        conn = obtener_conexion()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("SELECT * FROM usuarios WHERE correo = %s", (correo,))
        usuario = cur.fetchone()

        cur.close()
        conn.close()

        if usuario and check_password_hash(usuario['contraseña'], contraseña_input):
            return usuario
        return None
    except Exception as e:
        print(f"Error en login: {e}")
        return None


def actualizar_contraseña(correo, nueva_contraseña):
    """
    Actualiza la contraseña de un usuario con hashing.
    """
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

        return cur.rowcount > 0
    except Exception as e:
        print(f"Error al actualizar contraseña: {e}")
        return False





#para mostrar los datos del usuario 
def obtener_usuario_por_id (id_usuario):
    
    try:
        conn = obtener_conexion()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("SELECT * FROM usuarios WHERE id = %s", (id_usuario,))
        fila = cur.fetchone()

        cur.close()
        conn.close()

        if fila:
            return Usuario(
                id=fila['id'],
                nombre=fila['nombre'],
                correo=fila['correo'],
                contraseña=fila['contraseña'],
                fecha_registro=fila['fecha_registro']
            )
    except Exception as e:
        print(f"Error al obtener usuario por ID: {e}")
    return None
















# -----------------------------------------
# FUNCIONES PARA EL HOME-ADMIN.
# -----------------------------------------


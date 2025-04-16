from flask import Flask
from view_web.vista_usuarios import vista_usuarios  # importás el blueprint

app = Flask(__name__)

# Clave secreta para manejar sesiones y mensajes flash
app.secret_key = 'clave_super_secreta_ecoenergy'  # poné algo más seguro si es producción

# Registrar blueprints
app.register_blueprint(vista_usuarios)

# Ruta raíz opcional
@app.route('/')
def inicio():
    return "<h1>Bienvenido a EcoEnergy 🌱</h1>"

if __name__ == '__main__':
    app.run(debug=True)

import sys
sys.path.append("src")

from flask import Flask
from flask import render_template

from src.view_web import vista_usuarios


app = Flask(__name__)

app.secret_key = 'clave_secreta_super_segura_ecoenergy_123'


# Registramos los Blueprints que creamos 
app.register_blueprint(vista_usuarios.blueprint)


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request
from config import SECRET_KEY
from app.blueprints.autenticacion.rutas import autenticacion_bp
from app.blueprints.dashboard.rutas import dashboard_bp
from app.blueprints.usuario.rutas import usuario_bp
from app.blueprints.producto.rutas import producto_bp
from app.blueprints.inicio.rutas import inicio_bp
from app.blueprints.venta.rutas import ventas_bp
from app.blueprints.wishlist.wishlist_blueprint import wishlist_bp

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = SECRET_KEY

    
    @app.before_request
    def method_override():
        if request.method == 'POST' and '_method' in request.form:
            method = request.form['_method'].upper()
            print(f"Interceptando POST. Transformando a: {method}")
            if method in ['PUT', 'DELETE']:
                request.environ['REQUEST_METHOD'] = method


    # Registro de Blueprints
    app.register_blueprint(autenticacion_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(producto_bp)
    app.register_blueprint(inicio_bp)
    app.register_blueprint(ventas_bp)
    app.register_blueprint(wishlist_bp)

    return app

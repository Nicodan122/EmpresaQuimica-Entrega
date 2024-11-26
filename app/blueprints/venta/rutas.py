from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.ventas_service import VentasService
import uuid

ventas_bp = Blueprint('venta', __name__)

@ventas_bp.route('/agregar_venta', methods=['GET', 'POST'])
def agregar_venta():
    if request.method == 'POST':
        id = str(uuid.uuid4())  
        id_usuario = request.form['idUsuario'] 

        nueva_venta = {
            "id": id,
            "idUsuario": id_usuario
        }

        try:
            if VentasService.agregar_venta(nueva_venta):  
                flash("Venta agregada exitosamente.", "success")
                return redirect(url_for('venta.ver_ventas')) 
            else:
                flash("Error al agregar la venta.", "danger")
        except Exception as e:
            flash(f"Ocurrió un error: {str(e)}", "danger")

    return render_template('venta/agregar_venta.html')  

@ventas_bp.route('/editar_venta/<id_venta>', methods=['GET', 'POST'])
def editar_venta(id_venta):
    venta_a_editar = VentasService.obtener_venta_por_id(id_venta)  

    if request.method == 'POST':
        id = venta_a_editar['id']  
        id_usuario = request.form['idUsuario']

        venta_actualizada = {
            "id": id,
            "idUsuario": id_usuario,
            "fecha": venta_a_editar['fecha'] 
        }

        try:
            if VentasService.actualizar_venta(venta_actualizada): 
                flash("Venta actualizada exitosamente.", "success")
                return redirect(url_for('venta.ver_ventas')) 
            else:
                flash("Error al actualizar la venta.", "danger")
        except Exception as e:
            flash(f"Ocurrió un error: {str(e)}", "danger")

    return render_template('venta/editar_venta.html', venta=venta_a_editar)  

@ventas_bp.route('/eliminar_venta/<id_venta>', methods=['POST'])
def eliminar_venta(id_venta):
    try:
        if VentasService.eliminar_venta(id_venta):
            flash("Venta eliminada exitosamente.", "success")
        else:
            flash("Error al eliminar la venta.", "danger")
    except Exception as e:
        flash(f"Ocurrió un error: {str(e)}", "danger")

    return redirect(url_for('venta.ver_ventas'))

# @ventas_bp.route('/ver_ventas', methods=['GET'])
# def ver_ventas():
#     ventas = VentasService.obtener_ventas()  
#     return render_template('venta/ver_ventas.html', ventas=ventas) 

@ventas_bp.route('/ver_ventas', methods=['GET'])
def ver_ventas():
    ventas = VentasService.obtener_ventas()  
    usuarios = VentasService.obtener_usuarios()  

   
    usuarios_dict = {usuario['id']: usuario['usuario'] for usuario in usuarios}

    for venta in ventas:
        venta['nombreUsuario'] = usuarios_dict.get(venta['idUsuario'], "Usuario desconocido")

    return render_template('venta/ver_ventas.html', ventas=ventas)


@ventas_bp.route('/detalles_venta', methods=['GET'])
def detalles_venta():
    id_venta = request.args.get('id_venta')
    venta_detalle = VentasService.obtener_detalles_venta_por_id_venta(id_venta)  
    
    if not venta_detalle:
        venta_detalle = None

    return render_template('venta/detalles_venta.html', venta_detalle=venta_detalle)

@ventas_bp.route('/ver_estadisticas', methods=['GET'])
def ver_estadisticas():
    estadisticas = VentasService.obtener_estadisticas()

    return render_template('venta/ver_estadisticas.html',
                           total_ventas=estadisticas['total_ventas'],
                           promedio_ventas=estadisticas['promedio_ventas'],
                           ultima_venta=estadisticas['ultima_venta'],
                           meses=estadisticas['meses'],
                           ventas_por_mes=estadisticas['ventas_por_mes'],
                           usuarios=estadisticas['usuarios'],
                           ventas_por_usuario=estadisticas['ventas_por_usuario'])

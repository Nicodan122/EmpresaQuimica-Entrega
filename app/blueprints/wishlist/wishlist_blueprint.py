from flask import Blueprint, render_template, request, jsonify, session
from app.services.wishlist_service import get_all_items, add_item, delete_item

wishlist_bp = Blueprint('wishlist', __name__)

@wishlist_bp.route('/wishlist', methods=['GET'])
def get_wishlist():
    try:
        usuario = session['usuario']
        items = get_all_items(usuario['id'])
        return render_template('wishlist/ver_wishlist.html', wishlist=items)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@wishlist_bp.route('/wishlist', methods=['POST'])
def add_to_wishlist():
    data = request.json
    producto_id = data.get('producto_id')

    if not producto_id:
        return jsonify({"error": "El campo 'producto_id' es obligatorio"}), 400

    try:
        usuario = session['usuario']
        result = add_item(usuario['id'], producto_id)
        if "error" in result:
            return jsonify(result), 400
        return jsonify({"message": "Elemento agregado exitosamente", "id": result["id"]}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@wishlist_bp.route('/wishlist/<int:item_id>', methods=['DELETE'])
def delete_from_wishlist(item_id):
    try:
        rows_deleted = delete_item(item_id)
        if rows_deleted == 0:
            return jsonify({"error": "Elemento no encontrado"}), 404
        return jsonify({"message": "Elemento eliminado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



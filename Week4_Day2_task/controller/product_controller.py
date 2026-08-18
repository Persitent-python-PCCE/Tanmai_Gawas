from flask import Blueprint, jsonify, request
from service.product_service import ProductService
from dao.product_dao import ProductDAO

product_dao = ProductDAO()

product_service = ProductService(product_dao)

product_controller = Blueprint("product_controller", __name__)

@product_controller.route("/products", methods=["POST"])
def create_product():
    data = request.get_json(silent=True)

    if data is None:
        return jsonify({
            "error": "Request body must be JSON"
        }), 415

    try:
        product = product_service.create_product(data)
    except Exception as e:
        return jsonify({
            "error":str(e)
        }),400

    return jsonify({
        "message":"Product created successfully",
        "product":product.to_dict()
        }),200

@product_controller.route("/products", methods=["GET"])
def get_all_products():
    try:
        products = product_service.get_all_products()
    except Exception as e:
        return jsonify({
            "error":str(e)
        }),400
    return jsonify({
        "message":"Products fetched successfully",
        "product":[product.to_dict() for product in products]
    })

@product_controller.route("/products/<int:id>", methods=["GET"])
def get_product_by_id(id):
    try:
        product = product_service.get_product_by_id(id)
    except Exception as e:
        return jsonify({
            "error":str(e)
        })
    return jsonify({
        "message":"Product fetched successfully",
        "product":product.to_dict()
    })

@product_controller.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    try:
        data = request.get_json(silent=True)
        product = product_service.update_product(id, data)
    except Exception as e:
            return jsonify({
                "error":str(e)
            })
    return jsonify({
            "message":"Product updated successfully",
            "product":product.to_dict()
        })

@product_controller.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    try:
        product_id = product_service.delete_product(id)
    except Exception as e:
            return jsonify({
                "error":str(e)
            })
    return jsonify({
            "message":f"Product with id {product_id} deleted successfully"
        })

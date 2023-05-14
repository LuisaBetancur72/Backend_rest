from flask import Blueprint, request
from http import HTTPStatus
import sqlalchemy.exc
from src.database import db,ma
import werkzeug
from datetime import datetime


from src.models.product import Product, product_schema, products_schema

products = Blueprint("products",__name__,url_prefix="/api/v1/products")

@products.get("/")
def read_all():
 products = Product.query.order_by(Product.codigo).all()
 return {"data": products_schema.dump(products)}, HTTPStatus.OK


@products.get("/<int:codigo>")
def read_one(codigo):
    products = Product.query.filter_by(codigo=codigo).first()
    
    if(not products):
        return {"error": "Resource not found"}, HTTPStatus.NOT_FOUND
    
    return {"data": product_schema.dump(products)}, HTTPStatus.OK
    
    

@products.post("/")
def create():
    post_data = None
    
    try:
        post_data = request.get_json()
    except werkzeug.exceptions.BadRequest as e:
        return {"error": "Post body JSON data not found",
            "message": str(e)}, HTTPStatus.BAD_REQUEST
    
    # Product.code is auto increment!
    product = Product(name = request.get_json().get("name", None),
                price = request.get_json().get("price", None),
                expiration = expiration_date,
                user_id = request.get_json().get("user_id", None))
    try:
        db.session.add(product)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return {"error": "Invalid resource values",
            "message": str(e)}, HTTPStatus.BAD_REQUEST

    return {"data": product_schema.dump(product)}, HTTPStatus.CREATED
    

@products.put('/<int:id>')
@products.patch('/<int:id>')
def update(id):
    pass

@products.delete("/<int:id>")
def delete(id):
    pass
#Proveedores de un producto
@products.get("/<int:id_producto>/providers")
def read_providers(id):
    pass
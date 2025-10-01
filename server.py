from flask import Flask, jsonify, request
from http import HTTPStatus
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

products = [
  {"id": 1, "title": "Cake", "price": 25, "category": "Electronics", "image": "https://picsum.photos/seed/1/300/300"},
  {"id": 2, "title": "Ice-cream", "price": 5, "category": "Kitchen", "image": "https://picsum.photos/seed/2/300/300"},
  {"id": 3, "title": "Cookie", "price": 3, "category": "Electronics", "image": "https://picsum.photos/seed/3/300/300"},
  {"id": 4, "title": "Chocolate", "price": 10, "category": "Entertainment", "image": "https://picsum.photos/seed/4/300/300"}
]



#products = [
    #{"id": 1, "name": "Cake", "price": 25},
    #{"id": 2, "name": "Ice-cream", "price": 5},
    #{"id": 3, "name": "Cookie", "price": 3},
    #{"id": 4, "name": "Chocolate", "price": 10}
#]




@app.route("/api/products",methods=["GET"])
def get_products():
    return jsonify(products)

@app.route("/api/products/count", methods=["GET"])
def get_product_count():
    return jsonify({"count": len(products)})
    



# ---- Assignment 2 ----


# In-memory products list (acting as a simple database)
# products = []
next_id = 1

# POST /api/products -> Add a new product
@app.route("/api/products", methods=["POST"])
def add_product():
    global next_id
    data = request.get_json()

    if not data or "name" not in data or "price" not in data:
        return jsonify({"error": "Invalid product data. 'name' and 'price' are required."}), 400

    product = {
        "id": next_id,
        "name": data['name'],
        "price": data['price']
    }
    products.append(product)
    next_id += 1

    return jsonify(product), 201  # 201 Created


# GET /api/products/<int:id> -> Retrieve product by id
@app.route('/api/products/<int:id>', methods=["GET"])
def get_product(id):
    product = next((p for p in products if p["id"] == id), None)
    if not product:
        return jsonify({"error": f"Product with id {id} not found."}), 404

    return jsonify(product), 200


# DELETE /api/products/<int:id> -> Delete product by id
@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    global products
    product = next((p for p in products if p["id"] == id), None)
    if not product:
        return jsonify({"error": f"Product with id {id} not found."}), 404

    products = [p for p in products if p['id'] != id]
    return jsonify({"message": f"Product with id {id} deleted successfully."}), 200

#------COUPONS------

coupons = [
    {"_id": 1, "code": "WELCOME10", "discount": 10},
    {"_id": 2, "code": "FALL25", "discount": 25},
    {"_id": 3, "code": "VIP50", "discount": 50},
]

#READ all coupons
@app.route("/api/coupons", methods=["GET"])
def get_coupons():
    return jsonify(coupons), HTTPStatus.OK

@app.route("/api/coupons", methods=["POST"])
def create_coupon():
    new_coupon = request.get_json()
    print(new_coupon)
    coupons.append(new_coupon)
    return jsonify(new_coupon), HTTPStatus.CREATED


#Path parameter
# A path parameter is a dynamic segment of the URL to pipoint a specific item or resource.
# http://127.0.0.1:5000/greet/jose
@app.route("/greet/<string:name>", methods=["GET"])
def greet(name):
    return f"hello {name}", HTTPStatus.OK




#  GET a coupon by id
@app.route("/api/coupons/<int:id>", methods=["GET"])
def get_coupon_by_id(id):
    for coupon in coupons:
        if coupon["_id"] == id:
            return jsonify(coupon), HTTPStatus.OK 
        print(f"coupon: {coupon}")
    return jsonify({"message": "coupon not found"}),HTTPStatus.NOT_FOUND



# --DELETE--
@app.route("/api/coupons/<int:id>", methods=["DELETE"])
def delete_coupon(id):
    for index, coupon in enumerate(coupons):
        if coupon["_id"] == id:
            coupons.pop(index)
            return  HTTPStatus.NO_CONTENT #204
        return jsonify({"message": "coupon deleted successfully"}),"testing"






# ---UPDATE ---

@app.route("/api/products/<int:id>", methods=["PUT"])
def update_product(id):
    data = request.get_json()
    for product in products:
        if product["id"] == id:
            product["name"] =data.get("name")
            product["price"] =data.get("price")
            return jsonify({"message": "Product updated successfully"}), HTTPStatus.OK
    return jsonify({"message": "Product not found"}), HTTPStatus.NOT_FOUND



# ------ Session #4 ------
# Query parameters
# A query parameter is added to the end of the URL to filter, sort or modify the response.

@app.route("/api/products/search", methods=["GET"])
def get_product_by_name():
    keyword = request.args.get("name").lower()
    print(keyword)
    
    
    matched = []
    for product in products:
        if keyword in product["name"].lower():
            matched.append(product)
        #if product["name"].lower() == keyword:
    
    return jsonify({"Results": matched}), HTTPStatus.OK






if __name__ == "__main__":
    app.run(debug=True)
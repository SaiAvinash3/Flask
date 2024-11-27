# from flask import Flask, request,jsonify

# # Initialize the Flask application
# app = Flask(__name__)

# # Define a simple GET API endpoint
# @app.route('/api/hello', methods=['GET'])
# def hello_world():
#     # Return a simple JSON response
#     a=int(request.args.get("a"))
#     b=int(request.args.get("b"))
#     di = {"message": "Hello, World!"}
#     return "a"+"b"
#     # return jsonify({"message": "Hello, World!"})

# # Run the Flask application
# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request
from db import stores, items

app = Flask(__name__)

stores = [
    {
        "name" : "My Store",
        "items" : [
            {
                "name": "Chair",
                "price" : 99
            }
        ]
    }
]

@app.get("/")
def sample():
    return "Hello Welcome to REST API course !!!"

# this is to return all the stores
@app.route("/store")   # http://127.0.0.1:5000/store
def get_stores():
    return {"stores": stores}

# this is to  add store into the list(stores)
@app.post("/store")
def create_store():
    requested_data = request.get_json()
    new_store = { "name" : requested_data["name"], "items" : []}
    stores.append(new_store)
    return new_store, 201

# this is to add the items into a specified store
@app.post("/store/<string:name>/item")
def create_item(name):
    requested_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name" : requested_data["name"], "price" : requested_data["price"]}
            store["items"].append(new_item)
            return new_item,201
    return {"Message : Store not found"}, 404

# How to get a specific store and its items
@app.get("/store/<string:name>")
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return store
    return {"Message : store not found"}, 404

@app.get("/store/<string:name>/item")
def get_item_store(name):
    for store in stores:
        if store["name"] == name:
            return {"items" : store["items"]}
    return {"Message : store not found"}, 404

if __name__ == '__main__':
    app.run(debug=True)
    
# ==================================================== #

#============================================================

# import uuid
# from flask import Flask, request
# from flask_smorest import abort

# from db import stores, items


# app = Flask(__name__)

# @app.get("/store")
# def get_stores():
#     return {"stores": list(stores.values())}


# @app.get("/item/<string:item_id>")
# def get_item(item_id):
#     try:
#         return items[item_id]
#     except KeyError:
#         abort(404, message="Item not found.")


# @app.post("/item")
# def create_item():
#     item_data = request.get_json()
#     # Here not only we need to validate data exists,
#     # But also what type of data. Price should be a float,
#     # for example.
#     if (
#         "price" not in item_data
#         or "store_id" not in item_data
#         or "name" not in item_data
#     ):
#         abort(
#             400,
#             message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.",
#         )
#     for item in items.values():
#         if (
#             item_data["name"] == item["name"]
#             and item_data["store_id"] == item["store_id"]
#         ):
#             abort(400, message=f"Item already exists.")

#     item_id = uuid.uuid4().hex
#     item = {**item_data, "id": item_id}
#     items[item_id] = item

#     return item


# @app.get("/item")
# def get_all_items():
#     return {"items": list(items.values())}


# @app.get("/store/<string:store_id>")
# def get_store(store_id):
#     try:
#         # Here you might also want to add the items in this store
#         # We'll do that later on in the course
#         return stores[store_id]
#     except KeyError:
#         abort(404, message="Store not found.")


# @app.post("/store")
# def create_store():
#     store_data = request.get_json()
#     if "name" not in store_data:
#         abort(
#             400,
#             message="Bad request. Ensure 'name' is included in the JSON payload.")
#     for store in stores.values():
#         if store_data["name"] == store["name"]:
#             abort(400, message=f"Store already exists.")

#     store_id = uuid.uuid4().hex
#     store = {**store_data, "id": store_id}
#     stores[store_id] = store

#     return store


# @app.delete("/item/<string:item_id>")
# def del_item(item_id):
#     try :
#         del items[item_id]
#         return {"message" : "Item deleted."}
#     except KeyError:
#         abort(404, message = "Item not found.")
        
# @app.put("/item/<string:item_id>")
# def update_item(item_id):
#     item_data = request.get_json()
#     if ( "price" not in item_data or "name" not in item_data):
#         abort(400, message = "Bad Request. Ensure 'price', 'store_id', 'name' are included in the JSON payload.")
    
#     try:
#         item = items[item_id]
#         item |= item_data
        
#         return item
#     except:
#         abort(404, message = "Item not found.")

# if __name__ == '__main__':
#     app.run(debug=True)
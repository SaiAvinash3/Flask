from flask import Flask, request
from flask_smorest import abort
from db import stores, items
import uuid

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
    return {"stores": list(stores.values())}

# How to get a specific store and its items
@app.get("/store/<string:store_id>")
def get_store(store_id):
    try :
        return stores[store_id]
    except KeyError:
        abort(404, message = "Store not found.")

# this is to  add store into the list(stores)
@app.post("/store")
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(400, message = "Bad Request. Ensure 'name' is included in the JSON payload.")
    
    for store in stores.values():
        if (store_data["name"] == store["name"]):
            abort(400, message = f"Store already exists.")
            
    store_id = uuid.uuid4().hex
    store = {**store_data, "id" : store_id}
    stores[store_id] = store
    
    return store, 201


@app.delete("/store/<string:store_id>")
def del_store(store_id):
    try :
        del stores[store_id]
        return {"message" : "Store deleted."}
    except KeyError:
        abort(404, message = "Store not found.")



# app.route("/items")   # http://127.0.0.1:5000/items
# def get_items():
#     return {"items": list(items.values())}

@app.get("/item")
def get_all_items():
    return "Hello World!!!"
    return { "items" : list(items.values())}


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try :
        return items[item_id]
    except KeyError:
        abort(404, message = "Item not found.")


# this is to add the items into a specified store
@app.post("/item")
def create_item():
    item_data = request.get_json()
    # Here we need to validate the data exists and also type of data passing
    if ( "price" not in item_data or "store_id" not in item_data or
        "name" not in item_data):
        abort(400, message = "Bad Request. Ensure 'price', 'store_id', 'name' are included in the JSON payload.")
    
    for item in items.values():
        if ( item_data["name"] == item["name"] and 
            item_data["store_id"] == item["store_id"]):
            abort(400, message = f"Item already exists.")
    
    if item_data["store_id"] not in stores:
        abort(404, message = "Store not found.")
    
    item_id = uuid.uuid4().hex
    item = {**item_data, "id" : item_id}
    items[item_id] = item
    
    return item, 201
    

@app.delete("/item/<string:item_id>")
def del_item(item_id):
    try :
        del items[item_id]
        return {"message" : "Item deleted."}
    except KeyError:
        abort(404, message = "Item not found.")
    
@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if ( "price" not in item_data or "name" not in item_data):
        abort(400, message = "Bad Request. Ensure 'price', 'store_id', 'name' are included in the JSON payload.")
    
    try:
        item = items[item_id]
        item |= item_data
        
        return item
    except:
        abort(404, message = "Item not found.")
        
if __name__ == '__main__':
    app.run(debug=True)


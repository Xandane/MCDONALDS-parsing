from flask import Flask, jsonify, Response
import json

with open("products_data.json", "r", encoding="utf-8") as f:
    data_file = json.load(f)

app = Flask(__name__)


@app.route("/all_products/") # created endpoint for key words all_products
def all():
    return Response(
        json.dumps(data_file, ensure_ascii=False, indent=2),
        content_type="application/json"
    )


def normalize(text): # transform the data on one register
    return text.lower().replace(" ", "")

@app.route("/products/<string:product_name>")  #ability to find position on his name
def get_product(product_name):
    norm_input = normalize(product_name)
    for key in data_file:
        if normalize(key) == norm_input:
            return jsonify(data_file[key])
    return {"error": "Product not found"}, 404



@app.route("/product_names/") # take all names
def product_names():
    return jsonify(list(data_file.keys()))



# we get the desired value from a specific menu item
@app.route("/products/<string:product_name>/<string:field>")
def get_product_field(product_name, field):
    norm_input = normalize(product_name)
    for key in data_file:  #we go through all the properties through a loop
        if normalize(key) == norm_input: # align the register
            product = data_file[key] # compare info
            if field in product:
                return jsonify({field: product[field]}) # we provide information at the user's request
            return {"error": f"Field '{field}' not found"}, 404
    return {"error": "Product not found"}, 404





if __name__ == "__main__":
    app.run(debug=True)
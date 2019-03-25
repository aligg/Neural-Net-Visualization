from flask import (Flask, json, Response, request, render_template, session)
from flask_cors import CORS
# from flask.ext.session import Session
from NNDataSerialization import (load_sin_data, load_xor_data,
                                 nndata_deserializer, NNDataSerializer)
from FFBPNetwork import FFBPNetwork

app = Flask(__name__, template_folder="../javascript/public")
CORS(app, origins=["http://localhost:3000"], supports_credentials=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/fetch-objects/<string:obj>", methods=["GET"])
# @cross_origin(origin='*', supports_credentials=True, headers=['Content- Type', 'Authorization'])
def fetch_json_object(obj):
    """Retrieve user selection json obj type to run through network."""
    print("HOLA")
    if obj == "sin":
        payload = load_sin_data()
    else:
        payload = load_xor_data()

    session.clear()  # Loaded a new object, let's clear the session.
    session["data"] = payload  # Store the NNData object in the session.

    payload_decoded = json.loads(payload, object_hook=nndata_deserializer)
    # Add network info to the session.
    _create_network(len(payload_decoded.x), len(payload_decoded.y))

    return response(status=200, payload=payload)


@app.route("/fetch-current-layer", methods=["GET"])
# @cross_origin(origin='*', supports_credentials=True, headers=['Content- Type', 'Authorization'])
def get_current_layer():
    """Retrieve current layer."""
    network = _get_network_from_session()
    curr_layer = network.layers.current
    payload = json.dumps({
        "num_neurodes": curr_layer.num_neurodes,
        "neurode_type": str(curr_layer.my_type)
    })
    return response(status=200, payload=payload)


def _create_network(x, y):
    """Helper to create the network for user selected object."""
    # add network info to session
    session["x"] = x
    session["y"] = y
    session["current_layer"] = 0

    # List of hidden layers, where the value is the number of neurodes.
    session["hidden_layers"] = [3]


def _get_network_from_session():
    network = FFBPNetwork(session["x"], session["y"])
    # Add all of the hidden layers.
    for num_neurodes in session["hidden_layers"]:
        network.add_hidden_layer(num_neurodes)
    # Get to the current layer.
    for _ in range(session["current_layer"]):
        network.layers.iterate()
    return network


def response(status, payload):
    """Response helper to craft a Flask JSON response"""
    mimetype = "application/json"
    rsp = Response(response=payload, status=status, mimetype=mimetype)
    return rsp


if __name__ == "__main__":
    app.secret_key = 'woof'
    app.run()

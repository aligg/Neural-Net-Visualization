from flask import (Flask, json, Response, request, render_template, session)
from flask_cors import CORS
# from flask.ext.session import Session
from NNDataSerialization import (load_sin_data, load_xor_data,
                                 nndata_deserializer, NNDataSerializer)
from FFBPNetwork import FFBPNetwork
from NNData import NNData

app = Flask(__name__, template_folder="../javascript/public")
CORS(app, origins=["http://localhost:3000"], supports_credentials=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/fetch-objects/<string:obj>", methods=["GET"])
def fetch_json_object(obj):
    """Retrieve user selection json obj type to run through network."""
    if obj == "sin":
        payload = load_sin_data()
    else:
        payload = load_xor_data()

    session.clear()  # Loaded a new object, let's clear the session.
    session["data"] = payload  # Store the NNData object in the session.

    payload_decoded = json.loads(payload, object_hook=nndata_deserializer)
    # Add network info to the session.
    _save_network_specifications(
        len(payload_decoded.x[0]), len(payload_decoded.y[0]))

    return response(status=200, payload=payload)


@app.route("/run-network/<blob>", methods=["GET"])
def run_network(blob):
    """Send network specifications"""
    data = json.loads(blob)
    epochs = data["epochs"]
    hidden_layers = data["hiddenLayers"]
    session["hidden_layers"] = hidden_layers
    _run_network(epochs)
    return response(200)


@app.route("/fetch-current-layer", methods=["GET"])
def get_current_layer_info():
    """Retrieve current layer."""
    network = _get_network_from_session()
    curr_layer = network.layers.current
    payload = json.dumps({
        "num_neurodes": curr_layer.num_neurodes,
        "neurode_type": str(curr_layer.my_type)
    })
    return response(status=200, payload=payload)


def _save_network_specifications(x, y):
    """Helper to save the network to session for user selected object."""
    # add network info to session
    session["num_inputs"] = x
    session["num_outputs"] = y

    # List of hidden layers, where the value is the number of neurodes.
    session["hidden_layers"] = []


def _get_network_from_session():
    network = FFBPNetwork(session["num_inputs"], session["num_outputs"])
    # Add all of the hidden layers.
    for num_neurodes in session["hidden_layers"]:
        network.add_hidden_layer(num_neurodes)
    return network


def _run_network(epochs):
    """Helper to structure data and run the network."""

    network = _get_network_from_session()
    data = json.loads(session["data"], object_hook=nndata_deserializer)
    network.train(data, epochs, order=NNData.Order.RANDOM)


def response(status, payload=None):
    """Response helper to craft a Flask JSON response"""
    mimetype = "application/json"
    rsp = Response(response=payload, status=status, mimetype=mimetype)
    return rsp


if __name__ == "__main__":
    app.secret_key = 'woof'
    app.run()

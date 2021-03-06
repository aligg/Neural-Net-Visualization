import * as api from "../api.js";
import Network from "./Network";
import React from "react";

class Home extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            objectType: "",
            loadedObject: null,
            hiddenLayers: [1, 2, 3], // hard coding for now
            layers: [],
            showNetwork: false,
            epochs: 1000, // hard coding for now
        };
    }

    handleChangeObject = (e) => {
        const value = e.target.value;
        this.setState(
            {
                ...this.state,
                objectType: value,
            },
            () => {
                if (this.state.objectType !== "") {
                    api.fetchJSONObjects(this.state.objectType).then((json) => {
                        this.setState({
                            ...this.state,
                            loadedObject: json,
                        });
                        this.updateLayers(json.__NNData__);
                    });
                } else {
                    this.setState({
                        ...this.state,
                        loadedObject: null,
                        layers: [],
                        showNetwork: false,
                    });
                }
            },
        );
    };

    updateLayers = (obj) => {
        let layers = [...this.state.layers];
        if (layers.length === 0) {
            // num neurodes in input is the length of item in x
            layers.push({ layerType: "Input", numNeurodes: obj.x[0].length });
            // num neurodes in output is the length of an item in y
            layers.push({ layerType: "Output", numNeurodes: obj.y[0].length });
        }
        this.setState({
            ...this.state,
            layers: layers,
        });
    };

    runNetwork = () => {
        const blob = {
            epochs: this.state.epochs,
            hiddenLayers: this.state.hiddenLayers,
        };
        api.runNetwork(blob).then((result) => {
            console.log(result);
            // ToDo: show user some sort of indication running in progress
            // ToDo: use result to let user know training complete
        });
    };

    renderNetwork = () => {
        this.setState({
            ...this.state,
            showNetwork: true,
        });
    };

    render() {
        return (
            <div
                style={{
                    display: "flex",
                    flex: 1,
                    justifyContent: "center",
                    alignItems: "center",
                }}
            >
                <div>
                    Load object to run through the network
                    <select
                        value={this.state.objectType}
                        onChange={this.handleChangeObject}
                    >
                        <option value="">--</option>
                        <option value="xor">xor</option>
                        <option value="sin">sin</option>
                    </select>
                    {this.state.loadedObject && (
                        <div>
                            <div>
                                {`Got it. We'll pass  ${
                                    this.state.objectType
                                } data to the network`}
                                .
                            </div>
                            <button onClick={this.renderNetwork}>
                                Browse network
                            </button>
                            {this.state.showNetwork && (
                                <Network layers={this.state.layers} />
                            )}
                            <button onClick={this.runNetwork}>
                                Run network
                            </button>
                        </div>
                    )}
                </div>
            </div>
        );
    }
}

export default Home;

import * as api from "../api.js";
import React from "react";

class Home extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            objectType: "",
            loadedObject: null,
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
                    });
                }
            },
        );
    };

    fetchCurrentLayer = () => {
        api.fetchCurrentLayer().then((layer) => {
            console.log(layer);
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
                                {`Ready to go.  ${
                                    this.state.objectType
                                } loaded`}
                                .
                            </div>
                            <button onClick={this.fetchCurrentLayer}>
                                Browse network
                            </button>
                        </div>
                    )}
                </div>
            </div>
        );
    }
}

export default Home;

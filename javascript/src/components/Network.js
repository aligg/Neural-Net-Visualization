import Layer from "./Layer";
import PropTypes from "prop-types";
import React from "react";

class Network extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            current: 0,
        };
    }

    static propTypes = {
        layers: PropTypes.array.isRequired,
    };

    renderLayers = () => {
        const layersJSX = [];
        this.props.layers.map((layer, i) => {
            layersJSX.push(
                <Layer
                    numNeurodes={layer.numNeurodes}
                    layerType={layer.layerType}
                    current={this.state.current === i}
                    key={layer.numNeurodes}
                />,
            );
        });
        return layersJSX;
    };
    // ToDo: allow user to navigate between layers (toggling current underline)
    // ToDo: if allowed for current layer, allow user to add next hidden layer
    // ToDo: if allowed for current layer, allow user to remove hiddne layer
    // Update state accordingly for all above
    render() {
        return (
            <div
                style={{
                    display: "flex",
                    flexDirection: "row",
                    flex: 1,
                }}
            >
                {this.renderLayers()}
            </div>
        );
    }
}

export default Network;

import PropTypes from "prop-types";
import React from "react";

const styles = {
    circle: {
        width: "50px",
        height: "50px",
        background: "blue",
        borderRadius: "50%",
        margin: "5px",
    },
};

class Layer extends React.Component {
    constructor(props) {
        super(props);
    }

    static propTypes = {
        numNeurodes: PropTypes.number,
        layerType: PropTypes.string.isRequired,
        current: PropTypes.bool,
    };

    renderNeurodes = () => {
        const neurodesJSX = [];
        // javascript hack to get list of length numNeurodes
        [...Array(this.props.numNeurodes).keys()].map((neurode) => {
            neurodesJSX.push(<div style={styles.circle} key={neurode} />);
        });
        return neurodesJSX;
    };

    render() {
        console.log(this.props.current);
        return (
            <div
                style={{
                    display: "flex",
                    flexDirection: "column",
                    borderBottom: this.props.current ? "solid" : null,
                }}
            >
                <div>{this.props.layerType}</div>
                <div
                    style={{
                        display: "flex",
                        flexDirection: "column",
                    }}
                >
                    {this.renderNeurodes()}
                </div>
            </div>
        );
    }
}

export default Layer;

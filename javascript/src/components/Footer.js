import * as theme from "../../public/static/theme.js";
import React from "react";

const Footer = () => {
    return (
        <div
            style={{
                color: theme.colors.grey,
                fontSize: 12,
            }}
        >
            visualization of neural network created for CS 3B at foothill
            college
        </div>
    );
};

export default Footer;

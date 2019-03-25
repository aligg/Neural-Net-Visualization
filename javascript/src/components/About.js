import * as theme from "../../public/static/theme.js";
import React from "react";

class About extends React.Component {
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
                <div
                    style={{
                        maxWidth: "30vw",
                        fontSize: "14px",
                        color: theme.colors.blackish,
                        boxShadow: theme.boxShadow,
                        padding: theme.padding * 4,
                        borderRadius: "5px",
                        lineHeight: 1.3,
                        display: "flex",
                        flexDirection: "column",
                    }}
                >
                    <div
                        style={{
                            fontWeight: 600,
                            color: theme.colors.fuschia,
                            fontSize: "30px",
                            marginBottom: "10px",
                        }}
                    >
                        Welcome.
                    </div>
                    <div>
                        This website was built to satisfy an assignment to
                        visualize a neural network I created as part of a
                        computer science course at foothill college.
                    </div>
                    <div
                        style={{
                            marginTop: "20px",
                            lineHeight: 1.3,
                        }}
                    >
                        Created by
                        <a
                            style={{
                                textDecoration: "none",
                                color: theme.colors.blue,
                                fontWeight: 600,
                            }}
                            href="https://www.twitter.com/aliglenesk"
                            target="_blank"
                        >
                            {" "}
                            Ali Glenesk{" "}
                        </a>
                        .
                    </div>
                </div>
            </div>
        );
    }
}

export default About;

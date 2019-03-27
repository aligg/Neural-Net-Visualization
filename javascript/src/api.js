const ENGINE_URI = "http://localhost:5000";

const methods = {
    GET: "GET",
    POST: "POST",
};

const ERROR_CALLBACK = (error) => {
    console.log(error); // eslint-disable-line no-console
    return null;
};

const JSON_CALLBACK = (response) => {
    return response.json().then((json) => {
        if (response.ok) {
            return json;
        }
        console.error(json); // eslint-disable-line no-console
        throw new APIError(json);
    });
};

const headers = (method) => {
    let headers = {
        Accept: "application/json",
    };
    if (method === methods.POST) {
        headers["Content-Type"] = "application/json";
    }
    return headers;
};

export function fetchJSONObjects(obj) {
    let hdrs = headers(methods.GET);
    return fetch(`${ENGINE_URI}/fetch-objects/${obj}`, {
        method: methods.GET,
        headers: hdrs,
        credentials: "include",
    })
        .then(JSON_CALLBACK)
        .catch(ERROR_CALLBACK);
}

export function fetchCurrentLayer() {
    let hdrs = headers(methods.GET);
    return fetch(`${ENGINE_URI}/fetch-current-layer`, {
        method: methods.GET,
        headers: hdrs,
        credentials: "include",
    })
        .then(JSON_CALLBACK)
        .catch(ERROR_CALLBACK);
}

export function runNetwork(blob) {
    const str = JSON.stringify(blob);
    let hdrs = headers(methods.GET);
    return fetch(`${ENGINE_URI}/run-network/${str}`, {
        method: methods.GET,
        headers: hdrs,
        credentials: "include",
    })
        .then((response) => {
            console.log("Training done.");
        })
        .catch(ERROR_CALLBACK);
}

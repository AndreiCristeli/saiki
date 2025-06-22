// api.js
const API_BASE = "http://localhost:8000/api";

function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
            return decodeURIComponent(cookie.substring(name.length + 1));
        }
    }
    return '';
}

export async function api(endpoint, method = "GET", body = null) {
    const options = {
        method,
        headers: { "Content-Type": "application/json" },
    };

    if (method === "POST") {
        options.headers["X-CSRFToken"] = getCSRFToken();
    }

    if (body) {
        options.body = JSON.stringify(body);
    }

    const res = await fetch(`${API_BASE}/${endpoint}/`, options);
    if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `Error ${res.status}`);
    }

    return res.json();
}

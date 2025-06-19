/** 
 * @file frontend/site/script/api.js
 * 
 * @author AndreiCristeli
 * @author HexagonalUniverse
 * @author victorxaviercosta
 * 
 * @version 0.1
 */

const API_BASE = "http://localhost:8000/api";

export async function api(endpoint, method = "GET", body = null) {
  const options = {
    method,
    headers: { "Content-Type": "application/json" },
  };
  if (body) {
    options.body = JSON.stringify(body);
  }

  const res = await fetch(`${API_BASE}${endpoint}`, options);
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || Error `${res.status}`);
  }
  return res.json();
}

/*
api("/hangar")
        .then(data => {
            communicate(data.msg);
        })
        .catch(err => console.error(err));
*/
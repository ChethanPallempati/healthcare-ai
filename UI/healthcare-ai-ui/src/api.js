const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:8000";

export async function apiRequest(path, { token, headers = {}, ...options } = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      ...headers,
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
  });

  if (!response.ok) {
    let detail = "Request failed";

    try {
      const errorBody = await response.json();
      detail = errorBody.detail || errorBody.error || detail;
    } catch (error) {
      detail = response.statusText || detail;
    }

    throw new Error(detail);
  }

  return response.json();
}

export { API_BASE_URL };

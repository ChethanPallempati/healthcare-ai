# Healthcare AI UI

React frontend for the Healthcare AI demo.

## Run locally

1. Install dependencies:

```bash
npm install
```

2. Start the development server:

```bash
npm start
```

The app runs on `http://localhost:3000` by default.

## Backend URL

The UI talks to the API using `REACT_APP_API_BASE_URL`.

Example:

```bash
REACT_APP_API_BASE_URL=http://127.0.0.1:8000 npm start
```

If the variable is not set, the UI defaults to `http://127.0.0.1:8000`.

## Current flow

- Log in with any user ID in local development.
- Submit diabetes or heart-risk inputs.
- View normalized prediction results.
- Review the saved patient history for the current user session.

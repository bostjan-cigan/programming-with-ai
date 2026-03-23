---
name: flask-endpoints
description: Create Flask API endpoints with proper structure. Use when the user asks to create, add, or generate a Flask endpoint, route, or API.
---

# Flask Endpoint Creation

When creating a Flask API endpoint, follow this workflow:

## 1. Define the route

Use `@app.route()` with the path and allowed methods:

```python
@app.route("/api/example", methods=["GET", "POST"])
def example_endpoint():
    ...
```

## 2. Validate required input

Check that required parameters are present and valid:

```python
data = request.json or {}
required_field = data.get("field_name")
if not required_field or not str(required_field).strip():
    return jsonify({"error": "field_name is required."}), 400
```

For GET params: `request.args.get("key")`

## 3. Return JSON

Use `jsonify()` for responses:

```python
return jsonify({"key": value})
```

## 4. Include basic error handling

- Return 400 for validation errors
- Catch unexpected errors and return 500 with a message

```python
try:
    # main logic
    return jsonify({"result": ...})
except SomeError as e:
    return jsonify({"error": str(e)}), 500
```

## 5. Explain the implementation

Before or after applying changes, briefly explain:
- What the endpoint does
- How to call it (method, path, body/params)
- What it returns

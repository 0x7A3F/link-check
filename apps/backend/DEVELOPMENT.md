# backend

Thanks for contributing to my project, this is how you get a development environment running.

> [!TIP]
> Need help? I'll be happy to help you via email: hi@sander.tf

## Things you Need
- Python
- `pip` for dependencies

## Setting up the environment
Navigate to the `apps/backend/` directory with `cd apps/backend`.

### Create a virtual environment
Create a local Python environment for the backend dependencies.

```bash
py -m venv .venv
```

### Install Python dependencies
The backend is built with FastAPI and served locally with Uvicorn.

```bash
.\.venv\Scripts\python.exe -m pip install fastapi "uvicorn[standard]"
```

## Running the backend
Start the development server from `apps/backend/`.

```bash
.\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000
```

Keep this terminal open while using the frontend. Uvicorn reloads the backend when you change Python files.

The API is available at `http://localhost:8000`. Visit `http://localhost:8000/docs` for FastAPI's interactive API documentation.
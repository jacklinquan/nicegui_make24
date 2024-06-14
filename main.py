#!/usr/bin/env python3
from fastapi import FastAPI

import niceguiapp

app = FastAPI()
niceguiapp.run_with_fastapi(app)

if __name__ == "__main__":
    print("Please start the app with the `uvicorn` command:")
    print("uvicorn main:app --host 0.0.0.0 --port 8000")

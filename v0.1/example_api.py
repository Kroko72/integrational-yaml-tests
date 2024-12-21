from fastapi import FastAPI
from typing import Optional

app = FastAPI()

@app.get("/get_abc")
async def get_a(a: Optional[int] = None, b: Optional[int] = None, c: Optional[int] = None):
    return {"method": "get_abc", "a": a, "b": b, "c": c}

@app.get("/get_xy")
async def get_b(x: Optional[str] = None, y: Optional[str] = None):
    return {"method": "get_xy", "x": x, "y": y}

@app.get("/get_msg")
async def get_c(message: Optional[str] = "Hello"):
    return {"method": "get_msg", "message": message}

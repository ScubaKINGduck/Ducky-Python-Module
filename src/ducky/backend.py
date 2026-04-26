_backend = None

def set_backend(name: str):
    global _backend

    if name == "numpy":
        import numpy as duckpy
    elif name == "cupy":
        import cupy as duckpy
    else:
        raise ValueError("Backend must be numpy or cupy")

def backend():
    return _backend
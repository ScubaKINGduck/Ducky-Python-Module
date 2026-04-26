import numpy as _numpy
_backend = _numpy
def set_backend(name: str):
    global _backend

    if name == "numpy":
        import numpy
        _backend = numpy
    elif name == "cupy":
        import cupy as _cupy
        _backend = _cupy

    else:
        raise ValueError("Backend must be numpy or cupy")

def backend():
    return _backend
from .main import (
    get_time,
    wait,
    Turtle,
    TurtleManager,
    MatrixManager,
    matrix,
    draw,
    scan,
    shift,
    move,
    clear_matrix,
    render,
    IndependentTimer,
    Chatbot,
    Manage,
    rand_int,
    choose,
    current_hour,
    current_minute,
    current_second,
    tokenize,
    stem,
    array,
    calc,
    find_total,
    ask_url,
    ask_json,
    get_coords
)

try:
    import nltk
    nltk.download('punkt', quiet=True)
except Exception:
    pass

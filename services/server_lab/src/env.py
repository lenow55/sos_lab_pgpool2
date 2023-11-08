import os

def get_debug():
    debug: bool = False
    try:
        debug_env: str|None = os.environ.get("DEBUG")
        if isinstance(debug_env, str):
            debug = bool(debug_env)
    except:
        pass
    return debug

def get_root():
    root:str = ""
    try:
        root_env:str|None = os.environ.get("ROOT_PATH")
        if isinstance(root_env, str):
            root = root_env
    except:
        pass
    return root

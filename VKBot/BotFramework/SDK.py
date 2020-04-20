from contracts import contract


class HandleMessage(object):

    def __init__(self, msg: str):
        self.message_to_handle = msg

    def __call__(self, fn, *args, **kwargs):

        def new_func(*args, **kwargs):
            return fn(*args, **kwargs)
        return new_func


class RequiredLvl(object):

    @contract(lvl='int, >=0, <11')
    def __init__(self, lvl: int):
        self.required_level = lvl

    def __call__(self, fn, *args, **kwargs):

        def new_func(*args, **kwargs):
            return fn(*args, **kwargs)
        return new_func


class HandleMessage(object):

    def __init__(self, msg: str = None, first_word: str = None, words_length: int = None):
        self.message_to_handle = msg
        self.words_length = words_length
        self.start_with_word = first_word
        # TODO arguments check for correct

    def __call__(self, fn, *args, **kwargs):

        def new_func(*args, **kwargs):
            return fn(*args, **kwargs)
        return new_func


class InvokeOnAnyMessage(object):
    def __call__(self, fn, *args, **kwargs):
        def new_func(*args, **kwargs):
            return fn(*args, **kwargs)
        return new_func


class InvokeOnAnyEvent(object):
    def __call__(self, fn, *args, **kwargs):
        def new_func(*args, **kwargs):
            return fn(*args, **kwargs)
        return new_func

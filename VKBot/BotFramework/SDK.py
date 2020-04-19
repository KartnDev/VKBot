def wrapping_paper(func):
    def wrapped(gift: int):
        return 'I got a wrapped up {} for you'.format(str(func(gift)))

    return wrapped


@wrapping_paper
def gift_func(giftname: int):
    return giftname
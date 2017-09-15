from cymbology.alphanum import CHAR_MAP


def luhn_modn_checksum(sid):
    """calculate the luhn modolo n check sum."""

    return _luhnify(CHAR_MAP[c] for c in reversed(sid))


def _luhnify(gen):
    """calculates luhn sum given a generator of integers in reverse order."""

    sum_ = 0

    for index, val in enumerate(gen, 1):
        if index % 2:
            val *= 2
            sum_ += val // 10 + val % 10
        else:
            sum_ += val

    return (10 - sum_ % 10) % 10

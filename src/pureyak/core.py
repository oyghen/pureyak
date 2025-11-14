__all__ = ["max_signed_value"]


def max_signed_value(num_bits: int, /) -> int:
    """Return the maximum signed integer value for the specified bit width.

    Examples
    --------
    >>> # compute the maximum signed value for a 32-bit integer
    >>> from pureyak import core
    >>> core.max_signed_value(32)
    2147483647
    """
    if not isinstance(num_bits, int):
        raise TypeError(f"type(num_bits)={type(num_bits).__name__!r} - expected int")

    if num_bits < 2:
        raise ValueError(f"{num_bits=!r} - expected >= 2 for signed range")

    return (1 << (num_bits - 1)) - 1

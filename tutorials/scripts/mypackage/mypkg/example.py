#!/usr/bin/env python

__all__ = ["fibonacci"]


def _recur_fibo(n):
    if n <= 1:
        result = n
    else:
        result = _recur_fibo(n - 1) + _recur_fibo(n - 2)

    return result


def fibonacci(n_terms, verbose: bool = False) -> list[int]:
    r"""Calculate the `n_terms` first terms of the Fibonnaci sequence.

    Parameters
    ----------
    n_terms : int
        Number of terms to return.
    verbose : bool, Optional
        Verbosity flag.

    Returns
    -------
    result : list of int
        List of the `n_terms`th first terms of the Fibonacci sequence.

    """

    assert isinstance(n_terms, int), "n_terms must be an integer!!"

    nterms = 10

    # check if the number of terms is valid
    if nterms <= 0:
        raise ValueError("Plese enter a positive integer")

    if verbose:
        print(f"Calculating the first {n_terms:d}th terms of the Fibonacci sequence")

    result = list(map(_recur_fibo, range(n_terms)))

    return result

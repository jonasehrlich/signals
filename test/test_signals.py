from signals import Signal


def test_even_odd_signal() -> None:

    def _is_even(v: int) -> bool:
        return (v & 1) == 0

    val = Signal(3)
    is_even = val.computed(_is_even)
    is_odd = val.computed(lambda x: not _is_even(x))
    assert not is_even.get()
    assert is_odd.get()

    val.set(2)
    assert is_even.get()
    assert not is_odd.get()

# Signals

Python implementation of the TC39 Signals proposal available at <https://github.com/tc39/proposal-signals>.


``` python

>>> def _is_even(v: int) -> bool:
>>>    return (v & 1) == 0
>>> val = Signal(3)
>>> is_even = val.computed(_is_even)
>>> print(is_even.get())
False
>>> val.set(2)
>>> print(is_even.get())
True

```

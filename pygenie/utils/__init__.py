

import enum
import re
import pathlib

class IntAndDescriptionEnum(enum.Enum):

    def __init__(self, number, descripton):
        super().__init__()
        self.index = number
        self.descripton = descripton

    @classmethod
    def by_index(cls, index):
        for inst in cls:
            if inst.index == index:
                return inst
        raise KeyError("Couldn't find enum with index of {}".format(index))

# Regexp for single line define (all we need)
_DEFINE_REGEXP = r"\s*\#define\s+(?P<symbol>[^\s]+)\s+(?P<value>[^\s]+)\s*"

def strip_l(x):
    x=x.strip()
    if x.lower().endswith('l'):
        x=x[:-1]
    return x

hex_int = lambda x: int(strip_l(x), 16)

strip_int = lambda x: int(strip_l(x))

def extract_defines(file_name, prefix=None, value_mapper=strip_int, required_names=tuple()):

    if isinstance(file_name, (str, bytes)):
        file_name = pathlib.Path(file_name)

    required_names = set(required_names)
    with file_name.open() as f:
        result = []
        for m in re.finditer(_DEFINE_REGEXP, f.read()):
            symbol = m.group('symbol')
            if prefix is not None:
                if not symbol.startswith(prefix):
                    continue
                symbol = symbol[len(prefix):]
            value = value_mapper(m.group('value'))
            result.append((symbol, value))
            required_names.discard(symbol)

    if required_names:
        raise ValueError("Required defines: {} missing from file {}".format(required_names, file_name))

    return result




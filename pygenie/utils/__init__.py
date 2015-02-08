
import enum

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
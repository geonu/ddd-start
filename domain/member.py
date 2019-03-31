from dataclasses import dataclass


class Member:
    pass


@dataclass
class MemberId:
    _id: str

    @property
    def id(self) -> str:
        return self._id


class Customer(Member):
    pass

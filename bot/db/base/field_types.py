from dataclasses import dataclass


@dataclass
class DBFieldTypes:
    STRING: str
    NUMBER: str
    FLOAT: str
    BYTES: str
    BOOLEAN: str


if __name__ == '__main__':
    print(DBFieldTypes.__annotations__)

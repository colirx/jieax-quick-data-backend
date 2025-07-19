from enum import Enum


class Type(Enum):
    # 整型
    TINYINT = 1
    SMALLINT = 2
    MEDIUMINT = 3
    INT = 4
    BIGINT = 5
    # 浮点型
    FLOAT = 6
    DOUBLE = 7
    # 定点型，需要定点的位数，如 DECIMAL(2,0)
    DECIMAL = 8
    # 字符串
    CHAR = 9
    VARCHAR = 10
    TEXT = 11
    # 日期时间
    DATE = 12
    TIME = 13
    DATETIME = 14
    TIMESTAMP = 15


class Reference:
    _table = ''
    _column = ''

    def __init__(self, table: str, column: str):
        self._table = table
        self._column = column

    @property
    def table(self):
        return self._table

    @table.setter
    def table(self, value: str):
        self._table = value

    @property
    def column(self):
        return self._column

    @column.setter
    def column(self, value: str):
        self._column = value


class ReferenceNode:
    current_node = None
    next_node = None

class Column:
    _name = ''
    _type = None
    _size = 0
    _s_size = 0
    _reference = None
    _unique = False
    _nullable = False
    _default = None
    _comment = ''

    def __init__(
            self,
            name: str,
            type: Type,
            size: int,
            s_size: int = 0,
            reference: Reference = None,
            unique: bool = False,
            nullable: bool = False,
            default: object = None,
            comment: str = ''
    ):
        self._name = name
        self._type = type
        self._size = size
        if nullable:
            self._nullable = nullable
        if type == Type.DECIMAL and s_size < 0:
            raise Exception('decimal size must be positive')
        self._reference = reference
        if unique:
            self._unique = unique
        self._s_size = s_size
        self._default = default
        self._comment = comment

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value: Type):
        self._type = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value: int):
        self._size = value

    @property
    def s_size(self):
        return self._s_size

    @s_size.setter
    def s_size(self, value: int):
        self._s_size = value

    @property
    def reference(self):
        return self._reference

    @reference.setter
    def reference(self, value: Reference):
        self._reference = value

    @property
    def unique(self):
        return self._unique

    @unique.setter
    def unique(self, value: bool):
        self._unique = value

    @property
    def nullable(self):
        return self._nullable

    @nullable.setter
    def nullable(self, value: bool):
        self._nullable = value

    @property
    def default(self):
        return self._default

    @default.setter
    def default(self, value: object):
        self._default = value

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, value: str):
        self._comment = value


class Table:
    _name = ''
    _comment = ''
    _columns = []

    def __init__(self, name: str, columns: list[Column], comment):
        self._name = name
        self._columns = columns
        self._comment = comment

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, value: str):
        self._comment = value

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, value: list[Column]):
        self._columns = value

import csv
from collections import defaultdict
from re import findall
from typing import Any


class DuplicateKeyError(Exception):
    def __init__(self, table: str):
        super().__init__(f'Duplicate key "{table}"')


class DuplicateColumnError(Exception):
    def __init__(self, table: str):
        super().__init__(f'Duplicate column in table "{table}"')


def reader(text: str, lower=False, word=False) -> dict[str, Any]:
    def key(s: str) -> str:
        if lower:
            s = s.lower()
        if word:
            s = ''.join(findall(r'\w', s))
        return s

    def value(s: str) -> Any:
        try:
            return int(s)
        except ValueError:
            pass
        try:
            return float(s)
        except ValueError:
            pass
        return s

    data = defaultdict(list)
    step = 0
    for line in csv.reader(text.splitlines()):
        line = [c.strip() for c in line]
        if line == [] or all(c == '' for c in line):
            step = 0
        elif step == 0:
            k = key(line[0])
            if len(line) == 1:
                table = k
                step = 1
            else:
                data[k] = value(line[1])
        elif step == 1:
            columns = [key(c) for c in line]
            if len(columns) != len(set(columns)):
                raise DuplicateColumnError(table)
            step = 2
        else:
            while len(line) < len(columns):
                line.append('')
            data[table].append(
                {columns[i]: value(v) for i, v in enumerate(line[: len(columns)])}
            )
    return data

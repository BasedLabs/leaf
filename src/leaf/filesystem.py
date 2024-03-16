from __future__ import annotations

import glob
import json
import os
import pathlib
import shutil
from enum import StrEnum
from typing import List, Callable, Iterable, TypeVar, Set

from src.leaf.exception import LeafException, ErrorCodes

T = TypeVar('T')


class ObjectType(StrEnum):
    TEMPORAL = 'TEMPORAL'
    FILE = 'FILE'
    DIRECTORY = 'DIRECTORY'


class Object:
    def __init__(self, path_or_object_name: str, parent: Object | None = None):
        """Create an Object instance
        :param Object parent: The parent filesystem object
        :param str path_or_object_name: Path to the object in the filesystem"""

        if not parent and not os.path.exists(path_or_object_name) or not os.path.isabs(path_or_object_name):
            raise LeafException(ErrorCodes.MUST_BE_ABS_PATH).with_additional_message('Must be an absolute path')

        self.parent = parent
        self.extension = '.'.join(pathlib.Path(path_or_object_name).suffixes)
        self.name = os.path.basename(path_or_object_name)

        if parent:
            self.full_path = os.path.join(parent.full_path, self.name)
        else:
            self.full_path = path_or_object_name

        self._temporal_children: Set[Object] = set()

    def add_children(self, path_or_object_name: str) -> Object:
        self._ensure_exists()

        if self.type == ObjectType.TEMPORAL:
            os.mkdir(self.full_path)
            self._permanentize()

        o = Object(
            path_or_object_name,
            self
        )

        if o not in self._temporal_children and o.type == ObjectType.TEMPORAL:
            self._temporal_children.add(o)

        return o

    @property
    def children(self) -> Iterable[Object]:
        self._ensure_exists()

        if self.type == ObjectType.FILE:
            return []

        if not self.physically_exists():
            return []

        for obj in self._temporal_children:
            yield obj

        for file in glob.glob(os.path.join(self.full_path, '*')):
            yield Object(
                os.path.basename(file),
                self
            )

    def _permanentize(self):
        if self.parent and self in self.parent._temporal_children:
            self.parent._temporal_children.remove(self)

    def read_string(self) -> str:
        self._ensure_exists()

        with open(self.full_path, "r") as f:
            return f.read()

    def read_lines(self) -> List[str]:
        self._ensure_exists()

        with open(self.full_path, "r") as f:
            return f.readlines()

    def read_bytes(self) -> bytes:
        self._ensure_exists()

        self._permanentize()

        with open(self.full_path, "rb") as f:
            return f.read()

    def write_string(self, s: str):
        self._ensure_exists()

        self._permanentize()

        with open(self.full_path, 'w') as f:
            f.write(s)

    def write_bytes(self, b: bytes):
        self._ensure_exists()

        self._permanentize()

        with open(self.full_path, 'wb') as f:
            f.write(b)

    def read_json(self) -> T:
        self._ensure_exists()

        return json.load(open(self.full_path, 'r'))

    def write_json(self, j):
        self._ensure_exists()

        self._permanentize()

        json.dump(j, open(self.full_path, 'w'))

    def delete(self):
        if self.parent:
            self._permanentize()
        if self.physically_exists():
            if self.type == ObjectType.FILE:
                os.remove(self.full_path)
            else:
                shutil.rmtree(self.full_path)

    def physically_exists(self) -> bool:
        return os.path.exists(self.full_path)

    def _ensure_exists(self):
        if self.parent and self in self.parent._temporal_children:
            return
        if os.path.exists(self.full_path):
            return
        raise LeafException(ErrorCodes.OBJECT_DOES_NOT_EXIST).with_additional_message(
            f'Object {self.full_path} does not exists')

    @property
    def type(self) -> ObjectType:
        if os.path.isdir(self.full_path):
            return ObjectType.DIRECTORY

        if os.path.isfile(self.full_path):
            return ObjectType.FILE

        return ObjectType.TEMPORAL

    def ch_where(self, predicate: Callable[[Object], bool], recursive=False) -> Iterable[Object]:
        self._ensure_exists()

        for child in self.children:
            if predicate(child):
                yield child
            if recursive:
                yield from child.ch_where(predicate)

    def ch_exists(self, predicate: Callable[[Object], bool], recursive=False) -> bool:
        self._ensure_exists()

        for child in self.children:
            if predicate(child):
                return True
            if recursive and child.ch_exists(predicate):
                return True

        return False

    def ch_first_or_default(self, predicate: Callable[[Object], bool], recursive=False) -> Object | None:
        self._ensure_exists()

        for child in self.children:
            if predicate(child):
                return child
            if recursive:
                found = child.ch_first_or_default(predicate)
                if found:
                    return found
        return None

    def __str__(self):
        return f'{self.type}: {self.full_path}'

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return self.full_path.__hash__()

    def __eq__(self, other: Object) -> bool:
        return self.full_path == other.full_path

    def __ne__(self, other: Object) -> bool:
        return self.full_path != other.full_path

from typing import TYPE_CHECKING, Iterator
from weakref import WeakValueDictionary

from django.core.files.storage import Storage

if TYPE_CHECKING:
    # Avoid circular imports
    from .fields import S3FileField

    FieldsDictType = WeakValueDictionary[str, 'S3FileField']
    StoragesDictType = WeakValueDictionary[int, Storage]


_fields: 'FieldsDictType' = WeakValueDictionary()
_storages: 'StoragesDictType' = WeakValueDictionary()


def register_field(field: 'S3FileField') -> None:
    field_label = str(field)
    if field_label in _fields:
        raise Exception(f'Duplicate S3FileField declaration: {field_label}')
    _fields[field_label] = field

    storage = field.storage
    storage_label = id(storage)
    _storages[storage_label] = storage


def get_field(field_name: str) -> 'S3FileField':
    """Get an S3FileFields by its __str__."""
    return _fields[field_name]


def iter_fields() -> Iterator['S3FileField']:
    """Iterate over the S3FileFields in use."""
    return _fields.values()


def iter_storages() -> Iterator[Storage]:
    """Iterate over the unique Storage instances used by S3FileFields."""
    return _storages.values()
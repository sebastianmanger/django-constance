from __future__ import annotations

import json
import logging
import uuid
from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta
from decimal import Decimal
from typing import Any
from typing import Protocol
from typing import TypeVar

logger = logging.getLogger(__name__)

DEFAULT_DISCRIMINATOR = 'default'


class JSONEncoder(json.JSONEncoder):
    """Django-constance custom json encoder."""

    def default(self, o):
        for discriminator, (t, _, encoder) in _codecs.items():
            if isinstance(o, t):
                return _as(discriminator, encoder(o))
        raise TypeError(f'Object of type {o.__class__.__name__} is not JSON serializable')


def _as(discriminator: str, v: Any) -> dict[str, Any]:
    return {'__type__': discriminator, '__value__': v}


def dumps(obj, _dumps=json.dumps, cls=JSONEncoder, default_kwargs=None, **kwargs):
    """Serialize object to json string."""
    default_kwargs = default_kwargs or {}
    is_default_type = isinstance(obj, (str, int, bool, float, type(None), dict, list))
    return _dumps(
        _as(DEFAULT_DISCRIMINATOR, obj) if is_default_type else obj, cls=cls, **dict(default_kwargs, **kwargs)
    )


def loads(s, _loads=json.loads, **kwargs):
    """Deserialize json string to object."""
    return _loads(s, object_hook=object_hook, **kwargs)


def object_hook(o: dict) -> Any:
    """Hook function to perform custom deserialization."""
    if o.keys() == {'__type__', '__value__'}:
        if o['__type__'] == DEFAULT_DISCRIMINATOR:
            return o['__value__']
        codec = _codecs.get(o['__type__'])
        if not codec:
            raise ValueError(f'Unsupported type: {o["__type__"]}')
        return codec[1](o['__value__'])
    logger.error('Cannot deserialize object: %s', o)
    raise ValueError(f'Invalid object: {o}')


T = TypeVar('T')


class Encoder(Protocol[T]):
    def __call__(self, value: T, /) -> str: ...  # pragma: no cover


class Decoder(Protocol[T]):
    def __call__(self, value: str, /) -> T: ...  # pragma: no cover


def register_type(t: type[T], discriminator: str, encoder: Encoder[T], decoder: Decoder[T]):
    if not discriminator:
        raise ValueError('Discriminator must be specified')
    if _codecs.get(discriminator) or discriminator == DEFAULT_DISCRIMINATOR:
        raise ValueError(f'Type with discriminator {discriminator} is already registered')
    _codecs[discriminator] = (t, decoder, encoder)


_codecs: dict[str, tuple[type, Decoder, Encoder]] = {}


def _register_default_types():
    # NOTE: datetime should be registered before date, because datetime is also instance of date.
    register_type(datetime, 'datetime', datetime.isoformat, datetime.fromisoformat)
    register_type(date, 'date', lambda o: o.isoformat(), lambda o: datetime.fromisoformat(o).date())
    register_type(time, 'time', lambda o: o.isoformat(), time.fromisoformat)
    register_type(Decimal, 'decimal', str, Decimal)
    register_type(uuid.UUID, 'uuid', lambda o: o.hex, uuid.UUID)
    register_type(timedelta, 'timedelta', lambda o: o.total_seconds(), lambda o: timedelta(seconds=o))


_register_default_types()

"""
Kick API Wrapper
~~~~~~~~~~~~~~~~~~~
A basic wrapper for the Kick API.
"""

__version__ = "0.0.1"

from typing import Any, Literal, NamedTuple

from .assets import *
from .chatroom import *
from .client import *
from .emotes import *
from .enums import *
from .errors import *
from .livestream import *
from .message import *
from .object import *
from .user import *
from .videos import *


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int

    @classmethod
    def from_version(cls, ver: str):
        major, minor, micro = ver.split(".")
        releaselevel: Any = "f"
        if not micro.isdigit():
            releaselevel = micro[-1]
            micro = micro.removesuffix(releaselevel)
        self = cls(
            major=int(major),
            minor=int(minor),
            micro=int(micro),
            releaselevel={
                "a": "alpha",
                "b": "beta",
                "c": "candidate",
                "f": "final",
            }.get(
                releaselevel, "final"
            ),  # type: ignore
            serial=0,
        )
        return self


version_info: VersionInfo = VersionInfo.from_version(__version__)

del NamedTuple, Literal, VersionInfo, Any

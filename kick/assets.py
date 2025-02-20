from __future__ import annotations

import os
from io import BufferedIOBase
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from typing_extensions import Self

    from .http import HTTPClient
    from .types.assets import AssetOnlySrc, AssetSrcset

__all__ = ("Asset",)


class Asset:
    """
    A class which represents a kick asset.

    Attributes
    -----------
    url: str
        The asset's url
    """

    def __init__(self, *, url: str, http: HTTPClient) -> None:
        self.http = http
        self.url = url

    async def read(self) -> bytes:
        """
        |coro|

        Fetches the asset from kick

        Raises
        -----------
        HTTPException
            Fetching the asset failed
        NotFound
            Asset no longer exists

        Returns
        -----------
        bytes
            The asset's bytes
        """

        return await self.http.get_asset(self.url)

    async def save(
        self,
        fp: str | bytes | os.PathLike[Any] | BufferedIOBase,
        *,
        seek_begin: bool = True,
    ) -> int:
        """
        |coro|

        Saves the asset into a file-like object

        Parameters
        -----------
        fp: str | bytes | os.PathLike[Any] | BufferedIOBase
            The file-like object for the asset to be written to.
            If a filepath is given, then a file will be created instead.
        seek_begin: bool
            Whether to seek to the beginning of the file after saving is
            successfully done.

        Raises
        -----------
        HTTPException
            Fetching the asset failed
        NotFound
            Asset no longer exists

        Returns
        -----------
        int
            The amount of bytes written
        """

        data = await self.read()
        if isinstance(fp, BufferedIOBase):
            written = fp.write(data)
            if seek_begin:
                fp.seek(0)
            return written
        else:
            with open(fp, "wb") as f:
                return f.write(data)

    def __str__(self) -> str:
        return self.url

    def __len__(self) -> int:
        return len(self.url)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and other.url == self.url

    @classmethod
    def _from_asset_src(
        cls, *, data: AssetSrcset | AssetOnlySrc, http: HTTPClient
    ) -> Self:
        return cls(url=data["src"], http=http)

    @classmethod
    def _from_emote(cls, emote_id: int, /, *, http: HTTPClient) -> Self:
        return cls(url=f"https://files.kick.com/emotes/{emote_id}/fullsize", http=http)

    def __repr__(self) -> str:
        return f"<Asset url={self.url}>"

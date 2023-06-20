from typing_extensions import TypedDict


class AssetUrl(TypedDict):
    url: str


class AssetSrcset(TypedDict):
    src: str
    srcset: str


class AssetOnlySrc(TypedDict):
    src: str

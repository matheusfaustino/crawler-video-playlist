from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

@dataclass
class Season:
    title: str
    url: str


@dataclass
class Episode:
    name: str
    url: str


@dataclass
class File:
    detail_href: str
    description: str
    id: str
    name: str
    size: int
    views: int
    bandwidth_used: int
    bandwidth_used_paid: int
    downloads: int
    date_upload: datetime
    date_last_view: datetime
    mime_type: str
    thumbnail_href: str
    hash_sha256: str
    delete_after_date: datetime
    delete_after_downloads: int
    availability: str
    availability_message: str
    abuse_type: str
    abuse_reporter_name: str
    embed_domains: list[str]
    can_edit: bool
    can_download: bool
    show_ads: bool
    allow_video_player: bool
    download_speed_limit: int

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> File:
        return cls(
            detail_href=d["detail_href"],
            description=d["description"],
            id=d["id"],
            name=d["name"],
            size=d["size"],
            views=d["views"],
            bandwidth_used=d["bandwidth_used"],
            bandwidth_used_paid=d["bandwidth_used_paid"],
            downloads=d["downloads"],
            date_upload=_parse_dt(d["date_upload"]),
            date_last_view=_parse_dt(d["date_last_view"]),
            mime_type=d["mime_type"],
            thumbnail_href=d["thumbnail_href"],
            hash_sha256=d["hash_sha256"],
            delete_after_date=_parse_dt(d["delete_after_date"]),
            delete_after_downloads=d["delete_after_downloads"],
            availability=d["availability"],
            availability_message=d["availability_message"],
            abuse_type=d["abuse_type"],
            abuse_reporter_name=d["abuse_reporter_name"],
            embed_domains=d["embed_domains"],
            can_edit=d["can_edit"],
            can_download=d["can_download"],
            show_ads=d["show_ads"],
            allow_video_player=d["allow_video_player"],
            download_speed_limit=d["download_speed_limit"],
        )


@dataclass
class ApiResponse:
    id: str
    title: str
    date_created: datetime
    file_count: int
    files: list[File]
    can_edit: bool

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ApiResponse:
        return cls(
            id=d["id"],
            title=d["title"],
            date_created=_parse_dt(d["date_created"]),
            file_count=d["file_count"],
            files=[File.from_dict(f) for f in d["files"]],
            can_edit=d["can_edit"],
        )


@dataclass
class ViewerData:
    type: str
    api_response: ApiResponse
    captcha_key: str
    embedded: bool
    user_ads_enabled: bool
    theme_uri: str

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ViewerData:
        return cls(
            type=d["type"],
            api_response=ApiResponse.from_dict(d["api_response"]),
            captcha_key=d["captcha_key"],
            embedded=d["embedded"],
            user_ads_enabled=d["user_ads_enabled"],
            theme_uri=d["theme_uri"],
        )


def _parse_dt(value: str) -> datetime:
    # handles trailing 'Z' (UTC) and the 0001-01-01 sentinel
    return datetime.fromisoformat(value.replace("Z", "+00:00"))
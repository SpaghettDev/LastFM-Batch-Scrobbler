from typing import Union, NoReturn
from time import mktime
from os import _Environ
from json import load, JSONDecodeError
from datetime import datetime
import ciso8601


FORMATTED_SPOTIFY_DATA_KEYS1 = [
    "artistName", "albumName", "trackName", "time"
]
FORMATTED_SPOTIFY_DATA_KEYS2 = [
    "artistName", "albumName", "trackName", "time", "duration"
]
NONFORMATTED_SPOTIFY_DATA_KEYS = [
    "ts", "username", "platform", "ms_played",
    "conn_country", "ip_addr_decrypted",
    "user_agent_decrypted", "master_metadata_track_name",
    "master_metadata_album_artist_name",
    "master_metadata_album_album_name",
    "spotify_track_uri", "episode_name",
    "episode_show_name", "spotify_episode_uri",
    "reason_start", "reason_end", "shuffle", "skipped",
    "offline", "offline_timestamp", "incognito_mode"
]


class InvalidJSONFile(Exception):
    def __init__(message: str):
        super().__init__(f"The given JSON file is invalid! [{message}]")


def verify_env(env: _Environ):
    env_keys = [
        "LASTFM_API_KEY",
        "LASTFM_API_SECRET",

        "LASTFM_USERNAME",
        "LASTFM_HASHED_PASSWORD",
        # "LASTFM_PASSWORD"
    ]

    for _, e in enumerate(env_keys):
        if e == "LASTFM_HASHED_PASSWORD":
            try:
                env[e]
            except KeyError:
                env["LASTFM_PASSWORD"]

            break

        env[e]


def verify_data(data: list) -> None:
    try:
        assert (
            isinstance(data, list) and
            isinstance(data[0], dict) and
            (
                (
                    list(data[0].keys()) == FORMATTED_SPOTIFY_DATA_KEYS1 or
                    list(data[0].keys()) == FORMATTED_SPOTIFY_DATA_KEYS2
                ) or
                (
                    list(data[0].keys()) == NONFORMATTED_SPOTIFY_DATA_KEYS
                )
            )), \
            "Data must be an array of scrobbles!"
    except (KeyError, AssertionError) as e:
        raise InvalidJSONFile(e) from e


def convert_data(data: list) -> list:
    if list(data[0].keys()) == NONFORMATTED_SPOTIFY_DATA_KEYS:
        return [
            {
                "trackName": e["master_metadata_track_name"],
                "artistName": e["master_metadata_album_artist_name"],
                "albumName": e["master_metadata_album_album_name"],
                "time": e["ts"]
            } for _, e in enumerate(data)
        ]

    return data


def load_file(file: str) -> Union[list, None]:
    with open(file, "r") as f:
        try:
            data = load(f)

            verify_data(data)
            data = convert_data(data)

            return data
        except JSONDecodeError as e:
            raise InvalidJSONFile(e) from e


def convert_time(time: str) -> int:
    return mktime(
        ciso8601.parse_datetime(time).timetuple()
    )


def get_current_time() -> int:
    return int(mktime(datetime.now().timetuple()))


def halt() -> NoReturn:
    raise SystemExit

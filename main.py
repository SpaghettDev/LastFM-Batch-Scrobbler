#!/usr/bin/env python3

from os import environ
from sys import argv
from time import sleep
from pylast import LastFMNetwork, md5, NetworkError
from src.functions import verify_env, load_file, convert_time, get_current_time, halt

from dotenv import load_dotenv
load_dotenv()

try:
    LASTFM_NETWORK = LastFMNetwork(
        api_key=environ["LASTFM_API_KEY"],
        api_secret=environ["LASTFM_API_SECRET"],
        username=environ["LASTFM_USERNAME"],
        password_hash=environ.get(
            "LASTFM_HASHED_PASSWORD", md5(environ["LASTFM_PASSWORD"])
        )
    )
except NetworkError as e:
    print(f"Error connecting to the lastfm api! [{e}]")
    halt()
except KeyError as e:
    print(f"Could not find {e} in .env file!")
    print("Did you forget to fill the .env file?")
    halt()


def main():
    if len(argv) == 2:
        data = load_file(argv[1])

        response = input(
            f"Are you sure you want to scrobble {len(data)} tracks? [y/n] "
        ).lower()

        if not response == "y":
            halt()

        for i, e in enumerate(data):
            # 5 requests every second, half a second removed
            # to account for requests' time
            if i % 5 == 0:
                sleep(0.5)

            LASTFM_NETWORK.scrobble(
                artist=e["artistName"],
                title=e["trackName"],
                timestamp=get_current_time()#convert_time(e["time"])
                # can't scrobble before lastfm account creation date
            )
            print(
                f"""Scrobbled {i + 1} tracks """
                f"""[{
                    e["trackName"]
                } by {
                    e["artistName"]
                } on {
                    e["albumName"]
                } the {
                    e["time"]
                }]""")

        print(f"Finished scrobbling {len(data)} tracks.")

    elif len(argv) == 3 or len(argv) == 4:
        timestamp = 0
        if len(argv) == 4:
            timestamp = argv[3]

        # parse timestamp since it can be a unix timestamp or a text timestamp
        try:
            timestamp = int(timestamp)
        except ValueError:
            try:
                timestamp = convert_time(timestamp)
            except ValueError:
                pass

        artist_name = argv[1]
        artist_track = argv[2]

        LASTFM_NETWORK.scrobble(
            artist=artist_name,
            title=artist_track,
            timestamp=get_current_time() if timestamp == 0 else timestamp
        )

        print(f"Successfully scrobbled {artist_track} by {artist_name}.")
    else:
        print(
            "Usage:\n"
            "\t1) main.py file\n"
            """\t2) main.py "artist" "track" [timestamp]\n"""
            "*everything between brackets is optional*"
        )
        halt()


if __name__ == "__main__":
    main()

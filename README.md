# LastFM-Batch-Scrobbler
A simple script that batch scrobbles Spotify Data. Can also scrobble one song. <br/>
Related: [Spotify-Data-Splitter](https://github.com/SpaghettDev/Spotify-Data-Splitter)

## Setup:
1. Install python 3.8 or higher from [here](https://www.python.org/downloads)
2. Install the script using `git clone https://github.com/SpaghettDev/LastFM-Batch-Scrobbler` or click the green download button above
3. If you have installed using the green download button, extract the file somewhere
4. Open your preffered shell and `cd` into the directory containing the project
5. Fill the .env file with the information needed. For the API key and SECRET visit [the LastFM api creation page](https://www.last.fm/api/account/create)
6. Run `pip install -r requirements.txt` to install the needed dependency (pylast)

## Usage:
```shell
python main.py "path/to/data.json"
```
and
```shell
python main.py "artist" "track" [timestamp]
```

eg.:
1. Scrobbling a file
```shell
python main.py "path/to/data_split1.json"
```
2. Scrobbling a single track
  Right Now:
  ```shell
  python main.py "Kanye West" "No More Parties In LA"
  ```
  Specific Time (date):
  ```shell
  python main.py "Kanye West" "No More Parties In LA" 2023-08-09
  ```
  Specific Time (Unix Timestamp):
  ```shell
  python main.py "Kanye West" "No More Parties In LA" 1691586000
  ```

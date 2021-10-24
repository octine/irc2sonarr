# irc2sonarr

Simple python script for monitoring an IRC channel and push releases to Sonarr.

## Requirements 
* Requests https://pypi.org/project/requests/
* python >= 3.8

## Usage
```bash
python3 bot.py
usage: bot.py [-h] [--nick NICK] [--sonarr-ip SONARR_IP] [--sonarr-port SONARR_PORT]
              --sonarr-api-key SONARR_API_KEY --auth AUTH --tracker {tl,td}
```
Where AUTH is your tracker RSS key.

Example:
```bash
python3 bot.py --sonarr-api-key <api-key> --auth <rss-key> --tracker tl
```

## Supported Trackers
* Torrentleech
* Torrentday

Shouldn't be hard to add any tracker which use IRC and RSS.
## License
[MIT](https://choosealicense.com/licenses/mit/)
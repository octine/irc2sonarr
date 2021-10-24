import time
import argparse
import uuid
import trackers
from sonarr import SonarrApi
from irc import IRC


def main(sonarr, irc, conf):
    while True:
        try:
            for user, message in irc.receive():
                if user == conf['announcer']:
                    torrent_name, dl_link = conf['parser'](message, conf['rss_key'])
                    if (sonarr_response := sonarr.release_push(torrent_name, dl_link).json())['rejected']:
                        print('{}: Sonarr rejected torrent {}, {}'.format(time.asctime(), torrent_name, sonarr_response['rejections'][0]))
                    else:
                        print('{}: Sonarr accepted torrent {}'.format(time.asctime(), torrent_name))
        except KeyError:
            print('{}: Sonarr could not process torrent {}'.format(time.asctime(), torrent_name))
        except IndexError:
            print('{}: Could not find torrent name / id in message: {}'.format(time.asctime(), message))
        except KeyboardInterrupt:
            print('{}: Exiting...'.format(time.asctime()))
            irc.quit("https://github.com/octine/irc2sonarr")
            exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--nick', default="pybot_"+str(uuid.uuid4()).split('-')[0])
    parser.add_argument('--sonarr-ip', default="localhost")
    parser.add_argument('--sonarr-port', default=8989)
    parser.add_argument('--sonarr-api-key', required=True)
    parser.add_argument('--auth', required=True)
    parser.add_argument('--tracker', required=True, choices=trackers.trackers.keys())
    args = parser.parse_args()

    conf = trackers.trackers[args.tracker]
    conf['rss_key'] = args.auth

    sonarr = SonarrApi(args.sonarr_api_key, args.sonarr_ip, args.sonarr_port)

    irc = IRC()
    irc.connect(conf['server'], conf['port'], args.nick)
    irc.join(conf['channel'])

    # Enter main loop
    main(sonarr, irc, conf)

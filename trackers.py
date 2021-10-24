import re


def tl_parse(msg, rss_key):
    torrent_name, torrent_id = re.findall("(?<=Name:')(.*)(?=' up)(?:.*)(?<=torrent/)(.*)", msg)[0]
    torrent_name = torrent_name.replace(' ', '.')
    dl_link = 'https://www.torrentleech.org/rss/download/{id}/{key}/{name}.torrent'.format(
        id=torrent_id, key=rss_key, name=torrent_name)

    return torrent_name, dl_link


def td_parse(msg, rss_key):
    torrent_name, torrent_id = re.findall("(?<=\ )(.*)(?=\ -)(?:.*)(?<=\?id=)([0-9]*)", msg)[0]
    torrent_name = torrent_name.replace(' ', '.')[:-1]
    dl_link = "https://www.torrentday.com/download.php/{id}/{name}.torrent?torrent_pass={key}".format(
        id=torrent_id, key=rss_key, name=torrent_name)

    return torrent_name, dl_link


trackers = {
        'tl': {
            'server': "irc.torrentleech.org",
            'port': 7011,
            'parser': tl_parse,
            'announcer': "_AnnounceBot_",
            'channel': "#tlannounces"
        },
        'td': {
            'server': "irc.torrentday.com",
            'port': 6667,
            'parser': td_parse,
            'announcer': "TD_Announce",
            'channel': "#td.announce"
        }
    }

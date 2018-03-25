from utorrentapi import UTorrentAPI
import sys
import json

if __name__ == "__main__":
    # Arg1 Url, Arg3 Username, Arg4 Password
    client = UTorrentAPI(sys.argv[1], sys.argv[2], sys.argv[3])
    data = client.get_list()
    print(data)

    # Get torrent names
    torrents = {}
    for d in data["torrents"]:
        torrents[d[2]] = {
            "id": d[0]
        }
    print("Your torrents: " + json.dumps(torrents, indent=2))
    magnet = raw_input("Provide Magnet URL of torrent>> ")
    get = client.add_url(magnet)
    print(get)
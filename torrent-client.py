from utorrentapi import UTorrentAPI
import sys

if __name__ == "__main__":
    apiclient = UTorrentAPI(sys.argv[1], sys.argv[2], sys.argv[3])

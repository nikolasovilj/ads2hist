import argparse
from pathlib import Path
from os import walk
import sys
from tqdm import tqdm
from collections import OrderedDict
import json

argp = argparse.ArgumentParser()
argp.add_argument("search_path")
args = argp.parse_args()
target_dir = Path(args.search_path)

history = []

sys.stdout.flush() # didn't help with showing progress bar correctly
for root, dirs, files in tqdm(walk(target_dir), dynamic_ncols=False):
    for file in files:
        joined_path = Path(root).joinpath(file)
        if not joined_path.is_symlink():
            try:
                with open(str(joined_path) + ":zone.identifier") as f:
                    zone_info = f.read()
                    if "about:internet" not in zone_info and ("ReferrerUrl" in zone_info or "HostUrl" in zone_info):
                        hist_entry = OrderedDict()
                        print(joined_path)
                        hist_entry.update({"rel_file_path": str(joined_path)})
                        try:
                            referrerUrl = zone_info.split("\n")[2].split("ReferrerUrl")[1][1:]
                            hist_entry.update({"referrerUrl": referrerUrl})
                        except IndexError as e:
                            hist_entry.update({"referrerUrl": None})
                        print(referrerUrl)
                        try:
                            hostUrl = zone_info.split("\n")[3].split("HostUrl")[1][1:]
                            hist_entry.update({"hostUrl": hostUrl})
                        except IndexError as e:
                            hist_entry.update({"hostUrl": None})
                        print(hostUrl)
                        print()
                        history.append(hist_entry)
            except FileNotFoundError as e:
                pass

print(json.dumps(history, indent=4))
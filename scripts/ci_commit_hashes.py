from collections import defaultdict
import json
from pathlib import Path
import subprocess


PROJECT_ROOT_PATH = Path(__file__).parent.parent
# Firmware hashes mapped from commit hash
ALL_HASHES_PATH = PROJECT_ROOT_PATH / "firmware_hashes.json"
PROJECT_HASHES_PATH = PROJECT_ROOT_PATH / ".pio" / "firmware_hashes.json"


def get_commit_hash() -> str:
    return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()


if __name__ == "__main__":
    commit_hash = get_commit_hash()
    
    print("=" * 80)
    print("Commit hash:\t", commit_hash)
    print("=" * 80)

    all_hashes = defaultdict()
    if ALL_HASHES_PATH.exists():
        with open(ALL_HASHES_PATH, "r") as ff:
            all_hashes = json.load(ff)

    with open(PROJECT_HASHES_PATH, "r") as ff:
        hashes = json.load(ff)

    '''
    {
        GIT-HASH: {
            "env-1": FIRMWARE-HASH,
            "env-2": FIRMWARE-HASH,
            ...
        },
        ...
    }
    '''
    all_hashes[commit_hash] = hashes

    with open(ALL_HASHES_PATH, 'w') as ff:
        json.dump(all_hashes, ff, indent=4)

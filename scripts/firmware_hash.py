from collections import defaultdict
import hashlib
import json
from pathlib import Path

Import("env")

HASH_SIGNATURE = "BBASBBASBBASBBAS".encode('ascii')

# Firmware hashes for current project
# Local: .pio/firmware_hashes.json  
PROJECT_HASHES_PATH = Path(env['PROJECT_WORKSPACE_DIR']) / "firmware_hashes.json"


def save_hash(hash: str):
    print("Saving hash to\t", str(PROJECT_HASHES_PATH))

    hashes = defaultdict()
    if PROJECT_HASHES_PATH.exists():
        with open(PROJECT_HASHES_PATH, "r") as ff:
            hashes = json.load(ff)

    '''
    {
        "env-1": FIRMWARE-HASH,
        "env-2": FIRMWARE-HASH,
        ...
    }
    '''
    env_name = env['PIOENV']
    hashes[env_name] = hash

    with open(PROJECT_HASHES_PATH, 'w') as ff:
        json.dump(hashes, ff, indent=4)

# Calculate firmware hash using binary
def hash_file(file_path):

    ff = open(file_path, "rb+")
    data = ff.read()

    # First 8 bytes of SHA1 as string
    hash = hashlib.sha1(data).hexdigest()[:16]
    return hash


# Inject calculated hash into ELF file
def replace_firmware_hash(source, target, env):
    print("-" * 80)

    elf_path = target[0].get_abspath()
    elf = open(elf_path, 'rb+')
    elf_data = elf.read()

    hash = hash_file(elf_path)
    print("Firmware hash:\t", hash)
    
    save_hash(hash)

    offset = elf_data.find(HASH_SIGNATURE)
    assert offset != -1, "Firmware hash default signature not found"

    elf.seek(offset)
    elf.write(hash.encode('ascii'))
    elf.close()

    print("-" * 80)

# Find toolchain strip using gcc name
strip_tool = env['CC'].replace("gcc", "strip")

env.AddPostAction(
    "$BUILD_DIR/firmware.elf",
    [
        env.VerboseAction(" ".join([
            strip_tool, "--strip-unneeded", "\"$BUILD_DIR/firmware.elf\""
        ]), "Stripping symbols..."),
        replace_firmware_hash
    ]
)
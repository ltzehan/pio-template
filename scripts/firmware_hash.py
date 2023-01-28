import hashlib
import json
from pathlib import Path

Import("env")

HASH_DEFAULT = "BBASBBASBBASBBAS".encode('ascii')
HASHES_FNAME = "firmware_hashes.json"

def save_hash(env, hash: str):
    # Save hashes to .pio/
    workspace_dir = Path(env['PROJECT_WORKSPACE_DIR'])
    hashes_path = Path(workspace_dir / HASHES_FNAME)

    print("Saving hash to\t", str(hashes_path))

    hashes = None
    if not hashes_path.exists():
        hashes = {}
    else:
        with open(hashes_path, 'r') as ff:
            hashes = json.load(ff)

    env_name = env['PIOENV']
    hashes[env_name] = hash

    with open(hashes_path, 'w') as ff:
        json.dump(hashes, ff, indent=4)


def hash_file(file_path):

    ff = open(file_path, "rb+")
    data = ff.read()

    # First 8 bytes of SHA1 as string
    hash = hashlib.sha1(data).hexdigest()[:16]
    return hash


def replace_firmware_hash(source, target, env):
    print("-" * 80)

    elf_path = target[0].get_abspath()
    elf = open(elf_path, 'rb+')
    elf_data = elf.read()

    hash = hash_file(elf_path)
    print("Firmware hash:\t", hash)
    
    save_hash(env, hash)

    offset = elf_data.find(HASH_DEFAULT)
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
            strip_tool, "--strip-unneeded", "$BUILD_DIR/firmware.elf"
        ]), "Stripping symbols..."),
        replace_firmware_hash
    ]
)
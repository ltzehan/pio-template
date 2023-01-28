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

def get_hash(hex_path):

    # Read output HEX file
    hex = open(hex_path, "rb+")
    hex_data = hex.read()

    # First 8 byte of SHA1 as string
    hash = hashlib.sha1(hex_data).hexdigest()[:16]
    return hash


def replace_firmware_hash(source, target, env):
    print("-" * 80)

    # firmware.hex
    hex_path = target[0].get_abspath()

    # firmware.elf
    elf_path = Path(env['PROJECT_BUILD_DIR']) / env['PIOENV'] / "firmware.elf"
    elf = open(elf_path, 'rb+')
    elf_data = elf.read()

    # Compute hash from HEX file
    # Doesn't work with ELF because of random debug symbols and paths
    hash = get_hash(hex_path)
    print("Firmware hash:\t", hash)
    
    save_hash(env, hash)

    offset = elf_data.find(HASH_DEFAULT)
    assert offset != -1, "Firmware hash default signature not found"

    elf.seek(offset)
    elf.write(hash.encode('ascii'))
    elf.close()

    print("-" * 80)

env.AddPostAction(
    "$BUILD_DIR/firmware.elf",
    [
        replace_firmware_hash,
        env.VerboseAction(" ".join([
            "$OBJCOPY", "-O", "ihex", "-R", ".eeprom", 
            '"$BUILD_DIR/firmware.elf"', '"$BUILD_DIR/firmware.hex"'
        ]), "Re-building HEX file")
    ]
)
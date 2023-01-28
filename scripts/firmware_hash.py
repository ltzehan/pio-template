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

    print("Saving hash to ", str(hashes_path))

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

def replace_firmware_hash(source, target, env):
    elf_path = target[0].get_abspath()
    
    # Read output ELF file
    elf = open(elf_path, "rb+")
    elf_data = elf.read()

    # First 8 byte of SHA1 as string
    hash = hashlib.sha1(elf_data).hexdigest()[:16]
    save_hash(env, hash)

    print("-" * 60)
    print("Injecting firmware hash: ", hash)
    print("-" * 60)

    offset = elf_data.find(HASH_DEFAULT)
    assert offset != -1, "Firmware hash default signature not found"

    elf.seek(offset)
    elf.write(hash.encode('ascii'))
    elf.close()


env.AddPostAction("$BUILD_DIR/firmware.elf", replace_firmware_hash)

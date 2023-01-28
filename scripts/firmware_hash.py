import hashlib

Import("env")

HASH_DEFAULT = "BBASBBASBBASBBAS".encode('ascii')


def replace_firmware_hash(source, target, env):
    # Read output ELF file
    elf_path = target[0].get_abspath()
    elf = open(elf_path, "rb+")
    elf_data = elf.read()

    # First 8 byte of SHA1 as string
    hash = hashlib.sha1(elf_data).hexdigest()[:16]
    print("-" * 60)
    print("Injecting firmware hash: ", hash)
    print("-" * 60)

    offset = elf_data.find(HASH_DEFAULT)
    assert offset != -1, "Firmware hash default signature not found"

    elf.seek(offset)
    elf.write(hash.encode('ascii'))
    elf.close()


env.AddPostAction("$BUILD_DIR/firmware.elf", replace_firmware_hash)

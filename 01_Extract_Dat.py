import os, binascii, struct, lzss, shutil
from pathlib import Path

ror = lambda val, r_bits, max_bits: \
    ((val & (2 ** max_bits - 1)) >> r_bits % max_bits) | \
    (val << (max_bits - (r_bits % max_bits)) & (2 ** max_bits - 1))


def decrypt(file, start, end, key):
    b = bytearray(end-start)
    file_ptr = start
    while file_ptr < end:
        by = (ror(fileContent[file_ptr], 4, 8) ^ 255) - key[file_ptr % 16]
        if by < 0:
            by += 256
        b[file_ptr - start] = by
        file_ptr += 1
    return b


def decrypt_int(file, start, key):
    return int.from_bytes(decrypt(bin_file, start, start + 4, key), byteorder='little', signed=False)

key = b'*TGM4ABSOLUTEEYE'
align = int("0x800", 0)
folders = 1

filelist = []
file_count = 0
block_count = 0

shutil.copy("C:\Program Files (x86)\Steam\steamapps\common\TGM4\GAME.DAT", "GAME.DAT")
shutil.copy("C:\Program Files (x86)\Steam\steamapps\common\TGM4\INFO.DAT", "INFO.DAT")

with (open("INFO.DAT", mode='rb') as bin_file):
    fileContent = bin_file.read()
    key = bytes(fileContent[0:16])
    print("Key: " + str(fileContent[0:16]))
    align = decrypt_int(bin_file, 36, key)
    folders = decrypt_int(bin_file, 40, key)
    files = decrypt_int(bin_file, 44, key)
    file_end_pos = (files + 1) * 48
    print("Align: " + hex(align))
    print("Folders: " + hex(folders))
    print("Files: " + hex(files))

    file_ptr = 48
    filelist = []
    while file_ptr < file_end_pos:
        (name, pack_size, blockstart, blocks, unpack_size) = struct.unpack("<32sIIII", decrypt(fileContent, file_ptr, file_ptr + 48, key))
        print(name.rstrip(b'\x00').decode('ascii') + " has packed size " + str(hex(pack_size)) + ", block start " + str(hex(blockstart)) + ", # of blocks " + str(hex(blocks)) + ", and unpacked size " + str(hex(unpack_size)))
        l = list((name, pack_size, blockstart, blocks, unpack_size))
        filelist.append(l)
        file_ptr += 48

with (open("GAME.DAT", mode='rb') as game_file):
    fileContent = game_file.read()
    file_ptr = align
    gamedat_size = os.path.getsize("GAME.DAT")
    print("GAME.DAT expected size: " + str(hex((blockstart + blocks) * align)) + " vs. actual: " + str(hex(gamedat_size)))
    for file_data in filelist:
        name = "data/" + file_data[0].rstrip(b'\x00').decode('ascii')
        current_file = Path(name)
        current_file.parent.mkdir(exist_ok=True, parents=True)
        with (open(current_file, mode='wb') as out_file):
            print("Extracting " + out_file.name + ", expected size " + str(file_data[4]))
            if fileContent[file_data[2] * align:file_data[2] * align + 4] == b'ALZ1':
                out_file.write(lzss.decompress(fileContent[file_data[2] * align + 4:file_data[2] * align + file_data[1]], 0))
            else:
                out_file.write(fileContent[file_data[2] * align:file_data[2] * align + file_data[1]])
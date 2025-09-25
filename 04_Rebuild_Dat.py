import glob, os, lzss


ror = lambda val, r_bits, max_bits: \
    ((val & (2 ** max_bits - 1)) >> r_bits % max_bits) | \
    (val << (max_bits - (r_bits % max_bits)) & (2 ** max_bits - 1))


def encrypt(key_v, data, start_pos):
    b = bytearray(len(data))
    file_ptr = 0
    while file_ptr < len(data):
        by = data[file_ptr] + key_v[(file_ptr + start_pos) % 16]
        if by > 255:
            by -= 256
        b[file_ptr] = ror((by ^ 255), 4, 8)
        file_ptr += 1
    return b


def encrypt_int(key_v, int_v, start_pos):
    return encrypt(key_v, int_v.to_bytes(4, 'little'), start_pos)


key = b'*TGM4ABSOLUTEEYE'
align = int("0x800", 0)
folders = 1

filelist = []
file_count = 0
block_count = 0

with open("GAME_PATCH.DAT", "wb") as game:
    for root, dirs, files in os.walk("data"):
        for file in files:
            file_count += 1
            name = bytes(os.path.join(root, file).replace("data\\", "", 1).replace("\\", "/"), "utf-8")
            name += b'\x00' * (32 - len(name))
            #print(os.path.join(root, file))
            with open(os.path.join(root, file), "rb") as sb:
                bin_s = sb.read()
            try:
                source_f = os.path.join(root, file).replace("data", "datapatch")
                with open(source_f, "rb") as pb:
                    bin_p = pb.read()
            except FileNotFoundError:
                bin_p = bin_s
            if bin_p != bin_s:
                print("Adding modified file " + str(file) + " to GAME.DAT.")
                new_bin = bin_p
            else:
                new_bin = bin_s
            size = len(new_bin)
            if name.startswith(b'snd/'):
                #print("Not compressing the file: " + os.path.join(root, file))
                comp = new_bin
                csize = size
            else:
                comp = b'ALZ1' + lzss.compress(new_bin)
                csize = len(comp)
            # pad to alignment
            if (csize % align) != 0:
                comp += b'\xCD' * (align - (csize % align))
            game.write(comp)
            blocks = ((csize - 1) // align) + 1
            l = list((name, csize, block_count, blocks, size))
            block_count += blocks
            filelist.append(l)

with open("INFO_PATCH.DAT", mode='wb') as new_file:
    new_file.write(key)
    new_file.write(encrypt(key, bytearray(20), new_file.tell()))
    new_file.write(encrypt_int(key, align, new_file.tell()))
    new_file.write(encrypt_int(key, folders, new_file.tell()))
    new_file.write(encrypt_int(key, file_count, new_file.tell()))
    for f in filelist:
        new_file.write(encrypt(key, f[0], new_file.tell())) # name
        new_file.write(encrypt_int(key, f[1], new_file.tell())) # compressed size
        new_file.write(encrypt_int(key, f[2], new_file.tell())) # block start
        new_file.write(encrypt_int(key, f[3], new_file.tell())) # blocks
        new_file.write(encrypt_int(key, f[4], new_file.tell())) # uncompressed size
    new_file.write(bytearray(b'\x40') * (align * 3 - new_file.tell() % align))
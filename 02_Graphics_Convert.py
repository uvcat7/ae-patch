import glob, struct, os

formats = {
    0x00: "P8",
    0x07: "R8G8B8",
    0x08: "A8R8G8B8",
    0x09: "DXT1",
    0x0B: "DXT4",
    0x0D: "DXT5"
}

headers = {}

with open("tools/P8.dds", "rb") as f:
    headers["P8"] = f.read()[:0x80]
with open("tools/R8G8B8.dds", "rb") as f:
    headers["R8G8B8"] = f.read()[:0x80]
with open("tools/A8R8G8B8.dds", "rb") as f:
    headers["A8R8G8B8"] = f.read()[:0x80]
with open("tools/DXT1.dds", "rb") as f:
    headers["DXT1"] = f.read()[:0x80]
with open("tools/DXT4.dds", "rb") as f:
    headers["DXT4"] = f.read()[:0x80]
with open("tools/DXT5.dds", "rb") as f:
    headers["DXT5"] = f.read()[:0x80]

eff_files = glob.glob("data/**/*.eff", recursive=True)
eff_files.extend(glob.glob("data/**/*.mdl", recursive=True))
for file in eff_files:
    with open(file, "rb") as f:
        data = f.read()
        (entries, hdrsize) = struct.unpack("<xxxxxxHxxxxxxxxH", data[:18])
        for entry in range(entries):
            offset = 0x20 + (entry * 0x20)
            (fname, fsize, foffset) = struct.unpack("<16sxxxxLLxxxx", data[offset:offset + 0x20])
            fname = str(fname, "utf-8").rstrip("\0")
            if "\\" in file: file = file.replace("\\", "/")
            new_f = (file + "/" + fname).replace("data/", "dataeff/").replace(".tmp", "")
            print(f"\t{new_f} ({fsize} bytes)")
            if (new_f.endswith(".mdl") or new_f.endswith(".eff")):
                new_f = new_f + ".tmp"
                #print(f"Trying to recurse this file: {new_f}")
                eff_files.append(new_f)
            os.makedirs(os.path.dirname(new_f), exist_ok=True)
            with open(new_f, "wb") as of:
                of.write(data[foffset:foffset+fsize])

twx_files = glob.glob("data/**/*.twx", recursive=True)
twx_files.extend(glob.glob("dataeff/**/*.twx", recursive=True))
for file in twx_files:
    with open(file, "rb") as f:
        data = f.read()
        if len(data) < 0x30: continue
        (width, height, fmt, mipmaps) = struct.unpack("<xxxxxxxxHHHxB", data[:0x10])
        print(f"Converting {file}\n- Resolution: {width} x {height}\n- Format: {formats[fmt]}\n- Mipmaps: {mipmaps}\n- Size: {len(data)-0x30}\n")
        new_f = file.replace(".twx", ".dds")
        new_f = new_f.replace("data", "images", 1)
        new_f = new_f.replace("dataeff", "images", 1)
        os.makedirs(os.path.dirname(new_f), exist_ok=True)
        header = bytearray(headers[formats[fmt]])
        struct.pack_into("<LL", header, 0x0C, height, width)
        with open(new_f, "wb") as of:
            of.write(header)
            of.write(data[0x30:])
import glob, struct, os

# Copy all the .eff/.mdl files to datapatch so the next loop can overwrite changes
eff_files = glob.glob("data/**/*.eff", recursive=True)
eff_files.extend(glob.glob("data/**/*.mdl", recursive=True))
for file in eff_files:
    with open(file, "rb") as f:
        new_f = file.replace("data", "datapatch")
        os.makedirs(os.path.dirname(new_f), exist_ok=True)
        with open(new_f, "wb") as g:
            g.write(f.read())

dds_files = glob.glob("imageseff/**/*.dds", recursive=True)
for file in dds_files:
    with open(file, "rb") as f:
        source_data = f.read()
        if len(source_data) < 0x80: continue
        if "\\" in file: file = file.replace("\\", "/")
        # What's the master file we are writing to?
        current_pos = file.find(".")+4
        source_file = file[:current_pos].replace("imageseff/", "datapatch/")
        print(f"Placing {file} back into its source {source_file}")
        # Offset this by the .dds - .twx header size
        expected_size = os.path.getsize(file) - 0x50
        with open(source_file, "r+b") as out_f:
            subfile_start = 0x0
            dest_data = out_f.read()
            while current_pos < len(file):
                # What's the array index of the next file within the master file?
                current_pos = file.find(".", current_pos) + 4
                # We are searching for the next file down the directory tree
                file_name = (file[:current_pos].split("/"))[-1].replace(".dds", ".twx")
                (entries, hdrsize) = struct.unpack("<xxxxxxHxxxxxxxxH", dest_data[subfile_start:subfile_start + 18])
                found = False
                # Find the matching entry for file_name
                for entry in range(entries):
                    offset = 0x20 + (entry * 0x20)
                    (fname, fsize, foffset) = struct.unpack("<16sxxxxLLxxxx", dest_data[subfile_start + offset:subfile_start + offset + 0x20])
                    fname = str(fname, "utf-8").rstrip("\0")
                    if (fname == file_name):
                        found = True
                        break
                if (not found):
                    print(f"Can't find {file_name} starting at offset {subfile_start}, ignoring...")
                    fsize = 0
                    break
                subfile_start += foffset
            #print(f"File pos {subfile_start}, size {fsize}, expected size {expected_size}, last name {fname}")
            # Don't overwrite or underwrite data
            if (fsize == expected_size):
                out_f.seek(subfile_start + 0x30)
                out_f.write(source_data[0x80:])
            else:
                print(f"{file} is the wrong size (expected {fsize} got {expected_size}), so cannot be inserted back into {source_file}")

dds_files = glob.glob("images/**/*.dds", recursive=True)
for file in dds_files:
    with open(file, "rb") as f:
        data = f.read()
        if len(data) < 0x80: continue
        print(f"Converting {file} to .twx")
        new_f = file.replace(".dds", ".twx")
        new_f = new_f.replace("images", "datapatch", 1)
        orig_f = file.replace(".dds", ".twx")
        orig_f = orig_f.replace("images", "data", 1)
        os.makedirs(os.path.dirname(new_f), exist_ok=True)
        try:
            with open(orig_f, "rb") as tf:
                origdata = tf.read()
                header = origdata[:0x30]
                with open(new_f, "wb") as of:
                    of.write(header)
                    of.write(data[0x80:])
        except FileNotFoundError:
            print(f"{file} doesn't exist in source, probably .eff or .mdl")
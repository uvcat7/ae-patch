import glob, struct, os

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
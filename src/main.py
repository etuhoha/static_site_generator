import os
import shutil

def copy_dir(src_dir, tgt_dir):
    print(f"copying contents of dir: {src_dir} -> {tgt_dir}")
    if not os.path.exists(tgt_dir):
        os.mkdir(tgt_dir)

    fs = os.listdir(src_dir)
    for f in fs:
        sf = os.path.join(src_dir, f)
        tf = os.path.join(tgt_dir, f)
        if os.path.isfile(sf):
            print(f"copying file: {sf} -> {tf}")
            shutil.copy(sf, tf)
        else:
            copy_dir(sf, tf)

def main():
    src_dir = "./static"
    tgt_dir = "./public"
    if os.path.exists(tgt_dir):
        shutil.rmtree(tgt_dir)
    copy_dir(src_dir, tgt_dir)



main()

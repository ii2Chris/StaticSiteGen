import os
import shutil

def prepare_public(public: str):
    if os.path.exists(public):
        shutil.rmtree(public)
    os.makedirs(public, exist_ok=True)

def copy_dir(static: str, public: str) -> str:
    if not os.path.exists(static):
        raise FileNotFoundError(f"Static path does not exist: {static}")
    if not os.path.isdir(static):
        raise NotADirectoryError(f"Source is not a directory: {static}")

    for name in os.listdir(static):
           src_path = os.path.join(static, name)
           dst_path = os.path.join(public, name)

           if os.path.isdir(src_path):
               # debugging: print(f"Making dir: {dst_path}")
               os.makedirs(dst_path, exist_ok=True)
               copy_dir(src_path, dst_path)
           else:
               # debugging: print(f"Copying file: {src_path} -> {dst_path}")
               shutil.copy(src_path, dst_path)

import os, shutil
from zipfile import ZipFile

NAME = "TechReforged"


def get_files(directory):
    file_paths = []
    for root, _, files in os.walk(directory):
        for filename in files:
            file_paths.append(os.path.join(root, filename))
    return file_paths


# Cleanup
try:
    shutil.rmtree("./tmp/release")
except FileNotFoundError:
    pass
os.makedirs("./tmp/release")

# Copy Instance
shutil.copyfile(f"./{NAME}.prism", f"./tmp/release/{NAME}.zip")


# Create Server ZIP
with ZipFile("./tmp/release/server.zip", "w") as z:
    for f in get_files("./server/"):
        z.write(f)

import os
import os.path
import shutil

# make temp build folder
dest = os.path.join(os.getcwd(), "build")
if os.path.exists(dest):
    shutil.rmtree(dest)
os.mkdir(dest)

# copy source code in build folder
root_dir = os.path.join(os.getcwd(), "../")
shutil.copytree(os.path.join(root_dir, "sibyl"), os.path.join(dest, "sibyl"))
shutil.copy(os.path.join(root_dir, "config.json"), dest)

for subdir, dirs, files in os.walk(dest):
    for f in files:
        if f.endswith(".pyc"):
            # print(f)
            os.remove(os.path.join(subdir, f))

# remove zip build
if os.path.exists("./sibyl.release.zip"):
    os.remove("./sibyl.release.zip")

print("generate release build: sibyl.release.zip")
shutil.make_archive("./sibyl.release", "zip", dest)
shutil.rmtree(dest)

import os
import os.path
import shutil

# make temp build folder
release_dir = os.path.dirname(os.path.abspath(__file__))
dest = os.path.join(release_dir, "build")
if os.path.exists(dest):
    shutil.rmtree(dest)
os.mkdir(dest)

# copy source code in build folder
root_dir = os.path.join(release_dir, "../")
shutil.copytree(os.path.join(root_dir, "sibyl"), os.path.join(dest, "sibyl"))
shutil.copy(os.path.join(root_dir, "config.json"), dest)

for subdir, dirs, files in os.walk(dest):
    for f in files:
        if f.endswith(".pyc"):
            # print(f)
            os.remove(os.path.join(subdir, f))

# remove zip build
zipfile = os.path.join(release_dir, "sibyl.release.zip")
if os.path.exists(zipfile):
    os.remove(zipfile)

print("generate release build: sibyl.release.zip")
shutil.make_archive(os.path.join(release_dir, "sibyl.release"), "zip", dest)
shutil.rmtree(dest)

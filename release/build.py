import os
import os.path
import shutil


print(os.getcwd())

for filename in os.listdir(os.path.join(os.getcwd(), "../")):
    if filename.endswith(".pyc"):
        print(filename)
        os.remove(filename)
    else:
        print("not remove %s", filename)

shutil.make_archive("./sibyl.release.zip",
                    "zip",
                    os.path.join(os.getcwd(), "../"))

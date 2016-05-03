import os
for fileName in os.listdir("."):
    os.rename(fileName, fileName.replace("test_v3", "test_v4"))

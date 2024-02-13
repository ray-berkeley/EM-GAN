import os
import subprocess
import argparse

parser = argparse.ArgumentParser(
    description="Parser for user-specifiable dataset paths."
)

parser.add_argument("dataset_dir", type=str, help="The directory for the dataset")

args = parser.parse_args()

dataset_dir = os.path.normpath(args.dataset_dir)
output_dir = dataset_dir + "_output"
flagPath = os.path.join(dataset_dir, "flag_dir/")

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

map_mrc = {}


def avg():
    for i in map_mrc:
        idx = map_mrc[i].index(0)
        w = "\n".join(map_mrc[i][:idx])
        tmpF = open(os.path.join(flagPath, "tmpF"), "w")
        tmpF.write(w)
        tmpF.close()
        print("./MergeMap -l " + os.path.join(flagPath, "tmpF"))
        exe = "./MergeMap -l " + os.path.join(flagPath, "tmpF")
        proc = subprocess.Popen(exe, shell=True)
        proc.wait()

        # Move hardcoded output from MergeMap binary exe
        output_filename = "Merged.mrc"
        new_output_filename = dataset_dir + "_Merged.mrc"
        os.rename(output_filename, new_output_filename)

        print(i + " done")


flagPath = os.path.join(dataset_dir, "flag_dir/")
srPath = os.path.join(dataset_dir, "sr_hr_lr/")

sr_imageFileNames = [
    os.path.join(srPath, x) for x in os.listdir(dataset_dir) if "SR" in x
]

print(srPath)
print(len(sr_imageFileNames))
for f in sr_imageFileNames:
    filename = f.split("/")[-1].split(".")[0]
    key = filename.split("_")[0]
    idx = int(filename.split("_")[-1])
    if key not in map_mrc:
        ARR = [0] * 12100
        ARR[idx] = f
        map_mrc[key] = ARR

    else:
        map_mrc[key][idx] = f
avg()

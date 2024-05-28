import glob, os

for name in glob.glob('Flask Restful API/*'):
    if os.path.isfile(name):
        print(name, "\n")
        f = open(name, "r")
        for x in f:
            print(x)
        
    print("------------------", "\n")

# python .\01_read_and_save_files.py >> data.txt
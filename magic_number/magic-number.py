import glob
import os

file = glob.glob('./magic_number/*')

bi1, bi2, bi3 = [], [], []   # ループの前で初期化

for i in file:
    if os.path.isfile(i):
        with open(i,'rb') as f:
            binaly = f.read(16).hex()
        if binaly.startswith('89504e47'):      # PNG
            bi1.append(i)
        elif binaly.startswith('52617221'):    # RAR
            bi2.append(i)
        elif binaly.startswith('ffd8ffe0'):    # JPEG
            bi3.append(i)
        
try:
    print(bi1,bi2,bi3)
except Exception as e:
    print("ファイルが見つからない")
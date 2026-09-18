import hashlib
import glob

def openhash():
    txtlist = [
    'aff02d6ad353ebf547f3b1f8ecd21efd7931e356f3930ab5ee502a391c5802d7',
    '8428f87e4dbbf1e95dba566b2095d989f5068a5465ebce96dcdf0b487edb8ecb',
    'e82f6ff15ddc9d67fc28c4b2c575adf7252d6e829af55c2b7ac1615b304d8962',
]
    # フォルダの中にあるtxtファイルパスを読み込む処理
    file = glob.glob('./hash/*.txt')

    for path in file:
        # rbをつかってバイトで読み込み
        with open(path,'rb') as f:
            hashed = f.read()
        hash256 = hashlib.sha256(hashed).hexdigest()

        if hash256 in txtlist:
            txtlist.append(path)
    
    return print(txtlist)

openhash()

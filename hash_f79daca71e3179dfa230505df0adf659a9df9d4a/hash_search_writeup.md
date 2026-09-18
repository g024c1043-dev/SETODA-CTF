# CTF解説: ハッシュ値でファイルを特定する問題

## 問題概要
複数のテキストファイルの中から、指定された3つの **SHA-256 ハッシュ値** を持つファイルを探し出す。

- 目的のハッシュ:
  - `aff02d6ad353ebf547f3b1f8ecd21efd7931e356f3930ab5ee502a391c5802d7`
  - `8428f87e4dbbf1e95dba566b2095d989f5068a5465ebce96dcdf0b487edb8ecb`
  - `e82f6ff15ddc9d67fc28c4b2c575adf7252d6e829af55c2b7ac1615b304d8962`

## 前提知識

| 用語 | 説明 |
|------|------|
| SHA-256 | ファイル内容から固定長(64文字の16進)の値を作る計算。同じ内容なら必ず同じ値になるため「ファイルの指紋」として使える |
| hashlib | Pythonの標準ライブラリ。ハッシュ計算を行う |
| glob | パターンに合うファイル名の一覧を取得する標準ライブラリ。`*` は任意の文字列 |
| バイナリ読み込み (`'rb'`) | ファイルをバイト列として読む方法。ハッシュ計算にはバイト列を渡す |

## 解法の流れ

1. `glob` でフォルダ内の全txtファイルのパスを取得
2. ループで1ファイルずつ `open(path, 'rb')` で開く
3. `hashlib.sha256(data).hexdigest()` でハッシュ計算
4. 計算結果を「目的のハッシュ3つ」と照合
5. 一致したパスをリストに追加

## つまずきポイント
- **比較相手を間違える**: ファイルの中身どうしではなく、**計算したハッシュ値** と **目的のハッシュ文字列** を比べる
- **型の不一致**: `'rb'` で読むとバイト列(bytes)。`hexdigest()` の結果は文字列(str)。bytes と str は一致しないため、照合は str どうしで行う
- **判定は `in` を使う**: 目的ハッシュをリストにして `if hash256 in targets:` とすると簡潔

## 完成コード

```python
import hashlib
import glob

targets = [
    'aff02d6ad353ebf547f3b1f8ecd21efd7931e356f3930ab5ee502a391c5802d7',
    '8428f87e4dbbf1e95dba566b2095d989f5068a5465ebce96dcdf0b487edb8ecb',
    'e82f6ff15ddc9d67fc28c4b2c575adf7252d6e829af55c2b7ac1615b304d8962',
]

def openhash():
    txtlist = []
    for path in glob.glob('./hash/*.txt'):
        with open(path, 'rb') as f:
            data = f.read()
        hash256 = hashlib.sha256(data).hexdigest()
        if hash256 in targets:
            txtlist.append(path)
    return txtlist

print(openhash())
```

## ポイントまとめ
- ハッシュは「内容の指紋」→ 内容比較ではなくハッシュ比較で探す
- 計算結果(str)と目的値(str)を揃えて比較する
- `glob` + ループで複数ファイルを一括処理

# setodaCTF 問題 解説：pcapからHTTPオブジェクトを抽出（flag.png）

## 問題概要
`.pcap` ファイル（`tkys_never_die.pcap`）を解析してフラグを見つける。

## 解法の流れ

### 1. 通信内容を確認
pcap内のHTTP通信を確認すると、2つのリクエストがあった。
```
GET /flag.html HTTP/1.1
GET /flag.png  HTTP/1.1   (Referer: .../flag.html)
```
- `flag.html` が画像 `flag.png` を読み込む構成。
```html
<img src="./flag.png" alt="flag.png" title="The Flag">
```

### 2. HTTPオブジェクトをエクスポート
Wiresharkの機能でやり取りされたファイルを取り出す。

**File → Export Objects → HTTP**

- **Export Objects**：pcapに記録された、通信でやり取りされたファイル（HTML・画像など）を丸ごと復元・保存する機能。
- 一覧から `flag.png` を選んで保存。

### 3. 画像を開いてフラグ確認
取り出した `flag.png` を開くと、フラグが画像として書かれていた。

## フラグ
```
flag{a_treasure_trove}
```

## ポイント
- pcapには通信でやり取りされた**ファイルそのもの**が入っている。
- 平文HTTPなら、画像やHTMLをそのまま復元できる。
- **Export Objects → HTTP** が定番の抽出手段。フラグが画像・ファイルに埋め込まれている問題で有効。

## 補足：コマンドでの抽出
Wiresharkが無くても、pcapのTCPペイロードからPNGのバイト列（`\x89PNG` 〜 `IEND`）を切り出せば画像を復元できる。
- PNGは必ず `89 50 4E 47`（`.PNG`）で始まり `IEND` で終わる。この範囲を抜き出す。

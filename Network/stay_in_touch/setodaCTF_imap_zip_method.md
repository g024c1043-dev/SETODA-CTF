# setodaCTF 問題 解説：IMAPメールからパスワード付きZIPを取り出す

## 問題概要
ある人物の通信を監視し、やりとりの内容を明らかにする。
通信データファイル（`stay_in_touch.pcapng`）を解析してフラグを見つける。

## 前提知識
- **IMAP**：メールを受信・閲覧するための通信の仕組み。
- **IMF（Internet Message Format）**：メール本文の標準形式（件名・本文・添付などの構造）。
- **MIMEエンコード**：メールで日本語や添付を送るための変換。件名の `=?UTF-8?B?...?=` の `?B?` はBase64を意味する。
- **boundary（境界線）**：メールで複数パート（本文・添付など）を区切る `--------------XXXX` の線。

## 解法の流れ

### 1. メールのやり取りを確認
IMAP通信の中に業務メールが往復していた。
件名は MIME(Base64) エンコードされているのでデコードして内容を把握。

### 2. 添付ファイルを発見
メールのパートに添付の記述があった。
```
Content-Type: application/x-zip-compressed;
 name="Report-AV-T0097.zip"
Content-Transfer-Encoding: base64
Content-Disposition: attachment;
 filename="Report-AV-T0097.zip"

UEsDBBQ...（Base64データ）...ewAAAAAA
--------------E3A9...--
```

### 3. 添付の範囲を見極める
- **ヘッダ部分**（`Content-Type:` 等）→ 保存には含めない。
- **空行の後のBase64**（`UEsD...` 〜 `...AAAAAA`）→ これが添付本体。
- **末尾の境界線**（`--------------XXXX--`）→ 含めない。
- 目印：ZIPのBase64は必ず `UEsD` で始まる（デコードすると `PK\x03\x04`）。

### 4. Base64をデコードしてZIPに復元
Base64部分だけを `enc.txt` に保存し、以下でデコード。

```python
import base64

with open('./enc.txt') as f:
    data = f.read().replace('\n', '').replace('\r', '').replace(' ', '').strip()

decoded = base64.b64decode(data)

with open('Report-AV-T0097.zip', 'wb') as f:
    f.write(decoded)

print('先頭バイト:', decoded[:4])  # b'PK\x03\x04' ならZIP成功
```

コマンドでも可：
```bash
base64 -d enc.txt > Report-AV-T0097.zip
```

### 5. ZIPを確認・解凍
```bash
file Report-AV-T0097.zip       # Zip archive data と出ればOK
unzip -l Report-AV-T0097.zip   # 中身の一覧
unzip Report-AV-T0097.zip      # 解凍（パスワードを要求される）
```

### 6. パスワードを本文から探す
ZIPはパスワード保護されていた。「やりとりの内容を明らかに」がヒント。
- メール本文に「パスワードは別にお送りします」と予告あり。
- パスワードは**別のメール**に記載されている（メールの慣習）。
- 検索方法：
  - Wireshark：`Edit → Find Packet` → Packet bytes / String で `パスワード` を検索。
  - コマンド：`strings stay_in_touch.pcapng | grep -i -E "パスワード|password"`
- 検索結果の先頭に文字化け（制御データのノイズ）が付くことがあるが、その後ろの読める文字列がパスワード本体。

### 7. パスワードで解凍してフラグ確認
```bash
unzip -P "見つけたパスワード" Report-AV-T0097.zip
cat Report-AV-T0097.txt
```
- `-P` … パスワード指定。記号やハイフンを含む場合は `" "` で囲む。

## 補足：ファイルの読み書きモード（r / rb / w / wb）
- 対象が**文字**（テキスト・Base64・HTML等）→ `r`（読み）/ `w`（書き）
- 対象が**生データ**（画像・ZIP・pcap等）→ `rb`（読み）/ `wb`（書き）
- 今回：`enc.txt`（文字）は `r`、デコード結果のZIP（生データ）は `wb`。
- `base64.b64decode()` の出力は必ずバイト（生データ）なので保存はいつも `wb`。
- 見分け方：テキストエディタで開いて記号だらけなら `rb`、読めるなら `r`。

## ポイント
- メールの件名・添付・本文はエンコード（Base64/MIME）されていることが多い。まずデコード。
- 添付の切り出しは boundary と空行が目印。ZIPは `UEsD`（＝`PK`）で始まる。
- 「パスワードは別送」はメールの慣習。会話を最後まで読むのが鍵。
- 表向きの内容はカモフラージュ。本命は添付ファイルとパスワードのやり取り。

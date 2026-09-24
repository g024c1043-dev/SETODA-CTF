# setodaCTF 問題 解説：ICMPパケットに隠されたフラグ（ICMPトンネリング）

## 問題概要
`.pcap` ファイル（`echo_request.pcap`）を解析してフラグを見つける。
ファイル名の `echo_request` がヒント。

## 前提知識
- **ICMP echo request**：`ping`（相手が生きているか確認するコマンド）が送る信号。「聞こえますか?」と呼びかけるパケット。
- **ICMPトンネリング**：本来ping用のICMPパケットの中に、こっそりデータを紛れ込ませて通信する手口。ファイル名・フラグの元ネタ。
- **T1095**：MITRE ATT&CK（攻撃手口の分類表）での、ICMP等を使った通信の番号。

## 解法の流れ

### 1. ICMPパケットを確認
pcap内のICMP echo request（type=8）を調べると、2種類あった。

| データ長 | 中身 | 正体 |
|---------|------|------|
| 56バイト | `\x10\x11\x12...` の決まったパターン | 普通のping（囮） |
| **1バイト** | 1文字だけ | ここにフラグが1文字ずつ埋め込み |

### 2. 1バイトのパケットだけ抽出
Wiresharkの表示フィルタ：
```
icmp && data.len == 1
```
- `icmp` … ICMP通信だけ表示
- `data.len == 1` … データ部分が1バイトのものだけ

出てきたパケットのdata（1文字）を送信順に並べる。

### 3. 文字を連結
並べた1バイトを連結すると：
```
.....flag{ICMP_Tunneling_T1095}.....
```
前後の `.` は区切り。中央の `flag{...}` がフラグ。

## フラグ
```
flag{ICMP_Tunneling_T1095}
```
※ `Tunneling` は **n が2つ**。1つ抜けやすいので注意。

## 抽出を効率化する方法

### tshark（コマンド版Wireshark）で一発
```bash
tshark -r echo_request.pcap -Y "icmp && data.len==1" -T fields -e data | tr -d '\n' | xxd -r -p
```
- `-Y` … 表示フィルタ
- `-T fields -e data` … データ部分だけ抜き出す
- `xxd -r -p` … 16進数を文字に変換

### Wiresharkだけで保存したい場合
1. フィルタ `icmp && data.len == 1` を適用
2. data値を右クリック → **Apply as Column**（列に追加）
3. **File → Export Packet Dissections → As CSV** で保存
（※ 1バイトずつの自動連結機能は無いので、連結はエクスポート後に行う）

### Python（scapy）で抽出
```python
from scapy.all import rdpcap, ICMP, Raw
pkts = rdpcap('echo_request.pcap')
s = b''
for p in pkts:
    if p.haslayer(ICMP) and p[ICMP].type == 8 and p.haslayer(Raw):
        d = bytes(p[Raw].load)
        if len(d) == 1:
            s += d
print(s.decode())
```

## ポイント
- ファイル名やフラグ内容（`echo_request`, `ICMP_Tunneling`）が解法のテーマを示していた。
- ping（ICMP）のデータ部分は自由に書き換えられるため、情報を隠す定番手口。
- 「データ長が普通と違うパケット」を見つけるのが突破口。フィルタで長さを条件にすると効率的。

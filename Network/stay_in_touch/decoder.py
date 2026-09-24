import base64

with open('./enc.txt') as f:
    data = f.read().replace('\n', '').replace('\r', '').strip()

decoded = base64.b64decode(data)

with open('Report-AV-T0097.zip', 'wb') as f:
    f.write(decoded)

print('保存完了', len(decoded), 'バイト')
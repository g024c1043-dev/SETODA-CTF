from PIL import Image

img = Image.open('./stegano.png')
pixels = list(img.getdata())

bits = ''
for px in pixels:
    for value in px[:3]:
        bits += str(value & 1)
        
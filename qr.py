import qrcode
img = qrcode.make("hello world")
img.save("qr.png")
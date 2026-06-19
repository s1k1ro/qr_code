import qrcode
import argparse

def main():
    #create the parser object
    parser = argparse.ArgumentParser(description="Generate QR Code base on CLI input")

    #first postiional argument
    parser.add_argument("url", help="The URL to encode")
    args = parser.parse_args()

    img = qrcode.make(args.url)
    img.save("qr.png")

if __name__ == "__main__":
    main()

#img = qrcode.make("hello world")
#oimg.save("qr.png")
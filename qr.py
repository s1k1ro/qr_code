import qrcode
import argparse

def main():
    #create the parser object
    parser = argparse.ArgumentParser(description="Generate QR Code base on CLI input")

    #first postiional argument
    parser.add_argument("url", help="The URL to encode")
    #optional arguments
    parser.add_argument("-o", "--output", help="output file name and type e.g myqr.png", default="qr.png")
    args = parser.parse_args()

    if not args.url.strip (): #.strip()removes spaces so "  " also becomes false
        print("You are missing the url")
        return
    
    img = qrcode.make(args.url)
    try:
        img.save(args.output)
        print(f"Successfully saved {args.output}")
    except Exception as e:
        print(f"Error: Couldnt save file. {e}")

if __name__ == "__main__":
    main()

#img = qrcode.make("hello world")
#oimg.save("qr.png")
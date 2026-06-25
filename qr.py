import qrcode 
import argparse

def main():

    

    parser = argparse.ArgumentParser(description="Generate QR Code base on CLI input")

    #positional arguments 
    #--consider maybe version size border can all be optional
    parser.add_argument("data", help="The URL or data to encode")   

    #optional arguments
    parser.add_argument("-o", "--output", help="output file name and type e.g myqr.png", default="qr.png")
    parser.add_argument("-v", "--version", type=int,  help="The version parameter is an int from 1 to 40 that cotnrols the size of the QR Code (smallest is 1)", default=None)
    parser.add_argument("-s", "--size", type=int, help="the size parameter controls how many pixels each 'box' of the QR code is", default = 10)
    parser.add_argument("-b","--border", type=int,  help="the border paramater contols how many boxes thick the border should be the (default is 4 minimum from specs)", default=4)
    parser.add_argument("-bc","--back-colour", help="control background colour, accepts colour name in string format", default="white")
    parser.add_argument("-fc","--fill-colour", help="control fill colour, accepts colour name in string format", default="black")
    parser.add_argument("-l", "--level", choices=["L","M","Q","H"], default = "L", help="Error correction level (L, M, Q, H)"  )
    
    args = parser.parse_args()

    error_levels = {
        "L": qrcode.constants.ERROR_CORRECT_L,
        "M": qrcode.constants.ERROR_CORRECT_M,
        "Q": qrcode.constants.ERROR_CORRECT_Q,
        "H": qrcode.constants.ERROR_CORRECT_H,
    }

    selected_level = error_levels[args.level]

    if not args.data.strip():
        print("You are missing the url/required data")
        return
    
    qr = qrcode.QRCode(
        version= args.version,
        error_correction=selected_level,
        box_size= args.size,
        border= args.border,
    )

    qr.add_data(args.data)
    qr.make(fit=True)

    img= qr.make_image(fill_color = args.fill_colour, back_color = args.back_colour)

    try:
        img.save(args.output)
        print(f"Successfully saved {args.output}")
    except Exception as e:
        print(f"Error: Couldnt save file. {e}")

if __name__ == "__main__":
    main()

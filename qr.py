import argparse
import qrcode

def pass_args():

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

    return parser

def get_error_level(level_key):


    error_levels = {
        "L": qrcode.constants.ERROR_CORRECT_L,
        "M": qrcode.constants.ERROR_CORRECT_M,
        "Q": qrcode.constants.ERROR_CORRECT_Q,
        "H": qrcode.constants.ERROR_CORRECT_H,
    }

    return error_levels.get(level_key, qrcode.constants.ERROR_CORRECT_L)

def is_valid_data(input):

    if input.strip() == "":
        return False
    
    return True

def build_qr(version, level, size, border):
    qr = qrcode.QRCode(
        version= version,
        error_correction= level,
        box_size= size,
        border= border,
    )

    return qr

def create_image(qr_object, fill_colour, back_colour):
    return qr_object.make_image(fill_color=fill_colour, back_color=back_colour)

def save_image(image_object, output_path):
    try:
        image_object.save(output_path)
        print(f"Successfully saved {output_path}")
    except Exception as e:
        print(f"Error: Couldnt save file. {e}")


def main():

    parser = pass_args()

    args = parser.parse_args()

    selected_level = get_error_level(args.level)

    if not is_valid_data(args.data):
        print("You are missing the url/required data")
        return

    qr = build_qr(
        version=args.version, 
        level=selected_level, 
        size=args.size, 
        border=args.border
        )
    
    qr.add_data(args.data)
    qr.make(fit=True)

    img = create_image(qr, args.fill_colour, args.back_colour)

    save_image(img, args.output)

if __name__ == "__main__":
    main()
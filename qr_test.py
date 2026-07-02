import argparse
import qrcode
import csv 


def pass_args():

    parser = argparse.ArgumentParser(description="Generate QR Code base on CLI input")

    #positional arguments 
    #--consider maybe version size border can all be optional
    parser.add_argument("data", nargs="?", default=None,  help="The URL or data to encode")   

    #optional arguments
    parser.add_argument("-o", "--output", help="output file name and type e.g myqr.png", default="qr.png")
    parser.add_argument("-v", "--version", type=int,  help="The version parameter is an int from 1 to 40 that cotnrols the size of the QR Code (smallest is 1)", default=None)
    parser.add_argument("-s", "--size", type=int, help="the size parameter controls how many pixels each 'box' of the QR code is", default = 10)
    parser.add_argument("-b","--border", type=int,  help="the border paramater contols how many boxes thick the border should be the (default is 4 minimum from specs)", default=4)
    parser.add_argument("-bc","--back-colour", help="control background colour, accepts colour name in string format", default="white")
    parser.add_argument("-fc","--fill-colour", help="control fill colour, accepts colour name in string format", default="black")
    parser.add_argument("-l", "--level", choices=["L","M","Q","H"], default = "L", help="Error correction level (L, M, Q, H)")
    parser.add_argument("-t", "--type", choices=["text", "url", "wifi", "vcard"], default="text", help="how to interpret the data: raw text, a link, wifi credentials, or a contact card")
    parser.add_argument("--ssid", help="ssid for wifi network (used with type=wifi)")
    parser.add_argument("--password", help="password for wifi netwrok (used with type=wifi)")
    parser.add_argument("--first-name", help="First Name for vcard output(used with type=vcard)")
    parser.add_argument("--last-name", help="Last Name for vcard output(used with type=vcard)")
    parser.add_argument("--phone", help="phone number for vcard output(used with type=vcard)")
    parser.add_argument("--email", help="email address for vcard output(used with type=vcard)")
    parser.add_argument("--batch", help="accepts a string (the path to the CSV file)", default=None)


    return parser

def get_error_level(level_key):


    error_levels = {
        "L": qrcode.constants.ERROR_CORRECT_L,
        "M": qrcode.constants.ERROR_CORRECT_M,
        "Q": qrcode.constants.ERROR_CORRECT_Q,
        "H": qrcode.constants.ERROR_CORRECT_H,
    }

    return error_levels.get(level_key, qrcode.constants.ERROR_CORRECT_L)

def is_valid_data(input, input_type, ssid, password, first_name, last_name):
    if input_type == "text" or input_type == "url":
        if input is None or input.strip() == "":
            print("You are missing the url/required data")
            return False
    if input_type == "wifi":
        if ssid is None or password is None:
            print("wifi output needs --ssid and --password")
            return False
    if input_type == "vcard":
        if first_name is None and last_name is None:
            print("vcard needs --first-name or --last-name")
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

def format_text(text: str):
    return text

def format_url(url: str):
    if not url.startswith("http://") and not url.startswith("https://"):
        print("Warning: no scheme detected, prepending https://")
        url = "https://" + url
    
    return url

def format_wifi(ssid, password):
    wifi_str = f"WIFI:S:{ssid};T:WPA;P:{password};;"
    return wifi_str

def format_vcard(first_name, last_name, phone, email):

    safe_first = first_name or ""
    safe_last = last_name or ""

    lines = ["BEGIN:VCARD", "VERSION:3.0"]
    lines.append(f"N:{safe_last};{safe_first}")
    lines.append(f"FN:{(safe_first + ' ' + safe_last).strip()}")

    if phone is not None:
        lines.append(f"TEL:{phone}")
    if email is not None:
        lines.append(f"EMAIL:{email}")
    
    lines.append("END:VCARD")

    return "\n".join(lines)

def normalize_row(row):

    #int withd defauls
    int_fields = ["size","border","version"]

    for field in row:
        if field not in int_fields:
            if row[field].strip() == "":
                row[field] = None
        elif field == "size":
            if row["size"].strip() == "":
                row["size"] = 10
            else:
                row["size"] =int(row["size"])
        elif field == "border":
            if row["border"].strip() == "":
                row["border"] = 4
            else:
                row["border"] =int(row["border"])
        elif field == "version":
            if row["version"].strip() == "":
                row["version"] = None
            else:
                row["version"] = int(row["version"])

    return row



def proccess_one(job):

    selected_level = get_error_level(job["level"])

    if not is_valid_data(
        input=job["data"], 
        input_type=job["type"],
        ssid=job["ssid"],
        password=job["password"], 
        first_name=job["first_name"],
        last_name=job["last_name"]
    ):
        raise ValueError("validation failed")

    if job["type"] == "text":
        formatted_data = format_text(job["data"])
    elif job["type"] == "url":
        formatted_data = format_url(job["data"])
    elif job["type"] == "wifi":
        formatted_data = format_wifi(job["ssid"], job["password"])
    elif job["type"] == "vcard":
        formatted_data = format_vcard(job["first_name"], job["last_name"], job["phone"], job["email"])
    else:
        raise ValueError(f"unhandled type: {job['type']}")

    qr = build_qr(
        version=job["version"], 
        level=selected_level, 
        size=job["size"], 
        border=job["border"]
        )
    qr.add_data(formatted_data)
    qr.make(fit=True)

    img = create_image(qr, job["fill_colour"], job["back_colour"])

    save_image(img, job["output"])    


def main():

    parser = pass_args()

    args = parser.parse_args()

    # If batchmode checks start here:

    if args.batch:
        with open(args.batch, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            success = 0
            fail = 0
            for row in reader:
                
                try:
                    row_clean = normalize_row(row)
                    proccess_one(row_clean)
                    success += 1
                except Exception as e:
                    print(f"Row failed: {e}")
                    fail +=1
            print(f"{success} succeeded, {fail} failed")
    else:
        arg_list = vars(args)
        proccess_one(arg_list)


if __name__ == "__main__":
     main()
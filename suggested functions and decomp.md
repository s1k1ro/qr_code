suggested functions and decomp

arguments_parser() --- build all arguments postional and optional 

> leave args = parser.parse_args() in main?

contsants.py
error_levels = {
        "L": qrcode.constants.ERROR_CORRECT_L,
        "M": qrcode.constants.ERROR_CORRECT_M,
        "Q": qrcode.constants.ERROR_CORRECT_Q,
        "H": qrcode.constants.ERROR_CORRECT_H,
    }


data_check() -- check for data if not print missing url etc

build_qr() -- 
    qr = qrcode.QRCode(
        version= args.version,
        error_correction=selected_level,
        box_size= args.size,
        border= args.border,
    )

    qr.add_data(args.data)
    qr.make(fit=True)


save_img() --
    try:
        img.save(args.output)
        print(f"Successfully saved {args.output}")
    except Exception as e:
        print(f"Error: Couldnt save file. {e}")
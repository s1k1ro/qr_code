from qr import format_text, format_url, format_vcard, format_wifi

def test_format_url():
    result = format_url("google.com")
    assert result == "https://google.com"

def test_format_url_unchanged():
    result = format_url("http://www.google.com/")
    assert result ==  "http://www.google.com/" 

def test_format_url_unchanged_s():
    result = format_url("https://www.google.com/")
    assert result ==  "https://www.google.com/"  

def test_format_wifi():
    ssid = "test_network"
    password = "password"
    result = format_wifi(ssid, password)
    assert result == f"WIFI:S:{ssid};T:WPA;P:{password};;"

def test_format_wifi_ssidwithsc():
    ssid = "cafe;wifi"
    password = "password"
    result = format_wifi(ssid, password)
    assert result == f"WIFI:S:cafe\\;wifi;T:WPA;P:{password};;"

def test_format_vcard():
    first_name = "Rick"
    last_name = "Owens"
    phone = "612000000"
    email= "rick@owenscorp.eu"
    result = format_vcard(first_name, last_name, phone, email)
    expected = """BEGIN:VCARD
VERSION:3.0
N:Owens;Rick
FN:Rick Owens
TEL:612000000
EMAIL:rick@owenscorp.eu
END:VCARD"""
    assert result == expected

def test_format_vcard_esc():
    first_name = "Rick"
    last_name = "Owens,jr"
    phone = "613;0\n999"
    email = "owens,jr@owenscorp.eu"
    result = format_vcard(first_name, last_name, phone, email)
    expected = """BEGIN:VCARD
VERSION:3.0
N:Owens\\,jr;Rick
FN:Rick Owens\\,jr
TEL:613\\;0\\n999
EMAIL:owens\\,jr@owenscorp.eu
END:VCARD"""
    assert result == expected

def test_format_vcard_no_phone():
    first_name = "Rick"
    last_name = "Owens,jr"
    phone = ""
    email = "owens,jr@owenscorp.eu"
    result = format_vcard(first_name, last_name, phone, email)
    expected = """BEGIN:VCARD
VERSION:3.0
N:Owens\\,jr;Rick
FN:Rick Owens\\,jr
EMAIL:owens\\,jr@owenscorp.eu
END:VCARD"""
    assert result == expected


def test_format_text():
    string = "text"
    result = format_text(string)
    assert result == string

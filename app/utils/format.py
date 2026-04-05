def format_rupiah(value):
    try:
        return "Rp {:,}".format(int(value)).replace(",", ".")
    except:
        return "Rp 0"
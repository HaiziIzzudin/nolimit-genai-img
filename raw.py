def convert2raw(input_string):
    raw_string = input_string.replace("/", "\\")
    raw_string = r"{}".format(raw_string)
    return raw_string
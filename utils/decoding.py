def decode_char_codes(codes):
    """
    Decodes a list of dot-separated character codes into a string.

    :param codes: A list of strings, where each string contains character codes 
                  separated by dots (e.g., "72.101.108").
    :return: A string formed by decoding each valid character code in the input list.
    
    :example:
        decode_char_codes(["72.101.108.108.111", "87.111.114.108.100"])
        # Returns: "HelloWorld"
    """
    return ''.join(
        chr(int(code)) for part in codes for code in part.split('.') if code.isdigit()
    )

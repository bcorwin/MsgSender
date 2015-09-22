from random import sample
import re

def rand_code():
    code = sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 2) + sample('1234567890', 4)
    return ''.join(code)
    
def format_number(phone_number):
    phone_number = str(phone_number)
    phonePattern = re.compile(r'^\D*\+{0,1}1{0,1}\D*(\d{3})\D*(\d{3})\D*(\d{4}).*$', re.VERBOSE)
    if phonePattern.match(phone_number):
        grps = phonePattern.search(phone_number).groups()
        out = "+1" + ''.join(grps[0:3])
    else:
        raise ValueError(phone_number + " is not a valid phone number format.")
    return(out)
    
def extract_command(text, commands):
    """
    Loops through the list of commands and looks for the pattern
    "COMMAND [PARAMETERS]" and outputs the first match it finds
    """
    out = [None, None]
    for c in commands:
        pattern = re.compile(c + " *(.*)", re.IGNORECASE)
        if pattern.match(text):
            parm = pattern.match(text).groups()[0]
            out[0] = c
            out[1] = parm if parm != '' else None
            break
    return out 
        
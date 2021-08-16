import re

def is_email_head(line):
    # match the colon format (Standard)
    if is_standard(line):
        return 'Standard'

    # match reply format
    p = re.compile("^On (Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)")
    reply_match = p.search(line)
    if reply_match:
        return 'Reply'
    
    # not an email head
    return None

def is_standard(line):
    p = re.compile("^\w+:")
    std_match = p.search(line)
    if std_match:
        return True
    else:
        return False
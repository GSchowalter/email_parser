import re

def is_email_head(line):
    # match the colon format (Standard)
    if is_standard(line):
        return 'Standard'

    # match reply format
    p = re.compile("^On (Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?) \d?\d")
    reply_match = p.search(line)
    if reply_match:
        return 'Reply'
    
    # not an email head
    return False

def is_standard(line):
    p = re.compile("^(From|To|Subject|Sent|Date|Cc):")
    std_match = p.search(line)
    if std_match:
        return True
    else:
        return False


# Electric Wizard “Dopethrone.”
# Cc: Ben Hervey <campblackfoot@hotmail.com>; David Durst <thedurst@gmail.com>; Eric Dyrhsen <anjipapa@gmail.com>; Jimmy Askew <james.askew@gmail.com>; Mike Halverson <themikehalverson@gmail.com>; Nathan Burke <Jnathanburke76@gmail.com>; Scott Teems <steems@gmail.com>; Timothy McCready <takethefirstleft@gmail.com>

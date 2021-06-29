from email import email
from striprtf import rtf_to_text
import sys

def main(argv):
    body = ""
    _from = ""
    subject = ""
    date = ""
    to = ""
    FILE = open("sample.out", "w+")
    line_count = 0

    with open(argv[1], 'r') as _in:
        contents = _in.readlines()

    # create an iterator object from that iterable
    iter_obj = iter(contents)

    # infinite loop
    while True:
        try:
            # get the next item
            line = next(iter_obj)
            plain_line = rtf_to_text(line)
            if(plain_line.startswith("From:")):
                new_email = email(_from, subject, date, to, body)
                body = ""
                _from = line
                subject = rtf_to_text(next(iter_obj))
                date = rtf_to_text(next(iter_obj))
                to = rtf_to_text(next(iter_obj))
                FILE.write(new_email.to_string())
            else:
                body += line
        except StopIteration:
            # if StopIteration is raised, break from loop
            break
    FILE.close()
        

if __name__ == "__main__":
    main(sys.argv)
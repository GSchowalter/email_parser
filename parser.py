from email import email
from striprtf import rtf_to_text
import sys

def main(argv):
    body = ""
    _from = ""
    subject = ""
    date = ""
    to = ""
    FILE = open("first_draft.txt", "w+")

    with open(argv[1], 'r', errors="ignore") as _in:
        contents = _in.readlines()

    # create an iterator object from that iterable
    iter_obj = iter(contents)

    # infinite loop
    while True:
        try:
            # TODO add support for other email formats
            # get the next item
            line = next(iter_obj)
            if(line.startswith("From:")):
                new_email = email(_from, subject, date, to, body)
                body = ""
                _from = line
                subject_line = rtf_to_text(next(iter_obj))
                if(subject_line.startswith("Subject:")):
                    subject = subject_line
                    date = rtf_to_text(next(iter_obj))
                    to = rtf_to_text(next(iter_obj))
                else:
                    subject = "No Subject"
                    date = subject_line
                    to = rtf_to_text(next(iter_obj))
                FILE.write(new_email.to_string())
            else:
                body += line
        except StopIteration:
            # if StopIteration is raised, break from loop
            new_email = email(_from, subject, date, to, body)
            FILE.write(new_email.to_string())
            break
    FILE.close()
        

if __name__ == "__main__":
    main(sys.argv)
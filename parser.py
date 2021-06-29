from email import email
from striprtf import rtf_to_text
import sys

def main(argv):
    line = ""
    body = ""
    _from = ""
    subject = ""
    date = ""
    to = ""
    FILE = open("sample.out", "w+")
    line_count = 0
    while(line != None):
        try:
            line = rtf_to_text(input())
            line_count += 1
        except(EOFError) as e:
            print(e)
            new_email = email(_from, subject, date, to, body)
            FILE.write(new_email.to_string())
            FILE.close()
            exit()
        if(line.startswith("From:")):
            new_email = email(_from, subject, date, to, body)
            body = ""
            _from = line
            subject = input()
            date = input()
            to = input()
            FILE.write(new_email.to_string())
        else:
            body += line + "\n"
    FILE.close()
        

if __name__ == "__main__":
    main(sys.argv)
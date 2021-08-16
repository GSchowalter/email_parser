from email import email
from re import L
from striprtf import rtf_to_text
import parsing_svc
import sys

def main(argv):

    # open file to parse and file to write to
    FILE = open("output.txt", "w+")
    with open(argv[1], 'r', errors="ignore") as _in:
        contents = _in.readlines()

    # create an iterator object from the input file
    iter_obj = iter(contents)

    # set of every date time for each email
    sent_times = set()

    # list of emails
    emails = []

    email_found = False

    # infinite loop
    while True:
        try:
            format = ''
            if not email_found == True:
                line = next(iter_obj)
            # parse through each line and determine if it starts a new email
            format = parsing_svc.is_email_head(line)
            # create a new email based on email format
            new_email = None
            if format == 'Standard':
                # standard email case
                print('Entered the Standard branch on line {}'.format(line))
                new_email, next_line = parse_standard(line, iter_obj)
                line = next_line
                email_found = True
            elif format == 'Reply':
                # reply email case
                print('Entered the Reply branch on line {}'.format(line))
                new_email, next_line = parse_reply(line, iter_obj)
                line = next_line
                email_found = True

            if new_email != None:
                print('hit {}'.format(new_email.date))
                emails.append(new_email)
                
            # check the sent_times set to see if the email already exists
        except StopIteration:
            # if StopIteration is raised, break from loop
            break

    print(len(emails))

    for mail in emails:
        FILE.write(mail.to_string())

    FILE.close()

def parse_standard(start, iter):
    line = start
    _from = ''
    subject = ''
    date = ''
    to = ''
    body = ''
    while parsing_svc.is_standard(line):
        section = line[:line.index(':')].upper()
        if section == 'FROM':
            # this keeps a space preceeding the string
            _from = line[line.index(':') + 1:]
        elif section == 'SUBJECT':
            subject = line[line.index(':') + 1:]
        elif section == 'DATE':
            date = line[line.index(':') + 1:]
        elif section == 'TO':
            to = line[line.index(':') + 1:]
        else: 
            print('Unrecognized email field: {}'.format(line))
            break
        line = next(iter)

    # handle the email body
    while not parsing_svc.is_email_head(line):
        body += line
        line = next(iter)

    return (email(_from, subject, date, to, body, 'Standard'), line)

def parse_reply(start, iter):
    body = ''
    line = start
    date_time_str = start[3:start.index('M, ')-2]
    # this could fall apart with the whole 'M,' thing
    _from = start[start.index('M,')+3: start.index(' wrote')]

    line = next(iter)

    # handle the email body
    while not parsing_svc.is_email_head(line):
        body += line
        line = next(iter)

    return (email(_from=_from, date=date_time_str, body=body, type='Reply'), line)

if __name__ == "__main__":
    main(sys.argv)
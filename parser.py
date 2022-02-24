from datetime import datetime
from email import email
from re import L
from striprtf import rtf_to_text
import parsing_svc
import sys
import pytz


def main(argv):

    # open file to parse and file to write to
    FILE = open("new_output.html", "w+")
    with open(argv[1], 'r', errors="ignore") as _in:
        contents = _in.readlines()

    # create an iterator object from the input file
    iter_obj = iter(contents)

    # set of every date time for each email
    sent_times = dict()

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
                new_email, next_line = parse_standard(line, iter_obj, emails, sent_times)
                line = next_line
                email_found = True
            elif format == 'Reply':
                # reply email case
                new_email, next_line = parse_reply(line, iter_obj, emails, sent_times)
                line = next_line
                email_found = True

            add_email(new_email, sent_times, emails)
                
            # check the sent_times set to see if the email already exists
        except StopIteration as e:
            # if StopIteration is raised, break from loop
            break

    emails.sort()

    for mail in emails:
        FILE.write(mail.to_string())

    FILE.close()

def add_email(new_email, sent_times, emails):
    key = new_email.parse_to_datetime()
    print(key)
    if new_email != None and not (key in sent_times):
        sent_times[key] = new_email
        emails.append(new_email)
    elif new_email.type == "Standard":
        emails.remove(sent_times[key])
        emails.append(new_email)
        sent_times[key] = new_email

def parse_standard(start, iter, emails, sent_times):

    line = start
    _from = ''
    subject = ''
    date = ''
    to = ''
    body = ''
    cc = ''
    time_zone = pytz.timezone('US/Pacific')
    try:
        while parsing_svc.is_standard(line):
            section = line[:line.index(':')].upper()
            if section == 'FROM':
                # this keeps a space preceeding the string
                _from = line[line.index(':') + 1:]
            elif section == 'SUBJECT':
                subject = line[line.index(':') + 1:]
            elif section == 'DATE':
                date = line[line.index(':') + 1:]
                try:
                    time_zone = line[line.rindex('T') + 1:]
                except ValueError as e:
                    time_zone = "EST"
            elif section == 'SENT':
                date = line[line.index(':') + 1:]
                try:
                    time_zone = line[line.rindex('T') + 1:]
                except ValueError as e:
                    time_zone = "PST"
            elif section == 'TO':
                to = line[line.index(':') + 1:]
            elif section == 'CC':
                print("CC section in standard parsing hit")
                cc = line[line.index(':') + 1:]
            else: 
                print('Unrecognized email field: {}'.format(line))
            line = next(iter)

        # handle the email body
        while not parsing_svc.is_email_head(line):
            body += line
            line = next(iter)
    except StopIteration as e:
        new_email = email(_from, subject, date, to, body, 'Standard', time_zone)
        add_email(new_email, sent_times, emails)
        raise e
    return (email(_from, subject, date, to, body, 'Standard', time_zone), line)

def parse_reply(start, iter, emails, sent_times):
    body = ''
    line = start
    
    # this could fall apart with the whole 'M,' thing
    try:
        start_ind = start.index('M,')+3
    except ValueError as e:
        print('String that breaks the start of the reply patten: {}'.format(start))
        raise e
    try:
        end_ind = start.index(' wrote')
    except ValueError as e:
        print("The string that breaks the end of the reply pattern: {}".format(start))
        raise e
    date_time_str = start[3:start.index('M, ')+1]
    _from = start[start_ind: end_ind]

    try:
        # handle the email body
        line = next(iter)
        while not parsing_svc.is_email_head(line):
            body += line
            line = next(iter)

    except StopIteration as e:
        new_email = (email(_from=_from, date=date_time_str, body=body, type='Reply'))
        add_email(new_email, sent_times, emails)
        raise e

    return (email(_from=_from, date=date_time_str, body=body, type='Reply'), line)

if __name__ == "__main__":
    main(sys.argv)
import re
import datetime
import pytz
import calendar
class email:

    
    def __init__(self, _from="", subject="", date="", to="", body="", type="", time_zone=""):
        self._from = _from
        self.subject = subject
        self.date = date
        self.to = to
        self.body = body
        self.type = type
        self.rev_dict = {month: index for index, month in enumerate(calendar.month_name) if month}
        self.rev_dict['Jul'] = 7
        self.rev_dict['Sep'] = 9
        self.rev_dict['Feb'] = 2
        self.rev_dict['Mar'] = 3
        self.rev_dict['Apr'] = 4
        self.rev_dict['Dec'] = 12

    def __lt__(self, other):
        try:
            return self.parse_to_datetime() < other.parse_to_datetime()
        except TypeError as e:
            print('TYPE ERROR START OF ERROR MESSAGE')
            print('from: {}'.format(self._from))
            print('to: {}'.format(self.to))
            print('subject: {}'.format(self.subject))
            raise(e)

    def remove_reply(self, str):
        # "On ?((Mon|Tue(s)?|Wed(nes)?|Thu(r)?(s)?|Fri|Sat(ur)?|Sun)(day)?)?,? (Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)* \d?\d, \d\d\d\d,? at \d?\d:\d\d"
        p = re.compile("On ?((Mon|Tue(s)?|Wed(nes)?|Thu(r)?(s)?|Fri|Sat(ur)?|Sun)(day)?)?,? (Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)* \d?\d, \d\d\d\d,? at \d?\d:\d\d")
        match = p.search(str)
        if match:
            index_of_reply = match.start()
            return str[:index_of_reply]
        return str

    def find_str(self, str, pattern):
        p = re.compile(pattern)
        match = p.search(str)
        if match:
            index_of_reply = match.start()
            return str[match.start():match.end()]
        return "String Not Found"

    def parse_to_datetime(self):
        dt_obj = datetime.datetime(datetime.MAXYEAR, 1, 1)
        if self.date == '':
            print('blank date found in email:')
            print('from: {}'.format(self._from))
            print('to: {}'.format(self.to))
            print('subject: {}'.format(self.subject))
            return None
        if self.type == 'Standard':
            str = self.date.strip()

            # TODO: update this to change based on the actual time zone

            year = self.find_str(str, '(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?) \d\d?, \d\d\d\d')
            year = year[len(year)-4:].strip()

            str_month = self.find_str(str, '(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)')
            # only works with full month names
            try:
                int_month = self.rev_dict[str_month]
            except KeyError as e:
                print(str)
                raise(e)

            day = self.find_str(str, '(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?) \d\d?')
            day = day[len(day)-2:].strip()

            try:
                hour = self.find_str(str, '(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?) \d\d?, \d\d\d\d ?a?t? \d?\d')
                hour = int(hour[len(hour)-2:].strip())
            except ValueError as e:
                print(str)
                raise(e)

            minute = self.find_str(str, '(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?) \d\d?, \d\d\d\d ?a?t? \d?\d:\d\d')
            minute = minute[len(minute)-2:].strip()

            am_or_pm = self.find_str(str, '(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?) \d\d?, \d\d\d\d ?a?t? \d?\d:\d\d:\d\d \w\w')
            am_or_pm = am_or_pm[len(am_or_pm)-2:].strip()
            if(am_or_pm.upper() == 'PM' and hour < 12):
                hour = hour + 12

            timezone = self.find_str(str, '(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?) \d\d?, \d\d\d\d ?a?t? \d?\d:\d\d:\d\d \w\w \w\w\w')
            timezone = timezone[len(timezone)-3:].strip()
            #TODO: have this account for daylight savings time
            tz = pytz.timezone('US/Eastern')
            if('P' in timezone):
                tz = pytz.timezone('US/Pacific')


            try:
                dt_obj = datetime.datetime(int(year), int_month, int(day), hour, int(minute))
                dt_obj = tz.localize(dt_obj)
            except ValueError as e:
                print(hour)
                raise(e)

        else:
            dt_obj = datetime.datetime.strptime(self.date, '%b %d, %Y, at %I:%M %p')
            raw_tz = pytz.timezone('US/Pacific')
            if('Tim' not in self._from):
                raw_tz = pytz.timezone('US/Eastern')
            dt_obj = raw_tz.localize(dt_obj)

        return dt_obj

    def format_from(self):
        return self._from.strip()
    
    def format_date(self):
        dt_object = self.parse_to_datetime()
        return self.date.strip()

    def format_subject(self):
        return self.subject

    def format_body(self):
        return self.remove_reply(self.body.strip())

    def to_string(self):
        # TODO write a function that returns the a string in the output format
        # return self._from + self.subject + self.date + self.to + self.body

        if(self._from == "" and self.subject == "" and self.date == ""):
            return "Empty email\n"
        str = "<b> {} / {} / {}</b> <br><br> {}</br></br>\n\n".format(self.date, self._from.strip(), self.subject, self.format_body())
        return str
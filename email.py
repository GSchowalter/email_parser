import re
class email:
    
    def __init__(self, _from="From No One", subject="No Subject", date="No Date", to="To no one", body="No body text"):
        self._from = _from
        self.subject = subject
        self.date = date
        self.to = to
        self.body = body

    def remove_reply(self, str):
        # "On ?((Mon|Tue(s)?|Wed(nes)?|Thu(r)?(s)?|Fri|Sat(ur)?|Sun)(day)?)?,? (Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)* \d?\d, \d\d\d\d,? at \d?\d:\d\d"
        p = re.compile("On ?((Mon|Tue(s)?|Wed(nes)?|Thu(r)?(s)?|Fri|Sat(ur)?|Sun)(day)?)?,? (Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)* \d?\d, \d\d\d\d,? at \d?\d:\d\d")
        match = p.search(str)
        if match:
            index_of_reply = match.start()
            return str[:index_of_reply]
        return str

    def format_from(self):
        return self._from.strip()
    
    def format_date(self):
        return self.date

    def format_subject(self):
        return self.subject

    def format_body(self):
        return self.remove_reply(self.body.strip())

    def to_string(self):
        # TODO write a function that returns the a string in the output format
        # return self._from + self.subject + self.date + self.to + self.body

        if(self._from == "" and self.subject == "" and self.date == ""):
            return "Empty email\n"
        str = "<b> {} / {} / {}</b> <br><br> {}</br></br>".format(self.date, self._from.strip(), self.subject, self.format_body())
        return str
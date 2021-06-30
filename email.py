import re
class email:
    
    def __init__(self, _from="From No One", subject="No Subject", date="No Date", to="To no one", body="No body text"):
        self._from = _from
        self.subject = subject
        self.date = date
        self.to = to
        self.body = body

    def remove_reply(self, str):
        # "On (Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)* \d\d, \d\d\d\d, at \d?\d:\d\d"
        p = re.compile("On ?((Mon|Tue(s)?|Wed(nes)?|Thu(r)?(s)?|Fri|Sat(ur)?|Sun)(day)?)?,? (Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)* \d?\d, \d\d\d\d,? at \d?\d:\d\d")
        match = p.search(str)
        if match:
            index_of_reply = match.start()
            return str[:index_of_reply]
        return str


    def to_string(self):
        # TODO write a function that returns the a string in the output format
        # return self._from + self.subject + self.date + self.to + self.body

        if(self._from == "" and self.subject == "" and self.date == ""):
            return "Empty email\n"
        str = "BOLDKEYWORD {} / {} / {} \n\n {}\n\n".format(self.date, self._from.strip(), self.subject, self.remove_reply(self.body.strip()))
        return str
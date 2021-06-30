class email:
    
    def __init__(self, _from="From No One", subject="No Subject", date="No Date", to="To no one", body="No body text"):
        self._from = _from
        self.subject = subject
        self.date = date
        self.to = to
        self.body = body

    def remove_reply(self, str):
        # On (Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Oct|Nov|Dec)* \d\d, \d\d\d\d, at \d?\d:\d\d
        if(str.__contains__("On ")):
            index_of_reply = str.index("On ")
            return str[:index_of_reply]
        else:
            return str

    def to_string(self):
        # TODO write a function that returns the a string in the output format
        # return self._from + self.subject + self.date + self.to + self.body

        if(self._from == "" and self.subject == "" and self.date == ""):
            return "Empty email\n"
        str = "BOLDKEYWORD {} / {} / {} \n\n {}\n\n".format(self.date, self._from.strip(), self.subject, self.remove_reply(self.body.strip()))
        return str
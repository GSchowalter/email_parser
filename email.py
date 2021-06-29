class email:
    
    def __init__(self, _from="From No One", subject="No Subject", date="No Date", to="To no one", body="No body text"):
        self._from = _from
        self.subject = subject
        self.date = date
        self.to = to
        self.body = body

    def to_string(self):
        # TODO write a function that returns the a string in the output format
        # return self._from + self.subject + self.date + self.to + self.body

        if(self._from == "" and self.subject == "" and self.date == ""):
            return "Empty email\n"
        str = "{} / {} / {} \n {}".format(self.date, self._from.strip(), self.subject, self.body.strip())
        return str
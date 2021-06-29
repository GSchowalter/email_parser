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

        str = "{} / From {} / {} \n {}".format(self.date, self._from, self.subject, self.body)
        return str
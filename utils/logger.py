import datetime
import os


class Logger:
    def __init__(self):
        self.now_file = None

    def get_date(self):
        self.now_file = datetime.datetime.now().strftime("Log_%Y-%m-%d.txt")

    def write_to_log(self, text, new_line=True):
        self.get_date()
        with open('Log' + os.altsep + self.now_file, 'a+') as file:
            if new_line:
                file.write('\n[' + str(datetime.datetime.now()) + ']: ' + text)
            else:
                file.write(text)
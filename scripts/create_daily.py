# Create a daily journal file

from datetime import date, timedelta
from os import path, makedirs

'''
Dir structure:
Daily/
    2020/
        01-January/
            2020-01-02-Mon.md
'''

'''
TODO
- Handle todo hierarchy carryover
- handle todo carryover of more than one day (e.g. skipped a day)
- add logging
- handle holidays
- extract BASEPATH into env var
'''

class DailyFileInfo:
    '''Represents all the information needed to create a daily journal file'''
    BASEPATH = r'C:\Users\elliott_chenoweth\Box\Elliott_Chenoweth\Markdown\Daily'
    STARTER_CONTENTS = '''# Todo
{}

# Scrum update

# Notes

'''
    def __init__(self, date_obj = date.today()):
        self._date = date_obj

    @property
    def iso_date(self):
        return self._date.isoformat()

    @property
    def month(self):
        return self._date.strftime('%m-%B')

    @property
    def day_abbrev(self):
        return self._date.strftime('%a')

    @property
    def filename(self):
        return self.iso_date + '-' + self.day_abbrev + '.md'

    @property
    def folderpath(self):
        return path.join(DailyFileInfo.BASEPATH, str(self._date.year), self.month)

    @property
    def filepath(self):
        return path.join(self.folderpath, self.filename)

    @property
    def is_weekday(self):
        return self._date.weekday() in range(0, 5)

    def create(self):
        if not self.is_weekday:
            # don't make these files on weekends
            print('Exiting - Not a weekday')
            exit(0)   

        try:
            makedirs(self.folderpath)
        except FileExistsError as e:
            print(f"Directory {self.folderpath} already exists")
        finally:
            if not path.exists(self.filepath):
                print(f"Creating {self.filename}")
                leftover_todos = self.get_leftover_todos()
                with open(self.filepath, 'w') as f:
                    f.write(DailyFileInfo.STARTER_CONTENTS.format(leftover_todos))

    def get_leftover_todos(self):
        last_work_day = None
        
        if self._date.weekday() == 0: # if today = Monday
            # last work day was Friday
            last_work_day = self._date - timedelta(days=3)
        elif self._date.weekday() == 6: # if today = Sunday
            # last work day was Friday
            last_work_day = self._date - timedelta(days=2)
        else:
            last_work_day = self._date - timedelta(days=1)

        iso_date = last_work_day.isoformat()
        month = last_work_day.strftime('%m-%B')
        day_abbrev = last_work_day.strftime('%a')

        filename =  iso_date + '-' + day_abbrev + '.md'

        folderpath = path.join(DailyFileInfo.BASEPATH, str(last_work_day.year), month)

        filepath = path.join(folderpath, filename)

        # grab the todos from the last work day's file
        todos = ""
        try:
            with open(filepath, 'r') as f:
                contents = f.read()
                lines = map(lambda l: l.strip(), contents.splitlines())
                todos_list = filter(lambda l: l.startswith('- [ ]'), lines)
                todos = '\n'.join(todos_list)
        except FileNotFoundError:
            print(f"Last work day's file not found: {filepath}")

        return todos + '\n'


def main():
    fileobj = DailyFileInfo()
    fileobj.create()

if __name__ == '__main__':
    main()

import os, datetime

#Backup procedure - Old code - Rewrite - include file number limit
def backup(filepath):                                                             
    def get_root(filepath):
        index = filepath.rfind('/')
        root = filepath[0:index + 1]
        return root
    def get_filename(filepath):
        index = filepath.rfind('/')
        dot = filepath.rfind('.')
        filename = filepath[index + 1:dot]
        return filename
    def get_extension(filepath):
        dot = filepath.rfind('.')
        extension = filepath[dot:]
        return extension
    root = get_root(filepath)
    filename = get_filename(filepath)
    extension = get_extension(filepath)
    new_root = root + 'bkup/'
    def get_date():
        time = datetime.datetime.today()
        year = str(time.year)
        def add_zero(string):
            if len(string) == 1:
                return '0' + string
            elif len(string) == 2:
                return string
            else:
                raise ValueError
        month = add_zero(str(time.month))
        day = add_zero(str(time.day))
        hour = add_zero(str(time.hour))
        minute = add_zero(str(time.minute))
        return year + month + day + hour + minute
    new_filename = filename + '_' + get_date()
    new_filepath = new_root + new_filename + extension
    def write_file():
        with open(filepath, 'r') as source:
            with open (new_filepath, 'w') as target:
                target.write(source.read())
    try:
        write_file()
    except FileNotFoundError:
        try:
            os.mkdir(new_root)
            write_file()
        except FileExistsError:
            return

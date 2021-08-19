from datetime import datetime, timedelta


class Period:
    def __init__(self):
        self.current_month = str(datetime.today().year) +\
            '-' + str(datetime.today().month)
        self.last_month = str(datetime.today().year) +\
            '-' + str((datetime.today().replace(
                day=1) - timedelta(days=1)).month)
        self.two_months_ago = str(datetime.today().year) +\
            '-' + str(((datetime.today().replace(day=1) -
                        timedelta(days=1)).replace(day=1) -
                       timedelta(days=1)).month)

import datetime
import time


class RiskDB:
    def __init__(self):
        self.knownUserList = []
        self.knownDeviceList = []
        self.knownIPList = []
        self.successfulLoginDict = {}
        self.failedLoginDict = {}
        self.failedLoginCount = 0
        self.weektime_start, self.weektime_end = self.previous_week_range()

    def previous_week_range(self):
        today = datetime.date.today()
        start_date = today + datetime.timedelta(-today.weekday(), weeks=-1)
        end_date = today + datetime.timedelta(-today.weekday() - 1)
        weektime_start = time.mktime(start_date.timetuple())
        weektime_end = time.mktime(end_date.timetuple())
        return weektime_start, weektime_end

    def set_knownUserList(self, username):
        if username not in self.knownUserList:
            self.knownUserList.append(username)

    def set_knownDeviceList(self, deviceID):
        if deviceID not in self.knownDeviceList:
            self.knownDeviceList.append(deviceID)

    def set_knownIPList(self, ip):
        if ip not in self.knownIPList:
            self.knownIPList.append(ip)

    def set_successfulLoginDict(self, username, unix_time):
        if username in self.successfulLoginDict.keys():
            if self.successfulLoginDict[username] < unix_time:
                self.successfulLoginDict[username] = unix_time
        else:
            self.successfulLoginDict.update({username: unix_time})

    def set_failedLoginDict(self, username, unix_time):
        if username in self.failedLoginDict.keys():
            if self.failedLoginDict[username] < unix_time:
                self.failedLoginDict[username] = unix_time
        else:
            self.failedLoginDict.update({username: unix_time})

    def set_failedLoginCount(self, unix_time):
        # if unix_time >= self.weektime_start
        # and unix_time <= self.weektime_end:
        # self.failedLoginCount += 1
        self.failedLoginCount += 1

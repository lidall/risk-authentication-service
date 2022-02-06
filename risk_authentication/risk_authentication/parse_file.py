import json
import datetime

class ParseFile:

    def __init__(self, db):
        self.db = db

    def parse_timestamp(self, timestamp):
        date_format = datetime.datetime.strptime(timestamp,'%Y-%m-%dT%H:%M:%S.%fZ')
        unix_time = datetime.datetime.timestamp(date_format)
        return unix_time

    def parse_unixtime(self, unix_time):
        timestamp = datetime.datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return timestamp

    def parse_content(self, content):
        for line in content:
            if "authentication_type" in line:
                log_detail = line.split(' [AUDIT] ')[1]
                json_object = json.loads(log_detail)

                username = json_object["distinguished_name_user"]
                ip = json_object["client_ip"]
                deviceID = json_object["distinguished_name_device_id"]
                timestamp = json_object["timestamp"]
                unix_time = self.parse_timestamp(timestamp)
                eventType = json_object["event_type"]

                if eventType == "authentication_succeeded":

                    self.db.set_knownUserList(username)
                    self.db.set_knownIPList(ip)
                    self.db.set_knownDeviceList(deviceID)
                    self.db.set_successfulLoginDict(username, unix_time)

                elif eventType == "authentication_failed":
                    self.db.set_failedLoginDict(username, unix_time)
                    self.db.set_failedLoginCount(unix_time)

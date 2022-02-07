import json
import datetime
import logging
import time
import os


class ParseFile:
    def __init__(self, db):
        self.db = db
        self.parseLog = logging.getLogger(__name__)
        self.parseLog.setLevel(logging.DEBUG)
        os.environ['TZ'] = 'Europe/Stockholm'
        time.tzset()

    def parse_timestamp(self, timestamp):
        """

        Input: String timestamp with format: '%Y-%m-%dT%H:%M:%S.%fZ'
        Output: Float Unix time

        Transform string timestamp to unix time
        for easier comparison and storage

        """
        date_format = datetime.datetime.strptime(
            timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')
        unix_time = datetime.datetime.timestamp(date_format)
        return unix_time

    def parse_unixtime(self, unix_time):
        """

        Input: Float Unix time
        Output: String timestamp with format: '%Y-%m-%dT%H:%M:%S.%fZ'

        Transform unix time to string timestamp for
        returning the result to clients

        """
        timestamp = datetime.datetime.utcfromtimestamp(
            unix_time).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return timestamp

    def parse_content(self, content):
        authentication_info = ["distinguished_name_user",
                               "client_ip",
                               "distinguished_name_device_id",
                               "timestamp",
                               "event_type"
                               ]

        for line in content:
            if "authentication_type" in line:
                log_detail = line.split(' [AUDIT] ')[1]
                json_object = None
                try:
                    json_object = json.loads(log_detail)
                except ValueError:
                    self.parseLog.error("Audit logs are not in json format," +
                                        " please double check.")
                if json_object and all(info in json_object
                                       for info in authentication_info):
                    username = json_object.get("distinguished_name_user")
                    ip = json_object.get("client_ip")
                    device_id = json_object.get("distinguished_name_device_id")
                    timestamp = json_object.get("timestamp")
                    unix_time = self.parse_timestamp(timestamp)
                    event_type = json_object.get("event_type")

                    if event_type == "authentication_succeeded":

                        self.db.set_knownUserList(username)
                        self.db.set_knownIPList(ip)
                        self.db.set_knownDeviceList(device_id)
                        self.db.set_successfulLoginDict(username, unix_time)

                    elif event_type == "authentication_failed":
                        self.db.set_failedLoginDict(username, unix_time)
                        self.db.set_failedLoginCount(unix_time)
                else:
                    self.parseLog.warning("Authentication log " +
                                          line + " lacks required info.")

        self.parseLog.info("All authentication logs have been processed.")

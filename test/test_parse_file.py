import unittest
import json
from pathlib import Path
from risk_authentication.parse_file import ParseFile
from risk_authentication.risk_database import RiskDB


class TestParseFile(unittest.TestCase):
    def setUp(self):
        self.db = RiskDB()
        self.parse_file = ParseFile(self.db)
        with Path(Path(__file__).parent,
                  'fixtures/test_logs.json').open() as json_file:
            self.testcases = json.load(json_file)
        self.valid_auth_log = self.testcases.get("valid_auth_log")
        self.valid_normal_log = self.testcases.get("valid_normal_log")
        self.auth_log_miss_ip = self.testcases.get("auth_log_miss_ip")
        self.invalid_auth_log = self.testcases.get("invalid_auth_log")

    def test_parse_content(self):
        with self.assertLogs() as captured:
            self.parse_file.parse_content(self.invalid_auth_log)
        self.assertEqual(len(captured.records), 1)
        self.assertEqual(
        	captured.records[0].getMessage(),
            "Audit logs are not in json format, please double check.")

        with self.assertLogs() as captured:
            self.parse_file.parse_content(self.valid_normal_log)
        self.assertEqual(len(captured.records), 1)
        self.assertEqual(captured.records[0].getMessage(),
                         "All authentication logs have been processed.")

        with self.assertLogs() as captured:
            self.parse_file.parse_content(self.auth_log_miss_ip)
        self.assertEqual(len(captured.records), 2)
        self.assertContains(captured.records[0].getMessage(),
        					"Authentication log lacks required info.")
        self.assertEqual(captured.records[1].getMessage(),
                         "All authentication logs have been processed.")

        self.parse_file.parse_content(self.valid_auth_log)
        self.assertEqual(self.db.knownUserList, ["admin"])
        self.assertEqual(self.db.knownDeviceList,
                         ["admin28b0016db5cd425975859abe570228f0"])
        self.assertEqual(self.db.successfulLoginDict, {"admin": ''})
        self.assertEqual(self.db.failedLoginDict, {})
        self.assertEqual(self.db.failedLoginCount, 0)
        self.assertEqual(self.db.knownIPList, ["10.97.3.53"])

import unittest
from risk_authentication.risk_database import RiskDB
# import random


class TestRiskDatabase(unittest.TestCase):
    def setUp(self):
        self.db = RiskDB()
        self.db.knownIPList = ['10.192.2.2']
        self.db.knownUserList = ['Bob']
        self.db.successfulLoginDict = {'Bob': 1644151100}
        self.db.failedLoginDict = {'Bob': 1644151199}
        self.db.failedLoginCount = 5

    def test_set_knownUserList(self):
        self.db.set_knownUserList('Bob')
        self.assertEqual(self.db.knownUserList, ['Bob'])
        self.db.set_knownUserList('Kevin')
        self.assertEqual(self.db.knownUserList, ['Bob', 'Kevin'])

    def test_set_knownIPList(self):
        self.db.set_knownIPList('10.192.2.2')
        self.assertEqual(self.db.knownIPList, ['10.192.2.2'])
        self.db.set_knownIPList('10.192.10.22')
        self.assertEqual(self.db.knownIPList, ['10.192.2.2', '10.192.10.22'])

    def test_set_successfulLoginDict(self):
        # Test if old Bob record has been ignored
        self.db.set_successfulLoginDict('Bob', 1644151000)
        self.assertEqual(self.db.successfulLoginDict['Bob'], 1644151100)
        # Test if new Bob record has been updated
        self.db.set_successfulLoginDict('Bob', 1644151500)
        self.assertEqual(self.db.successfulLoginDict['Bob'], 1644151500)
        # Test if new Kevin record has been added into the dict
        self.db.set_successfulLoginDict('Kevin', 1644151530)
        self.assertEqual(self.db.successfulLoginDict['Kevin'], 1644151530)

    def test_set_failedLoginDict(self):
        # Test if old Bob record has been ignored
        self.db.set_failedLoginDict('Bob', 1644151009)
        self.assertEqual(self.db.failedLoginDict['Bob'], 1644151009)
        # Test if new Bob record has been updated
        self.db.set_failedLoginDict('Bob', 1644151599)
        self.assertEqual(self.db.failedLoginDict['Bob'], 1644151599)
        # Test if new Kevin record has been added into the dict
        self.db.set_failedLoginDict('Kevin', 1644151530)
        self.assertEqual(self.db.failedLoginDict['Kevin'], 1644151530)

    def set_failedLoginCount(self):
        # Since in the main function I have simplify the adding method:
        # when there's a failed logging record, the counter will plus one.
        # I commented the following codes which can test if the record
        # is within the range of last week

        """
        weektime_start, weektime_end = self.db.previous_week_range()
        unixTimeTest = random.randint(weektime_start - 100, weektime_start)
        self.db.set_failedLoginCount(unixTimeTest)
        self.assertEqual(self.db.failedLoginCount, 5)
        unixTimeTest = random.randint(weektime_start, weektime_end)
        self.db.set_failedLoginCount(unixTimeTest)
        self.assertEqual(self.db.failedLoginCount, 6)
        """

        self.db.set_failedLoginCount(1644151530)
        self.assertEqual(self.db.failedLoginCount, 6)

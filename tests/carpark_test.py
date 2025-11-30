import unittest
import sys,os
from pathlib import Path
cwd = Path(os.path.dirname(__file__))
parent = str(cwd.parent)

sys.path.append(parent + "/smartpark")

from carpark import CarparkManager


class TestConfigParsing(unittest.TestCase):

    def test_fresh_carpark(self):
        # arrange: create a brand new carpark
        carpark = CarparkManager()

        # assert: a new carpark should have 1000 free spaces
        self.assertEqual(1000, carpark.available_spaces)

    def test_empty_on_start(self):
        """A brand new carpark should be empty."""
        carpark = CarparkManager()
        self.assertTrue(carpark.is_empty())

    def test_not_empty_after_arrival(self):
        """After one car arrives, the carpark should not be empty."""
        carpark = CarparkManager()
        carpark.car_arrives()
        self.assertFalse(carpark.is_empty())

if __name__=="__main__":
#    print("cwd: " + parent + "/smartpark")
    unittest.main()

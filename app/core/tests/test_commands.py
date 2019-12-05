from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        # Use patch to mock ConnectionHandler's __getitem__ function
        #   to force return True so as to override an OperationalError
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.return_value = True
            call_command('wait_for_db')
            # Check that gi is called only once
            self.assertEqual(gi.call_count, 1)

    # Use @patch decorator to mock time.sleep 
    #   to force return True so as not to slow down test execution
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # Set a side effect to raise OperationalError 5x,
            #   then return True on 6th try
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)

from unittest.mock import patch, MagicMock
from utils.config import (
    cast_bool,
    load
)
import unittest



class TestCastBool(unittest.TestCase):

    def test_falsy_containers(self):
        self.assertFalse(cast_bool([]))
        self.assertFalse(cast_bool(()))
        self.assertFalse(cast_bool({}))
        self.assertFalse(cast_bool(set()))
        self.assertFalse(cast_bool(range(0)))
    
    def test_falsy_values(self):
        self.assertFalse(cast_bool(0))
        self.assertFalse(cast_bool(0.0))
        self.assertFalse(cast_bool(0j))
        self.assertFalse(cast_bool(""))
    
    def test_falsy_constants(self):
        self.assertFalse(cast_bool(None))
        self.assertFalse(cast_bool(False))
    

    def test_truthy_strings(self):
        self.assertTrue(cast_bool('true'))
        self.assertTrue(cast_bool('t'))
        self.assertTrue(cast_bool('1'))
        self.assertTrue(cast_bool('yes'))
        self.assertTrue(cast_bool('y'))

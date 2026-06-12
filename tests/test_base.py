import unittest
import sys
import os

# Appends the src folder to the system path so the tests can find your drivers
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

class TestPrusa_Base(unittest.TestCase):
    """base Prusa MK4S test class"""
    pass

class TestImports(TestPrusa_Base):
    """test importing the module drivers"""

    def test_prusa_driver_import(self):
        """test importing the Prusa 3D printer driver"""
        import prusa_driver
        
        # Verifies the import succeeded and the primary function is accessible
        assert prusa_driver.run_parametric_loop is not None

    def test_camera_driver_import(self):
        """test importing the optical sensor driver"""
        import camera_driver
        
        # Verifies the import succeeded and the primary function is accessible
        assert camera_driver.get_single_measurement is not None

if __name__ == "__main__":
    unittest.main()

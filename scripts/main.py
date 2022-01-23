from src.scripts.testing_units import EncryptionUnitTests as encryption_tests
from src.scripts.testing_units import DecryptionUnitTests as decryption_tests
from src.scripts.testing_units import UnitTests as ut


encryptionTests = encryption_tests()
decryptionTests = decryption_tests()

encryptionTests.run_all_unit_tests("bmp")
decryptionTests.run_all_unit_tests("bmp")

ut.cleanup()
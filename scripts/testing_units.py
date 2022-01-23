import os
import shutil
import subprocess
from images import Images
from encryption import EncryptEngine


class UnitTests(object):
    """ Provides support for different units testing """

    _images_root_folder = r"E:\3. Repositories\ImageEncryption\src\resources\demo_images"
    _bmp_files_folder = _images_root_folder + r"\bmp_files"

    _tests_results = r"E:\3. Repositories\ImageEncryption\src\resources\test_results"
    _bmp_results_folder = _tests_results + r"\bmp_results"

    encryptEngine = None
    imageHandler = None

    @staticmethod
    def _get_folder_content(folder_path):
        return os.listdir(folder_path)

    @classmethod
    def _manage_dialogue_answers(cls, answer):
        if answer == "Yes":
            print("Performing results folders cleanup")
            print("Program finished.")
            return True
        elif answer == "No":
            print("Program finished.\nYou will now be redirected to the results folder.")
            return False

    @classmethod
    def _cleanup_dialogue(cls):
        answer = input("Would you like to perform results folders cleanup ?")
        cls._manage_dialogue_answers(answer)
        print()

        while answer != "Yes" and answer != "No":
            print("Your input is not a valid answer.\nPlease choose between Yes or No")
            answer = input("Would you like to perform cleanup ? ")
            print()
        cls._manage_dialogue_answers(answer)


    @classmethod
    def cleanup(cls):
        result_folders = folders = [f"{cls._bmp_results_folder}\\encrypted",
                                    f"{cls._bmp_results_folder}\\decrypted"]

        if cls._cleanup_dialogue():
            for folder in result_folders:
                for filename in os.listdir(folder):
                    file_path = os.path.join(folder, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print('Failed to delete %s. Reason: %s' % (file_path, e))
        else:
            subprocess.Popen(
                fr'explorer /select,"{cls._tests_results}"')


class EncryptionUnitTests(UnitTests):
    """ Contains all encryption test scenarios definitions """

    def _test_bmp_files_encryption(self):
        """ Test encryption method on bmp files test set. """

        for bmpFile in self._get_folder_content(self._bmp_files_folder):
            self.encryptEngine = EncryptEngine()
            img = Images(f"{self._bmp_files_folder}\\{bmpFile}")

            print("Image shape:")
            print("{height} x {width} x {color_depth}")
            print(img.get_image_dimensions())

            encrypted = self.encryptEngine.encrypt_image(
                img.get_image_array(),
                img.get_image_dimensions())

            img.save_image(encrypted, f"{self._bmp_results_folder}\\encrypted\\{bmpFile}")
            img.render_image_from_array(encrypted)

    def run_all_unit_tests(self, test_type="all"):
        """
            Calling all unit test sets using @test_type flag.
            @parm:
                @test_type  -> all for running all test sets.
                            -> specify a file type. (e.g: bmp, jpeg, jpg, etc).
        """

        if test_type == "all":
            pass

        elif test_type == "bmp":
            self._test_bmp_files_encryption()


class DecryptionUnitTests(UnitTests):
    """ Contains all decryption test scenarios definitions """

    def _test_bmp_files_decryption(self):
        """ Test encryption method on bmp files test set. """

        for bmpFile in self._get_folder_content(f"{self._bmp_results_folder}\\encrypted"):
            self.encryptEngine = EncryptEngine()
            img = Images(f"{self._bmp_results_folder}\\encrypted\\{bmpFile}")

            print("Image shape:")
            print("{height} x {width} x {color_depth}")
            print(img.get_image_dimensions())

            encrypted = self.encryptEngine.encrypt_image(
                img.get_image_array(),
                img.get_image_dimensions())

            img.save_image(encrypted, f"{self._bmp_results_folder}\\decrypted\\{bmpFile}")
            img.render_image_from_array(encrypted)

    def run_all_unit_tests(self, test_type="all"):
        """
            Calling all unit test sets using @test_type flag.
            @parm:
                @test_type  -> all for running all test sets.
                            -> specify a file type. (e.g: bmp, jpeg, jpg, etc).
        """

        if test_type == "all":
            pass

        elif test_type == "bmp":
            self._test_bmp_files_decryption()

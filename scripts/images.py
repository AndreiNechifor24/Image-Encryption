import matplotlib.pyplot as pyplot
import matplotlib.image as image
import numpy as np
from PIL import Image as pilimg


class Images(object):
    """ Offers support for image file reading and writing in specific formats for current framework. """

    _filePath = ""
    _rootFolder = ""

    _img = None
    _img_height = None
    _img_width = None

    def __init__(self, file_path, root_folder=""):

        if not(self._is_image(file_path)):
            raise TypeError("Given file path does not point to an image file")

        self._filePath = file_path
        _rootFolder = root_folder

        self._read_image()

    @staticmethod
    def _is_image(file_path):
        """ Performs validation over the given @file_path to verify if the file is image or not. """

        _image_type_extensions = (".jpeg", ".jpg", ".tiff", ".raw", ".png", ".bmp")
        return any(ext in file_path for ext in _image_type_extensions)

    @staticmethod
    def render_image_from_array(array):
        pyplot.imshow(array)
        pyplot.show()

    def get_image_array(self):
        return np.asarray(self._img)

    def _read_image(self):
        print(self._filePath)
        self._img = image.imread(self._filePath)
        self._set_image_dimensions()

    def _set_image_dimensions(self):
        self._img_height = self._img.shape[0]
        self._img_width = self._img.shape[1]

    def show_image(self):
        pyplot.imshow(self._img)
        pyplot.show()

    def get_resolution(self):
        return self._img_width * self._img_height

    def get_image_dimensions(self):
        return self._img.shape

    def save_image(self, array, name):
        pyplot.imsave(name, array)

    def convert_to_bmp(self):
        img = pilimg.open(self._filePath)
        r, g, b = img.split()
        img = pilimg.merge("RGB", (r, g, b))
        img.save("file.bmp")


import src.scripts.exceptions as encrex
import numpy as np
from PIL import Image as pil


class EncryptEngine(object):

    @staticmethod
    def _generate_key(x, r, size):

        """
            Generating key using chaotic logistic map definition.
            Logistic map definition: f(x1) = r * x0 * (1 - x0)

            @params:
                @x -> Sequence starting point

                @r -> Control parameter.
                   -> It stands as the confusion factor over the key generation.
                   -> The larger it gets, the greater the confusion over the encrypted data will be.
                   -> It might range from 3.0 up to 4.0

                @size -> Represents the number of the generated sequences.
                      -> In the context of a picture encryption:
                            -> {photo_resolution} for .bmp files.
                            -> {photo_resolution} * {color_depth} for other types.
        """

        if x is None or x == 0:
            raise encrex.BadArgumentException(method_argument=x, reason="Argument value is 0 or None")

        if r is None or r == 0:
            raise encrex.BadArgumentException(method_argument=r, reason="Argument value is 0 or None")

        if size is None or size == 0:
            raise encrex.BadArgumentException(method_argument=size, reason="Argument value is 0 or None")

        if x < 0:
            raise encrex.BadArgumentException(method_argument=x, reason="Argument should be a positive value")

        if r < 0:
            raise encrex.BadArgumentException(method_argument=r, reason="Argument should be a positive value")

        if size < 0:
            raise encrex.BadArgumentException(method_argument=size, reason="Argument should be a positive value")

        if not(isinstance(x, float) or isinstance(x, int)):
            raise encrex.BadArgumentException(method_argument=x, reason="Argument should be integer or float value")

        if not(isinstance(r, float) or isinstance(r, int)):
            raise encrex.BadArgumentException(method_argument=r, reason="Argument should be integer or float value")

        if not(isinstance(size, float) or isinstance(size, int)):
            raise encrex.BadArgumentException(method_argument=size, reason="Argument should be integer or float value")

        if r < 3 or r > 4:
            raise encrex.ArgumentOutOfRangeException(method_argument=r, reason="Arg value not in (3.0, 4.0) range.")

        key = []

        for i in range(size):
            # logistic map definition
            x = r * x * (1 - x)
            key.append(int((x * pow(10, 16)) % 256))

        return key

    def encrypt_image(self, image_object, image_dimensions):
        """
            Performs encryption over image using chaos map generated key and pixels substitution and permutation.

            Returns: encrypted array

            @params:
                @image_object -> ndarray of the read image
                @image_dimensions -> tuple containing read dimensions in ({height}, {width}, {color_depth}) format


         """
        if image_object is None:
            raise encrex.BadArgumentException(method_argument=image_object, reason="Argument does not have a value")

        if len(image_dimensions) < 3:
            raise encrex.ArgumentOutOfRangeException(method_argument=image_dimensions,
                                                     reason="Given argument does not have the specific picture number of dimensions")

        _height = image_dimensions[0]
        _width = image_dimensions[1]
        _depth = image_dimensions[2]
        _resolution = _height * _width * _depth
        z = 0

        key = self._generate_key(0.1, 3.799, _resolution)

        encrypted_array = np.zeros(shape=[image_dimensions[0], image_dimensions[1], 3],
                                   dtype=np.uint8)

        for i in range(_height):
            for j in range(_width):
                for d in range(_depth):
                    encrypted_array[i, j, d] = int(int(image_object[i, j, d]) ^ int(key[z]))
                    z += 1

        return encrypted_array

    def decrypt_image(self, image_object, image_dimensions):
        """
            Performs decryption over image using chaos map generated key and pixels substitution and permutation.

            Returns: decryption array

            @params:
                @image_object -> ndarray of the read image
                @image_dimensions -> tuple containing read dimensions in ({height}, {width}, {color_depth}) format


         """
        _height = image_dimensions[0]
        _width = image_dimensions[1]
        _depth = image_dimensions[2]
        _resolution = _height * _width
        z = 0

        key = self._generate_key(0.2, 3.0000001, _height*3*_width)

        decrypted_array = np.zeros(shape=[image_dimensions[0], image_dimensions[1], 4],
                                   dtype=np.uint8)

        for i in range(_height):
            for j in range(_width):
                for d in range(_depth):
                    decrypted_array[i, j, d] = int(image_object[i, j, d]) ^ int(key[z])
                    z += 1

        return decrypted_array

    def encrypt_bmp_image(self, image_object, image_dimensions):
        """
            Performs encryption over image using chaos map generated key and pixels substitution and permutation.

            Returns: encrypted array

            @params:
                @image_object -> ndarray of the read image
                @image_dimensions -> tuple containing read dimensions in ({height}, {width}, {color_depth}) format


         """
        _height = image_dimensions[0]
        _width = image_dimensions[1]
        # _depth = image_dimensions[2]
        _resolution = _height * _width
        z = 0

        key = self._generate_key(0.2, 3.49, _resolution)

        encrypted_array = np.zeros(shape=[image_dimensions[0], image_dimensions[1], 4],
                                   dtype=np.uint8)

        for i in range(_height):
            for j in range(_width):
                encrypted_array[i, j] = int(image_object[i, j]) ^ int(key[z])
                z += 1

        return encrypted_array, key

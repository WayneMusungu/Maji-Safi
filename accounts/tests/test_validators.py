import unittest
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.validators import allow_only_images_valdators
from django.core.exceptions import ValidationError

class AllowOnlyImagesValidatorTestCase(unittest.TestCase):
    def test_valid_image(self):
        file = SimpleUploadedFile("picture.jpg", b"file_content")
        try:
            allow_only_images_valdators(file)
        except ValidationError as e:
            self.fail("Valid image raised ValidationError")

    def test_invalid_image(self):
        file = SimpleUploadedFile("file.txt", b"file_content")
        with self.assertRaises(ValidationError):
            allow_only_images_valdators(file)

if __name__ == '__main__':
    unittest.main()
import os
from django.core.exceptions import ValidationError

"""
Create a custom validator function that allows
only upload of Images and pass the function to the form field
"""
# Value is the file name of the file being uploaded


def allow_only_images_valdators(value):
    ext = os.path.splitext(value.name)[1]  # picture.jpg
    print(ext)
    valid_extensions = ['.png', '.jpg', '.jpeg']

    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file format. Allowed formats are: ' + str(valid_extensions))

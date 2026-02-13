from models.commands import Command
from PIL import Image
from utils.image_operations import grayscale

class GrayscaleCommand(Command):
    '''
    Command for converting to grayscale.

    :param value: True for grayscale else False for normal.
    :type value: bool
    '''
    def __init__(self, value: bool) -> None:
        self._value = value
        self._description = f"Applied grayscale." if self._value else f"Unapplied grayscale."

    def execute(self, image: Image.Image) -> Image.Image:
        '''
        Convert to grayscale

        :param image: The image to modify.
        :type image: Image.Image
        :return: The modified image.
        :rtype: Image.Image
        '''
        return grayscale(image) if self._value else image

    def get_description(self) -> None:
        return self._description
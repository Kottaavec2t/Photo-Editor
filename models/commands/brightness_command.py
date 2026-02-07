from commands import Command
from PIL import Image
from utils.image_operations import brightness

class BrightnessCommand(Command):
    '''
    Command for adjusting brightness.

    :param factor: The brightness factor (1 = normal, <1 = black, >1 = white).
    :type factor: float
    '''
    def __init__(self, factor: float) -> None:
        self._factor = factor
    
    def execute(self, image: Image.Image) -> Image.Image:
        '''
        Apply brightness adjustment.

        :param image: The image to modify.
        :type image: Image.Image
        :return: The modified image.
        :rtype: Image.Image
        '''
        return brightness(image, self._factor)

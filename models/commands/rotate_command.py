from models.commands import Command
from PIL import Image
from utils.image_operations import rotate

class RotateCommand(Command):
    '''
    Command for rotating an image.

    :param angle: The angle of rotate.
    :type angle: float
    '''
    def __init__(self, angle: float) -> None:
        self._angle = angle

    def execute(self, image: Image.Image) -> Image.Image:
        '''
        Apply rotation adjustment.

        :param image: The image to modify.
        :type image: Image.Image
        :return: The modified image.
        :rtype: Image.Image
        '''
        return rotate(image, self._angle)

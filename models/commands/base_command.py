from abc import ABC, abstractmethod
from PIL import Image

class Command(ABC):
    '''
    Base class for all commands.
    '''
    @abstractmethod
    def execute(self, image: Image.Image) -> Image.Image:
        '''
        Execute the command.

        :param image: The image to modify.
        :type image: Image.Image
        :return: The modified image.
        :rtype: Image.Image
        '''
        pass
    
    @abstractmethod
    def get_description(self) -> None:
        pass
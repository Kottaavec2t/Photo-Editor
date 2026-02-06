from typing import Tuple
from PIL import ImageEnhance, Image, ImageDraw

def grayscale(image: Image.Image) -> Image.Image:
    '''
    Convert image to black and white

    :param image: The image to convert
    :type image: Image.Image
    :return: The modified image
    :rtype: Image.Image
    '''
    image = image.convert('L')
    return image

def resize(image: Image.Image, xy: Tuple[int | float, int | float]) -> Image.Image:
    '''
    Resize image to given dimensions
    
    :param image: The image to resize
    :type image: Image.Image
    :param xy: The new dimensions (width, height)
    :type xy: Tuple[int | float, int | float]
    :return: The resized image
    :rtype: Image.Image
    '''
    image = image.resize(xy)
    return image

def brightness(image: Image.Image, factor: float) -> Image.Image:
    '''
    Adjust image brightness. Factor > 1 increases brightness, factor < 1 decreases it

    :param image: The image to adjust
    :type image: Image.Image
    :param factor: The brightness adjustment factor
    :type factor: float
    :return: The modified image
    :rtype: Image.Image
    '''
    enhancer = ImageEnhance.Brightness(image=image)
    image = enhancer.enhance(factor)
    return image

def rotate(image: Image.Image, angle) -> Image.Image:
    '''
    Rotate image by given angle
    
    :param image: The image to rotate
    :type image: Image.Image
    :param angle: The angle to rotate the image (in degrees)
    :type angle: float
    :return: The rotated image
    :rtype: Image.Image
    '''
    image = image.rotate(angle)
    return image

def crop(image: Image.Image, box: Tuple[int | float, int | float, int | float, int | float]) -> Image.Image:
    '''
    Crop image to given box and make the rest transparent
    
    :param image: The image to crop
    :type image: Image.Image
    :param box: The box to crop (left, upper, right, lower)
    :type box: Tuple[int | float, int | float, int | float, int | float]
    :return: The cropped and transparent image
    :rtype: Image.Image
    '''
    image = image.crop(box)
    alpha_image = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(alpha_image)
    draw.rectangle((box), fill=255)
    image.putalpha(alpha_image)
    return image

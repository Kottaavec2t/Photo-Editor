from typing import Tuple
from PIL import ImageEnhance, Image, ImageDraw

def black_and_white(image: Image.Image):
    '''Convert image to black and white.'''
    image = image.convert('L')
    return image

def resize(image: Image.Image, xy: Tuple[int | float, int | float]):
    '''Resize image to given dimensions.'''
    image = image.resize(xy)
    return image

def brightness(image: Image.Image, factor: float):
    '''Adjust image brightness. Factor > 1 increases brightness, factor < 1 decreases it.'''
    enhancer = ImageEnhance.Brightness(image=image)
    image = enhancer.enhance(factor)
    return image

def rotate(image: Image.Image, angle):
    '''Rotate image by given angle.'''
    image = image.rotate(angle)
    return image

def crop(image: Image.Image, box: Tuple[int | float, int | float, int | float, int | float]):
    '''Crop image to given box and make the rest transparent.'''
    image = image.crop(box)
    alpha_image = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(alpha_image)
    draw.rectangle((box), fill=255)
    image.putalpha(alpha_image)
    return image

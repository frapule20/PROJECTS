import os
import io
import numpy as np
from PIL import Image, ImageFilter
from torchvision import transforms
from sklearn.neighbors import KNeighborsRegressor
import joblib
import random


transform = transforms.Compose([
    transforms.Resize((244, 244)),
    transforms.ToTensor()
])

def add_noise(im):
    img_array = np.array(im, dtype=np.float32)
    noise = np.random.normal(0, 60, img_array.shape)
    noisy_image_array = img_array + noise
    noisy_image_array = np.clip(noisy_image_array, 0, 255)
    noisy_image = Image.fromarray(np.uint8(noisy_image_array))
    return noisy_image


def blur_image(image):
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius=4))
    return blurred_image


def add_jpeg_noise(image, quality=8):
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=quality)
    noisy_image = Image.open(buffer)
    return noisy_image
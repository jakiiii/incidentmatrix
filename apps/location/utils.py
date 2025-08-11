import os
from datetime import datetime


def division_image_directory_path(instance, filename):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%Y-%m-%d-%H-%M-%S")
    file_name, ext = os.path.splitext(filename)
    return f"division/{date_str}/{file_name}-{time_str}{ext}"


def district_image_directory_path(instance, filename):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%Y-%m-%d-%H-%M-%S")
    file_name, ext = os.path.splitext(filename)
    return f"district/{date_str}/{file_name}-{time_str}{ext}"

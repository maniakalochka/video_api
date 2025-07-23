"""
Скрипт для генерации тестовых данных в базе данных.
"""


import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "video_api.settings")
django.setup()

from videos.test_data_gen.gen_fake_data import generate_test_data

generate_test_data()

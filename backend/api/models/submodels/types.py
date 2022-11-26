import base64

from djongo import models


class Tag(models.Model):
    name = models.CharField(max_length=12)

    def __str__(self):
        return self.name


class File(models.Model):
    FILE_TYPE = [
        ("TXT", ".txt"),
        ("CSV", ".csv"),
        ("PDF", ".pdf"),
        ("IMG", ".img"),
        ("PNG", ".png"),
        ("JPG", ".jpg"),
        ("JPEG", ".jpeg"),
    ]

    type = models.CharField(max_length=10, choices=FILE_TYPE, default="TXT")
    content = models.TextField()

    def __str__(self):
        return base64.b64decode(str(self.content)).decode()


class OptionId(models.Model):
    value = models.CharField(max_length=12)

    def __str__(self):
        return str(self.value)

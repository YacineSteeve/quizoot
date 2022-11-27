import base64

from djongo import models


class Tag(models.Model):
    name = models.CharField(
        max_length=12, unique=True, help_text="The tag name or label."
    )

    def __str__(self):
        return self.name


class File(models.Model):
    # Supported file extensions.
    FILE_TYPE = [
        ("TXT", ".txt"),
        ("CSV", ".csv"),
        ("PDF", ".pdf"),
        ("IMG", ".img"),
        ("PNG", ".png"),
        ("JPG", ".jpg"),
        ("JPEG", ".jpeg"),
    ]

    _id = models.ObjectIdField()
    type = models.CharField(
        max_length=10, choices=FILE_TYPE, default="TXT", help_text="The file type."
    )
    content = models.TextField(
        help_text="Encoded `base64` string of the file's content."
    )

    def save(self, *args, **kwargs):
        self.content = base64.b64encode(self.content.value_to_string(self))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.content[:50]}..."


class OptionId(models.Model):
    _id = models.ObjectIdField()
    value = models.CharField(
        max_length=12, help_text="The Id of an existing Question Option object."
    )

    def __str__(self):
        return str(self.value)

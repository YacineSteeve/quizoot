from djongo import models


class Author(models.Model):
    first_name = models.CharField(max_length=12)
    last_name = models.CharField(max_length=12)
    pseudo = models.CharField(max_length=12)
    email = models.EmailField()

    def __str__(self):
        if self.pseudo:
            return str(self.pseudo)
        elif self.last_name:
            return f"{str(self.first_name).title()} {str(self.last_name).upper()}"
        else:
            return str(self.first_name)

from djongo import models


class Author(models.Model):
    first_name = models.CharField(
        max_length=50, help_text="The quiz author's first name."
    )
    last_name = models.CharField(
        max_length=50, null=True, blank=True, help_text="The quiz author's last name."
    )
    pseudo = models.CharField(
        max_length=12, null=True, blank=True, help_text="A pseudo for the quiz author."
    )
    email = models.EmailField(help_text="The quiz author's email.")

    class Meta:
        verbose_name_plural = " Authors"

    def save(self, *args, **kwargs) -> None:
        if self.pseudo == "":
            self.pseudo = None
        super().save(*args, *kwargs)

    def __str__(self) -> str:
        if self.pseudo:
            return str(self.pseudo)
        elif self.last_name:
            return f"{str(self.first_name).title()} {str(self.last_name).upper()}"
        else:
            return str(self.first_name)

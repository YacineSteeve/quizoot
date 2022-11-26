from djongo import models


class Grading(models.Model):
    point_value = models.IntegerField()
    feedback = models.OneToOneField('Feedback', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.point_value)


class Feedback(models.Model):
    explanation = models.TextField()
    when_wrong = models.TextField()
    when_right = models.TextField()

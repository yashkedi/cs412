from django.db import models

class Joke(models.Model):
    text = models.TextField()
    contributor = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.contributor}: {self.text[:50]}"

class Picture(models.Model):
    image_url = models.URLField(max_length=500)
    contributor = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.contributor}: {self.image_url[:50]}"

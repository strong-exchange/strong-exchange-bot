from django.db import models


class Currency(models.Model):
    base = models.CharField(max_length=3)
    target = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=15, decimal_places=10)
    date = models.DateField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.date} | {self.base} to {self.target} - {self.rate}"

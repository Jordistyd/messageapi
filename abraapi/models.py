from django.db import models


# Create your models here.
class Message(models.Model):
    """
    Class to represent single message in DB.

    sender: string representing user-name that sent message

    receiver: string representing user-name that got message

    message: string representing the message itself

    subject: string representing subject of message

    creation_date: time of creation, automatically added
    """

    sender = models.CharField(max_length=100)
    receiver = models.CharField(max_length=100)
    message = models.TextField()
    subject = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    objects = models.Manager()

    class Meta:
        # Order by time of creation
        ordering = ["-creation_date"]

    def __str__(self):
        return f"{self.sender} to {self.receiver}, {self.subject} Created at: {self.creation_date}"

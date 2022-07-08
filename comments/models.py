from django.db import models

from books.models import Book
from users.models import User


class Comment(models.Model):
    use_in_migrations = True
    comment_id = models.AutoField(primary_key=True)
    comment = models.TextField()
    reg_date = models.DateField()
    auto_recode = models.TextField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        db_table = "comments"

    def __str__(self):
        return f'{self.pk} {self.comment_id}'

from django.db import models

class Book(models.Model):
    use_in_migrations = True
    isbn = models.CharField(primary_key=True, max_length=30)
    author = models.TextField()
    book_title = models.TextField()
    category = models.TextField()
    book_img = models.FileField()
    book_info = models.TextField(null=True)

    class Meta:
        db_table = "books"

    def __str__(self):
        return f'{self.pk} {self.isbn}'

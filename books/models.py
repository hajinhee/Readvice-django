from django.db import models

class Book(models.Model):
    use_in_migrations = True
    isbn = models.CharField(primary_key=True, max_length=30)
    author = models.TextField()
    book_title = models.TextField()
    book_info = models.TextField()
    library_name = models.TextField()
    price = models.TextField()
    category = models.TextField()

    class Meta:
        db_table = "books"

    def __str__(self):
        return f'{self.pk} {self.isbn}'
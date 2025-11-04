from django.db import models
from students.models import Student

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

class BookIssue(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.student.name} - {self.book.title}'

class Fine(models.Model):
    book_issue = models.OneToOneField(BookIssue, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Fine for {self.book_issue}'

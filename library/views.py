from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Book, BookIssue, Fine
from .serializers import BookSerializer, BookIssueSerializer, FineSerializer
from .permissions import IsAdminOrReadOnly, IsStudentOwner

class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or edited.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class BookIssueViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows book issues to be viewed or edited.
    """
    queryset = BookIssue.objects.all()
    serializer_class = BookIssueSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return BookIssue.objects.all()
        elif user.role == 'Student':
            return BookIssue.objects.filter(student__user=user)
        return BookIssue.objects.none()

    def get_permissions(self):
        if self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated, IsStudentOwner]
        return super().get_permissions()

class FineViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows fines to be viewed or edited.
    """
    queryset = Fine.objects.all()
    serializer_class = FineSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return Fine.objects.all()
        elif user.role == 'Student':
            return Fine.objects.filter(book_issue__student__user=user)
        return Fine.objects.none()

    def get_permissions(self):
        if self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated, IsStudentOwner]
        return super().get_permissions()

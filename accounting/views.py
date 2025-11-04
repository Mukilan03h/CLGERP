from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Ledger, Transaction
from .serializers import LedgerSerializer, TransactionSerializer
from .permissions import IsAccountantOrAdmin

class LedgerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing ledgers.
    """
    queryset = Ledger.objects.all()
    serializer_class = LedgerSerializer
    permission_classes = [IsAuthenticated, IsAccountantOrAdmin]

class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing transactions.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated, IsAccountantOrAdmin]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

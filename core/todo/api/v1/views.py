from rest_framework.viewsets import ModelViewSet
from .paginations import DefaultPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated


from .serializers import TaskSerializer, Task


class TaskList(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    pagination_class = DefaultPagination
    queryset = Task.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ["complete"]
    search_fields = ["title"]
    ordering_field = "_all_"

    def get_queryset(self, *args, **kwargs):
        return (
            super().get_queryset(*args, **kwargs).filter(user=self.request.user).all()
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

from rest_framework.viewsets import ReadOnlyModelViewSet


class FindingView(ReadOnlyModelViewSet):

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

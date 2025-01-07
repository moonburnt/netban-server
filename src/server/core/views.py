from rest_framework.views import APIView
from .permissions import HasCorrectAPIVersionHeader
from .mixins import FormattedResponseMixin


class NetbanAPIView(FormattedResponseMixin, APIView):
    permission_classes = APIView.permission_classes + [
        HasCorrectAPIVersionHeader,
    ]

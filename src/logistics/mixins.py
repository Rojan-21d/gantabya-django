from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class ConsignorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated and self.request.user.user_type == 'consignor':
            return True
        raise PermissionDenied("You must be a consignor to access this page.")

class CarrierRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if self.request.user.is_authenticated and self.request.user.user_type == 'carrier':
            return True
        raise PermissionDenied("You must be a carrier to access this page.")
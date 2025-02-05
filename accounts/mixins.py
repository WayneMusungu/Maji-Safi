"""
This module contains custom mixins for role-based access control.

Mixins:
- CustomerRoleRequiredMixin: Restricts customers from accessing supplier pages.
- SupplierRoleRequiredMixin: Restricts suppliers from accessing customer pages.
"""

from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class CustomerRoleRequiredMixin(UserPassesTestMixin):
    """Restricting customer from accessing the supplier's page"""
    def test_func(self):
        if self.request.user.role == 2:  # Customer role
            return True
        raise PermissionDenied


class SupplierRoleRequiredMixin(UserPassesTestMixin):
    """Restricting Supplier from accessing the customers page"""
    def test_func(self):
        if self.request.user.role == 1:  # Supplier role
            return True
        raise PermissionDenied

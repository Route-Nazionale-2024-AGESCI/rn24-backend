from rest_framework import permissions


class CanScanQRPermission(permissions.BasePermission):
    """
    Custom permission to only allow users to scan QR codes if they are
    authenticated and have a valid ticket.
    """

    def has_permission(self, request, view):
        if request.user.has_perm("people.can_scan_qr"):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return False

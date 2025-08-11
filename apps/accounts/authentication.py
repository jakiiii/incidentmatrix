# from django.contrib.auth.mixins import AccessMixin
# from django.contrib import messages
# from django.shortcuts import redirect
# from django.core.exceptions import PermissionDenied
#
#
# class SubscriberRequiredMixin(AccessMixin):
#     """Verify that the current user is authenticated and is a subscriber."""
#
#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return self.handle_no_permission()
#
#         if not request.user.is_subscriber:
#             # Add a message to inform the user
#             messages.error(request, "You must be a subscriber to access this page.")
#             # Redirect to a custom page, e.g., a subscription page or home page
#             return redirect('accounts:login')  # Replace 'subscription_page' with your actual URL name
#
#         return super().dispatch(request, *args, **kwargs)

"""
Admin configuration optimizations
"""
from django.contrib import admin
from django.db import models


# Disable autocomplete_fields where not needed to improve performance
# Autocomplete can be slow on large tables

# Override admin site to disable unnecessary features
class OptimizedAdminSite(admin.AdminSite):
    """
    Optimized admin site that disables slow features
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Disable recent actions panel (can be slow)
        self.enable_nav_sidebar = False


# Replace default admin site with optimized version
# Uncomment if you want to use the optimized site:
# admin_site = OptimizedAdminSite(name='admin')


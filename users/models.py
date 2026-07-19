from django.contrib.auth.models import AbstractUser
from django.db import models


from django.db import models


class TimeStampedModel(models.Model):
    """
    Abstract base model that provides timestamp fields
    for all inheriting models.
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="Record creation timestamp."
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last updated timestamp."
    )

    class Meta:
        abstract = True

class User(AbstractUser, TimeStampedModel):
    """
    Our own user, based on Django's built-in User.

    We just add the two extra fields the frontend's "Users" page needs:
    - role: what the person is allowed to do
    - building: which building they mainly work on (optional)

    Everything else (name, email, password, active/inactive, last login)
    already comes for free from AbstractUser.
    """

    class Role(models.TextChoices):
        ADMIN = "Admin", "Admin"
        MANAGER = "Manager", "Manager"
        OPERATOR = "Operator", "Operator"
        VIEWER = "Viewer", "Viewer"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.VIEWER)
    building = models.ForeignKey(
        "buildings.Building",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.role})"

from django.db import models
from django.utils import timezone
from django.utils.timesince import timesince
from django.utils.translation import gettext_lazy as _

from uuid import uuid4


class DBBase(models.Model):
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    guid = models.UUIDField(unique=True, default=uuid4, editable=False, verbose_name=_("Unique ID"),
                            help_text=_("This field is automatically determined by the system, do not interfere.")
                            )

    ORDER_BY = (
        ("created", _("Created Ascendant"),),
        ("-created", _("Created Descendant"),),
        ("modified", _("Modified Ascendant"),),
        ("-modified", _("Modified Descendant"),),
    )
    ORDER_BY_MODIFIED_DEFAULT = "-modified"
    ORDER_BY_CREATED_DEFAULT = "-created"

    class Meta:
        abstract = True

    def get_dict(self) -> dict:
        """
        Returns a dictionary containing information about the model

        :return: A dictionary containing information about the model
        :rtype: dict
        """
        return {
            "created": timezone.localtime(self.created).isoformat() if self.created else None,
            "createds": timesince(self.created) if self.created else None,
            "modified": timezone.localtime(self.modified).isoformat() if self.modified else None,
            "modifieds": timesince(self.modified) if self.modified else None,
            "isedited": self.isedited,
        }

    @property
    def isedited(self) -> bool:
        """
        Returns whether the model has been edited or not

        :return: True if the model has been edited, False otherwise
        :rtype: bool
        """
        return False if self.created.strftime('%Y-%m-%d %H:%M:%S') == self.modified.strftime(
            '%Y-%m-%d %H:%M:%S') else True

    def get_uid(self) -> str:
        """
        Returns the model's GUID as a string

        :return: The model's GUID as a string
        :rtype: str
        """
        return str(self.guid)

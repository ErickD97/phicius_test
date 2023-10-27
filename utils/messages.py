from enum import Enum

from django.utils.translation import gettext_lazy as _


class MESSAGES(Enum):
    SYS001 = _("A single user can't play both teams.")

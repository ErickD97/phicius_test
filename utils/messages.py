from enum import Enum

from django.utils.translation import gettext_lazy as _


class MESSAGES(Enum):
    SYS001 = _("A single user can't play both teams.")
    SYS002 = _("Invalid column or/and row.")
    SYS003 = _("{} object does not exist.")
    SYS004 = _("Not a vaid position, columns go from 'A' to 'C' and rows from 1 to 3.")
    SYS005 = _("Position already taken.")
    SYS006 = _("Not a vaid ID, this field should be a numerical string.")

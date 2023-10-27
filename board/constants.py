from django.utils.translation import gettext_lazy as _

STATUS = (
    (1, _("Unfinished")),
    (2, _("Cross Victory")),
    (3, _("Circle Victory")),
    (4, _("Draw")),
)


def get_default_positions():
    return {"A": [], "B": [], "C": []}

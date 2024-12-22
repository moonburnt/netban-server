from django.db.models import IntegerChoices


class UserRestrictionType(IntegerChoices):
    BAN = (0, "Ban")

from . import models


def get_all_clubs():
    return models.Club.objects.all()

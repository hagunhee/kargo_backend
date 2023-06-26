from . import models


def get_all_users():
    return models.User.objects.all()


def get_all_influencers():
    return models.Influencer.objects.all()

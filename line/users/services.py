from django.shortcuts import get_object_or_404

from products.models import File
from users.models import Profile


class UserServices(object):
    def __init__(self,
                 user,
                 last_name="",
                 first_name="",
                 phone="",
                 region="",
                 image=None):

        self.user = user
        self.last_name = last_name
        self.first_name = first_name
        self.phone: str = phone
        self.region: str = region
        self.image = image

    def update_profile(self):
        user_image = get_object_or_404(File, id=self.user.profile.image.id)
        user_profile = get_object_or_404(Profile, id=self.user.profile.id)

        user_image.image = self.image
        user_image.save()

        self.user.first_name = self.first_name
        self.user.last_name = self.last_name
        self.user.save()

        user_profile.phone = self.phone
        user_profile.region = self.region
        user_profile.save()




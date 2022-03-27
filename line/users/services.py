from django.shortcuts import get_object_or_404

from products.models import File


class UserServices:
    def __init__(self, user,
                 first_name=None,
                 last_name=None,
                 phone=None,
                 region=None,
                 image=None):

        self.user = user
        self.last_name = last_name
        self.first_name = first_name
        self.phone = phone,
        self.region = region,
        self.image = image

    def update_profile(self):
        user_image = get_object_or_404(File, id=self.user.profile.image.id)
        user_image.image = self.image
        user_image.save()

        self.user.first_name = self.first_name
        self.user.last_name = self.last_name
        self.user.profile.phone = self.phone
        self.user.profile.region = self.region
        self.user.save()



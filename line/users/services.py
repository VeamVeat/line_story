from django.shortcuts import render, get_object_or_404

from products.models import File


class UserServices:
    def __init__(self, user, model=None, last_name=None, first_name=None):
        self.user = user
        self.model = model
        self.last_name = last_name
        self.first_name = first_name

    def update_full_name(self, first_name, last_name):
        user = get_object_or_404(self.model, self.first_name, self.last_name)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

    def update_image(self, image):
        user_image = File.objects.get(id=self.user.image.id)
        user_image.image = image
        user_image.save()


class ProfileServices:
    def __init__(self, user, model=None, phone=None, region=None):
        self.user = user
        self.model = model
        self.phone = phone
        self.region = region

    def update_profile(self, phone, region):
        user_profile = get_object_or_404(self.model, self.phone, self.region)
        user_profile.phone = phone
        user_profile.region = region
        user_profile.save(update_fields=['phone', 'region'])


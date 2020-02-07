"""django-artwork views"""

from django.core.exceptions import ObjectDoesNotExist

from django.contrib import messages as msg

from .forms import ArtworkActiveForm


class ArtworkActiveMixin:

    def get_artwork_active_form(self):
        # Returns ArtworkActiveForm (essentially a form input with the name 'active'), main purpose is for validation
        return ArtworkActiveForm(prefix=self.get_prefix(), data=self.request.POST, files=self.request.FILES)

    def form_valid(self, form):
        result = super().form_valid(form)
        artwork_active_form = self.get_artwork_active_form()
        # Set active image
        if artwork_active_form.is_valid():
            try:
                if self.object.artwork_active.id != int(artwork_active_form.cleaned_data['active']):
                    self.object.artwork_active = form.get_queryset().get(pk=int(artwork_active_form.cleaned_data['active']))
                    self.object.save()
                    msg.add_message(self.request, msg.SUCCESS,
                                    f'Changed active artwork for "{self.object}" to "{self.object.artwork_active}"')
            except ObjectDoesNotExist:
                pass
        # Pick an image to set as active image if not yet set
        try:
            # Reload object in case active artwork was deleted
            obj = self.get_object()
            if obj.artwork_active is None:
                self.object.artwork_active = form.get_queryset().all()[0]
                self.object.save()
                msg.add_message(self.request, msg.SUCCESS,
                                f'Changed active artwork for "{self.object}" to "{self.object.artwork_active}"')
        except (ObjectDoesNotExist, IndexError):
            pass
        return result

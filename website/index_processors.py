"""
Utility class that helps haystack index m2m relations after instance it is
first save.
"""
from django.db import models
from haystack.signals import BaseSignalProcessor
from haystack.exceptions import NotHandled

from website.projects.models import Project
from website.tasks import update_object, remove_object


class BaseSignal(BaseSignalProcessor):
    "BaseSignalProcessor had to be rewritten to account for m2m relationships"

    def handle_save(self, sender, instance, **kwargs):
        """
        Given an individual model instance, determine which backends the
        update should be sent to & update the object on those backends.
        """
        # import pdb; pdb.set_trace()
        # changed_fields = kwargs['update_fields']
        # if not changed_fields:
        #     return False
        using_backends = self.connection_router.for_write(instance=instance)
        sender = sender if isinstance(instance, sender) else instance.__class__
        for using in using_backends:
            try:
                index = self.connections[using].get_unified_index().get_index(sender)
                update_object.delay(index, instance, using=using)
            except NotHandled:
                # TODO: Maybe log it or let the exception bubble?
                pass

    def handle_delete(self, sender, instance, **kwargs):
        """
        Given an individual model instance, determine which backends the
        delete should be sent to & delete the object on those backends.
        """
        using_backends = self.connection_router.for_write(instance =instance)
        sender = sender if isinstance(instance, sender) else instance.__class__
        for using in using_backends:
            try:
                index = self.connections[using].get_unified_index().get_index(sender)
                remove_object.delay(index, instance, using=using)
            except NotHandled:
                # TODO: Maybe log it or let the exception bubble?
                pass

    def removed_unplublished(self, sender, instance, **kwargs):
        """
        Checks the status of a project and and if it has changed from
        published to any other status removes it from the index.
        """
        # import pdb; pdb.set_trace()
        if isinstance(instance, Project):
            update_fields = kwargs.get('update_fields')
            if 'status' in update_fields:
                if not instance.status == instance.PUBLISHED:
                    self.handle_delete(sender, instance, **kwargs)


class M2MRealtimeSignalProcessor(BaseSignal):
    """
    Allows for observing when saves, deletes and m2m_changed fire &
    automatically updates the search engine appropriately.
    """
    def setup(self):
        # Naive (listen to all model saves).
        models.signals.pre_save.connect(self.removed_unplublished)
        models.signals.post_save.connect(self.handle_save)
        models.signals.m2m_changed.connect(self.handle_save)
        models.signals.post_delete.connect(self.handle_delete)
        # Efficient would be going through all backends & collecting all models
        # being used, then hooking up signals only for those.

    def teardown(self):
        # Naive (listen to all model saves).
        models.signals.pre_save.disconnect(self.removed_unplublished)
        models.signals.post_save.disconnect(self.handle_save)
        models.signals.m2m_changed.disconnect(self.handle_save)
        models.signals.post_delete.disconnect(self.handle_delete)
        # Efficient would be going through all backends & collecting all models
        # being used, then disconnecting signals only for those.

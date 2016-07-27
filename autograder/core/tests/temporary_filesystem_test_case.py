import os
import shutil

from django.core.cache import cache
from django.conf import settings
from django.test import TransactionTestCase
from django.test.utils import override_settings


@override_settings(MEDIA_ROOT=os.path.join(settings.BASE_DIR, 'tmp_filesystem'))
class TemporaryFilesystemTestCase(TransactionTestCase):
    """
    Base class for test cases that test code that performs
    filesystem operations. Overrides the MEDIA_ROOT setting

    The setUp() method does the following:
        - Creates a temporary directory for the test to use.
        - Saves the current settings.MEDIA_ROOT,
          then modifies it to refer to the temporary directory.
    The tearDown() method does the following:
        - Restores the original settings.MEDIA_ROOT
        - Deletes the temporary directory created in setUp()

    Since setUp() and tearDown() are called for each test case,
    you won't have to worry about tests interfering with each other.
    """

    def setUp(self):
        super().setUp()

        # HACK
        cache.clear()

        if os.path.isdir(settings.MEDIA_ROOT):
            print('Deleting temp filesystem')
            self.assertTrue(settings.MEDIA_ROOT.endswith('tmp_filesystem'))
            shutil.rmtree(settings.MEDIA_ROOT)

    def tearDown(self):
        shutil.rmtree(settings.MEDIA_ROOT)

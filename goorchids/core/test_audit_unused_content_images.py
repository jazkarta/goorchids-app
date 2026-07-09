from django.test import TestCase

from goorchids.core.management.commands.audit_unused_content_images import (
    derived_content_image_keys,
)


class ContentImageAuditTests(TestCase):

    def test_derived_content_image_keys_include_thumbnail_keys(self):
        keys = derived_content_image_keys(
            'taxon-images/Orchidaceae/example.jpg')

        self.assertEqual(keys, set([
            'taxon-images/Orchidaceae/example.jpg',
            'taxon-images-160x149/Orchidaceae/example.jpg',
            'taxon-images-239x239/Orchidaceae/example.jpg',
            'taxon-images-1000s1000/Orchidaceae/example.jpg',
        ]))

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from gobotany.core import models as gobotany_models
from goorchids.core.admin import ContentImageAdminForm


class ContentImageAdminFormTests(TestCase):

    def test_missing_image_type_is_a_form_error(self):
        image = SimpleUploadedFile(
            'test.gif',
            b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00'
            b'\xff\xff\xff,\x00\x00\x00\x00\x01\x00\x01\x00'
            b'\x00\x02\x02D\x01\x00;',
            content_type='image/gif')
        form = ContentImageAdminForm(data={
            'alt': 'Stem detail',
            'rank': 1,
            'creator': 'test-photographer',
        }, files={
            'image': image,
        })

        self.assertFalse(form.is_valid())
        self.assertIn('image_type', form.errors)


class ContentImageModelValidationTests(TestCase):

    def setUp(self):
        self.family = gobotany_models.Family.objects.create(
            name='Orchidaceae',
            common_name='orchid family')
        self.genus = gobotany_models.Genus.objects.create(
            name='Example',
            common_name='example genus',
            family=self.family)
        self.taxon = gobotany_models.Taxon.objects.create(
            scientific_name='Example orchid',
            family=self.family,
            genus=self.genus,
            taxonomic_authority='Tester')
        self.image_type = gobotany_models.ImageType.objects.create(
            name='habit')
        self.content_type = ContentType.objects.get_for_model(
            gobotany_models.Taxon)

    def test_duplicate_canonical_image_raises_validation_error(self):
        gobotany_models.ContentImage.objects.create(
            alt='First',
            rank=1,
            creator='test-photographer',
            image_type=self.image_type,
            content_type=self.content_type,
            object_id=self.taxon.id)

        image = gobotany_models.ContentImage(
            alt='Second',
            rank=1,
            creator='test-photographer',
            image_type=self.image_type,
            content_type=self.content_type,
            object_id=self.taxon.id)

        with self.assertRaisesMessage(
                ValidationError,
                'There is already a canonical (rank 1) habit image'):
            image.clean()

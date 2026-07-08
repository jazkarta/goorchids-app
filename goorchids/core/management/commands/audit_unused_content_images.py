from decimal import Decimal

from boto.s3.connection import S3Connection
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from gobotany.core.models import ContentImage


THUMBNAIL_SUFFIXES = ('160x149', '239x239', '1000s1000')
DEFAULT_PREFIXES = tuple(
    ['taxon-images'] +
    ['taxon-images-{}'.format(suffix) for suffix in THUMBNAIL_SUFFIXES])


def derived_content_image_keys(image_name):
    keys = set()
    if not image_name:
        return keys
    keys.add(image_name)
    if '/' in image_name:
        for suffix in THUMBNAIL_SUFFIXES:
            keys.add(image_name.replace('/', '-{}/'.format(suffix), 1))
    return keys


class Command(BaseCommand):
    help = (
        'Report content image objects present on S3 but not referenced by '
        'ContentImage records. This command is read-only.')

    def add_arguments(self, parser):
        parser.add_argument(
            '--bucket',
            default=getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None),
            help='S3 bucket to audit. Defaults to AWS_STORAGE_BUCKET_NAME.')
        parser.add_argument(
            '--prefix',
            action='append',
            dest='prefixes',
            help=(
                'S3 prefix to audit. Can be supplied multiple times. Defaults '
                'to taxon image originals and generated thumbnail prefixes.'))
        parser.add_argument(
            '--storage-price-per-gb-month',
            type=Decimal,
            default=Decimal('0.023'),
            help=(
                'Storage price used for the monthly estimate, in dollars per '
                'GB-month. Defaults to 0.023.'))
        parser.add_argument(
            '--show-keys',
            action='store_true',
            help='Print every unreferenced key found.')

    def handle(self, *args, **options):
        bucket_name = options['bucket']
        if not bucket_name:
            raise CommandError(
                'No bucket configured. Set AWS_STORAGE_BUCKET_NAME or pass '
                '--bucket.')

        referenced_keys = set()
        for image_name in ContentImage.objects.exclude(image='').values_list(
                'image', flat=True):
            referenced_keys.update(derived_content_image_keys(image_name))

        prefixes = options['prefixes'] or DEFAULT_PREFIXES
        bucket = S3Connection().get_bucket(bucket_name)

        total_count = 0
        total_size = 0
        unused_count = 0
        unused_size = 0
        unused_keys = []

        for prefix in prefixes:
            normalized_prefix = prefix.rstrip('/') + '/'
            for key in bucket.list(prefix=normalized_prefix):
                if key.name.endswith('/'):
                    continue
                total_count += 1
                total_size += key.size
                if key.name not in referenced_keys:
                    unused_count += 1
                    unused_size += key.size
                    if options['show_keys']:
                        unused_keys.append(key.name)

        unused_gb = Decimal(unused_size) / Decimal(1024 ** 3)
        monthly_cost = unused_gb * options['storage_price_per_gb_month']

        self.stdout.write('Bucket: {}'.format(bucket_name))
        self.stdout.write('Prefixes: {}'.format(', '.join(prefixes)))
        self.stdout.write('Referenced content image keys: {}'.format(
            len(referenced_keys)))
        self.stdout.write('S3 objects scanned: {}'.format(total_count))
        self.stdout.write('S3 bytes scanned: {}'.format(total_size))
        self.stdout.write('Unreferenced S3 objects: {}'.format(unused_count))
        self.stdout.write('Unreferenced S3 bytes: {}'.format(unused_size))
        self.stdout.write('Estimated monthly storage cost: ${:.4f}'.format(
            monthly_cost))

        if options['show_keys']:
            self.stdout.write('')
            self.stdout.write('Unreferenced keys:')
            for key_name in unused_keys:
                self.stdout.write(key_name)

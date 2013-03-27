from os.path import abspath, dirname
from django.conf import settings
from gobotany.mapping.map import (NorthAmericanPlantDistributionMap, NAMESPACES,
                                  Path)
from goorchids.core.models import Taxon


GRAPHICS_ROOT = abspath(dirname(__file__) + '/../core/static/graphics')

# To differentiate
CANADIAN_PROVINCES = {
    'ab': u'Alberta',
    'bc': u'British Columbia',
    'mb': u'Manitoba',
    'nb': u'New Brunswick',
    'nl': u'Newfoundland and Labrador',
    'nt': u'Northwest Territories',
    'ns': u'Nova Scotia',
    'nu': u'Nunavut',
    'on': u'Ontario',
    'pe': u'Prince Edward Island',
    'qc': u'Quebec',
    'sk': u'Saskatchewan',
    'yt': u'Yukon'
}

PRESENT_COLOR = '#78bf47'
ABSENT_COLOR = '#fff'
STATES_MAP = dict((v, k) for k, v in settings.STATE_NAMES.iteritems())


class NorthAmericanOrchidDistributionMap(NorthAmericanPlantDistributionMap):

    PATH_NODES_XPATH = 'svg:path|svg:g|svg:g/svg:g|svg:g/svg:path|svg:g/svg:g/svg:path'

    def __init__(self):
        blank_map_path = GRAPHICS_ROOT + '/na-state-distribution.svg'
        super(NorthAmericanPlantDistributionMap, self).__init__(
            blank_map_path)

    def set_plant(self, scientific_name):
        self.scientific_name = scientific_name
        taxon = Taxon.objects.get(scientific_name=scientific_name)
        self.distribution_records = taxon.character_values.filter(
            character__short_name='state_distribution')
        if self.distribution_records:
            self._add_name_to_title(self.scientific_name)

    def shade(self):
        """Set the colors of the states and provinces based
        on distribution data.
        """
        if self.distribution_records:
            path_nodes = self.svg_map.xpath(self.PATH_NODES_XPATH,
                namespaces=NAMESPACES)
            matching_regions = {}
            for record in self.distribution_records:
                region = STATES_MAP.get(record.value_str)
                region = ((region in CANADIAN_PROVINCES and 'ca-' or 'us-') +
                          region)
                matching_regions[region] = True

            for node in path_nodes:
                if node.get('style'):
                    node_id = node.get('id').lower()
                    box = Path(node)
                    if node_id in matching_regions:
                        box.color(PRESENT_COLOR)
                    else:
                        box.color(ABSENT_COLOR)
        return self

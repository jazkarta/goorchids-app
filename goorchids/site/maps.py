from os.path import abspath, dirname
from gobotany.mapping.map import (NorthAmericanPlantDistributionMap, NAMESPACES,
                                  Path)
from goorchids.core.models import (Taxon, RegionalConservationStatus,
                                   STATE_RANK_CODES, CANADIAN_RANK_CODES)


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

RANKS = STATE_RANK_CODES.copy()
RANKS.update(CANADIAN_RANK_CODES)
PRESENT_COLOR = '#78bf47'
ABSENT_COLOR = '#fff'


class NorthAmericanOrchidDistributionMap(NorthAmericanPlantDistributionMap):

    PATH_NODES_XPATH = 'svg:path|svg:g|svg:g/svg:g|svg:g/svg:path|svg:g/svg:g/svg:path'

    def __init__(self):
        blank_map_path = GRAPHICS_ROOT + '/na-state-distribution.svg'
        super(NorthAmericanPlantDistributionMap, self).__init__(
            blank_map_path)

    def set_plant(self, scientific_name):
        self.scientific_name = scientific_name
        taxon = Taxon.objects.get(scientific_name=scientific_name)
        self.distribution_records = RegionalConservationStatus.objects.filter(
            taxon=taxon)
        if self.distribution_records:
            self._add_name_to_title(self.scientific_name)

    def shade(self):
        """Set the colors of the states and provinces based
        on distribution data.
        """
        if self.distribution_records:
            path_nodes = self.svg_map.xpath(self.PATH_NODES_XPATH,
                namespaces=NAMESPACES)
            for record in self.distribution_records.all():
                region = record.region
                rank = record.rank
                region = ((region in CANADIAN_PROVINCES and 'ca-' or 'us-') +
                          region)
                for node in path_nodes:
                    node_id = node.get('id').lower()
                    if node_id == region:
                        box = Path(node)
                        rank = RANKS.get(rank, '').lower()
                        if rank and 'extinct' not in rank and 'extirpated' not in rank:
                            box.color(PRESENT_COLOR)
                        else:
                            box.color(ABSENT_COLOR)
                        break   # Move on to the next distribution record.
        return self

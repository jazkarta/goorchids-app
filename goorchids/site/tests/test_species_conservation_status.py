from django.test import TestCase

from gobotany.core import models as gobotany_models

from goorchids.core.models import GoOrchidTaxon, RegionalConservationStatus


class SpeciesPageTestCase(TestCase):

    def setUp(self):
        self.family = gobotany_models.Family.objects.create(
            name='Orchidaceae',
            common_name='orchid family')
        self.genus = gobotany_models.Genus.objects.create(
            name='Dendrophylax',
            common_name='ghost orchid',
            family=self.family)
        self.taxon = GoOrchidTaxon.objects.create(
            scientific_name='Dendrophylax lindenii',
            family=self.family,
            genus=self.genus,
            taxonomic_authority='Tester',
            ready_for_display=True)
        pilegroup = gobotany_models.PileGroup.objects.create(
            name='Monocots',
            slug='monocots')
        pile = gobotany_models.Pile.objects.create(
            name='Orchid monocots',
            slug='orchid-monocots',
            pilegroup=pilegroup)
        self.taxon.piles.add(pile)

    def get_species_page(self):
        response = self.client.get('/species/dendrophylax/lindenii/')
        self.assertEqual(response.status_code, 200)
        return response.content.decode('utf-8')


class ConservationStatusDisplayTests(SpeciesPageTestCase):

    def test_ranks_without_a_value_are_left_out(self):
        self.taxon.global_rank = 'G3'
        self.taxon.save()

        page = self.get_species_page()

        self.assertIn('Global Rank', page)
        self.assertIn('Vulnerable', page)
        self.assertNotIn('US Status', page)
        self.assertNotIn('Canadian Status', page)
        self.assertNotIn('N/A', page)

    def test_regional_statuses_without_a_value_are_left_out(self):
        self.taxon.global_rank = 'G3'
        self.taxon.save()
        RegionalConservationStatus.objects.create(
            taxon=self.taxon,
            region='fl',
            status='E')

        page = self.get_species_page()

        self.assertIn('Conservation status for: Florida', page)
        self.assertIn('Florida Status', page)
        self.assertIn('Endangered', page)
        self.assertNotIn('Florida Rank', page)
        self.assertNotIn('<th>Wetland Status</th>', page)
        self.assertNotIn('N/A', page)

    def test_a_species_without_any_status_shows_no_table(self):
        page = self.get_species_page()

        self.assertNotIn('<table class="conservation-status', page)
        self.assertNotIn('region-switcher', page)
        self.assertIn('No conservation status information is available',
                      page)
        self.assertNotIn('N/A', page)

    def test_a_region_without_any_status_is_not_offered(self):
        RegionalConservationStatus.objects.create(
            taxon=self.taxon,
            region='fl')

        page = self.get_species_page()

        self.assertNotIn('Florida', page)
        self.assertNotIn('N/A', page)

    def test_statuses_that_have_a_value_are_still_shown(self):
        self.taxon.global_rank = 'G3'
        self.taxon.us_status = 'LE'
        self.taxon.ca_rank = '1'
        self.taxon.save()
        RegionalConservationStatus.objects.create(
            taxon=self.taxon,
            region='fl',
            status='E',
            rank='S1',
            wetland_status='FACW')

        page = self.get_species_page()

        for expected in ('Vulnerable', 'Listed Endangered', 'At Risk',
                         'Endangered', 'Highly State Rare',
                         'Facultative Wetland'):
            self.assertIn(expected, page)
        self.assertIn('<option value="fl">Florida</option>', page)
        self.assertNotIn('N/A', page)


class FactsAboutDisplayTests(SpeciesPageTestCase):

    def test_facts_about_is_left_out_when_empty(self):
        page = self.get_species_page()

        self.assertNotIn('Facts About', page)
        self.assertNotIn('N/A', page)

    def test_facts_about_is_shown_when_present(self):
        self.taxon.factoid = 'Grows without leaves.'
        self.taxon.save()

        page = self.get_species_page()

        self.assertIn('Facts About', page)
        self.assertIn('Grows without leaves.', page)

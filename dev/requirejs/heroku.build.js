/* RequireJS Build profile for production deployment to Heroku instance */
({
    appDir: '../../external/gobotany-app/gobotany/static/scripts',
    dir: 'build',
    baseUrl: '.',
    mainConfigFile: '../../goorchids/core/static/scripts/require_config.js',

    findNestedDependencies: true,
    removeCombined: false,
    preserveLicenseComments: false,
    paths: {
        'select2': '../../../../../goorchids/core/static/scripts/select2',
        'orchid_site': '../../../../../goorchids/core/static/scripts/orchid_site'
    },

    modules: [
        {
            name: 'gobotany.application',
            include: [
                'lib/require',

                'dkey/dkey',
                'editor/cv',
                'mapping/geocoder',
                'mapping/google_maps',
                'mapping/marker_map',
                'mapping/place_parser',
                'plantshare/ask_the_botanist',
                'plantshare/checklist_form',
                'plantshare/delete_checklist',
                'plantshare/delete_sighting',
                'plantshare/find_people',
                'plantshare/find_people_profile',
                'plantshare/manage_sightings',
                'plantshare/redirect_old_question_urls',
                'plantshare/terms_of_agreement',
                'plantshare/your_profile',
                'plantshare/plantshare',
                'plantshare/registration_complete',
                'plantshare/sighting',
                'plantshare/sightings',
                'plantshare/sightings_locator',
                'plantshare/sightings_locator_part',
                'plantshare/sightings_map',
                'plantshare/sign_up',
                'plantshare/new_sighting',
                'plantshare/new_checklist',
                'plantshare/edit_checklist',
                'plantshare/checklists',
                'simplekey/simple',
                'simplekey/results',
                'taxa/species',
                'taxa/family',
                'taxa/genus',
                'site/help',
                'site/advanced_map',
                'site/glossary',
                'site/species_list',
                'site/home',
                'site/maps_test',
                'util/suggester_init',
                'util/formset',
                'util/image_popup',
                'util/location_field_init',
                'orchid_site/species',
                'orchid_site/results',
                'orchid_site/protect_images'
            ],
            create: true
        }
    ]
})

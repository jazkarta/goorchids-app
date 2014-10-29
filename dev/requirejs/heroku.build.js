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
                'plantshare/myprofile',
                'plantshare/plantshare',
                'plantshare/registration_complete',
                'plantshare/sightings_locator',
                'plantshare/sightings_locator_part',
                'plantshare/sightings_map',
                'plantshare/sign_up',
                'plantshare/new_sighting',
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
                'util/location_field_init',
                'orchid_site/species',
                'orchid_site/results',
                'orchid_site/protect_images'
            ],
            create: true
        }
    ]
})

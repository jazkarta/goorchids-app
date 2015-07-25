requirejs.config({
    baseUrl: "/static/scripts",
    paths: {
        'bridge': 'bridge',
        'dkey': 'dkey',
        'lib': 'lib',
        'mapping': 'mapping',
        'markerclusterer': 'lib/markerclusterer_compiled',
        'plantpreview': 'plantpreview',
        'plantshare': 'plantshare',
        'select2': 'select2',
        'simplekey': 'simplekey',
        'site': 'site',
        'taxa': 'taxa',
        'util': 'util',
        'orchid_site': 'orchid_site'
    },
    shim: {
        'markerclusterer': {
            exports: "MarkerClusterer"
        }
    }
});

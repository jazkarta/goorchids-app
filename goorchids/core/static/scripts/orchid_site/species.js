/*
 * Code for adding behavior to species pages.
 */
define([
    'bridge/jquery',
    'bridge/shadowbox',
    'select2/select2.min'
], function($, Shadowbox, shadowbox_init) {
    $(document).ready(function() {
        // Because the map is in an <object> element, a transparent div
        // is needed to make it clickable. Make this div cover the link
        // that appears below the map, too, for one large clickable area.
        var transparent_div =
            $('.namap div.trans').first();
        transparent_div.click($.proxy(function(event) {
            event.preventDefault();
            // Open the North America distribution map in a lightbox.
            var content_element =
                $('.namap div').first();
            var width = jQuery(window).width()*0.85;
            var height = Math.min(jQuery(window).height(), width);
            width = Math.min(width, height*1.01);
            Shadowbox.open({
                content: content_element.html(),
                player: 'html',
                height: height,
                width: width
            });
        }));

        // Set up the conservation status region switcher
        var update_region_tables = function() {
            $('table.conservation-status').addClass('hidden');
            $('table.conservation-status[data-region="' + $('#region-switcher').val() + '"]').removeClass('hidden');
        };
        $('#region-switcher').select2({width: '100%'}).change(function() { update_region_tables(); });
        update_region_tables();

        // Set up accordions for characteristics
        $('.accordion-header').each(function() {
            var $header = $(this);
            var $accordion = $header.closest('.accordion');
            var $body = $accordion.children('.accordion-body');
            $header.prepend('<span class="accordion-icon"><span class="icon-plus"></span></span>');
            $header.click(function(e) {
                e.preventDefault();
                $header.toggleClass('active');
                if ($header.hasClass('active')) {
                    $header.html($header.html().replace('Show', 'Hide'));
                } else {
                    $header.html($header.html().replace('Hide', 'Show'));
                }
                $body.toggleClass('hidden');
                $header.find('.accordion-icon span').toggleClass('icon-plus').toggleClass('icon-minus');
            });
        });
    });

});

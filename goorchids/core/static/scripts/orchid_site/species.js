/*
 * Code for adding behavior to species pages.
 */
define([
    'bridge/jquery',
    'bridge/shadowbox',
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
        }    ));
    });

});

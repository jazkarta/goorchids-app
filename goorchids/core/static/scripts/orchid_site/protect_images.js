define([
    'bridge/jquery',
], function($) {
    // Disable image right-clicking
    $(document).on('contextmenu', 'img', function(e) {
        alert('Images on this site are protected under copyright law.');
        e.preventDefault();
    });
});

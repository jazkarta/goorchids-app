define([
    'bridge/jquery',
], function($) {
    // Disable image right-clicking
    $(document).on('contextmenu', 'img', function(e) {
        alert('ATTENTION: Most images on this site are protected under copyright law and copying them from this site is not allowed.');
        e.preventDefault();
    });
});

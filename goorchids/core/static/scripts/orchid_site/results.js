/*
 * Code for adding behavior to level 3 results page.
 */
define([
    'bridge/jquery',
    'bridge/ember',
    'select2/select2.min',
], function($, Ember) {
    $('.toplink').click(function(e) {
        e.preventDefault();
        $('body,html').animate({scrollTop: $('#question-nav').offset().top}, 200);
    });
    // Register handlebars helper function to turn newlines into <br>
    Handlebars.registerHelper("linebreaksbr", function (text) {
        text = text.toString();
        return text.replace(/(\r\n|\n|\r)/gm, '<br />');
    });
    // Make Ember selectboxes use select2
    // (from http://stackoverflow.com/questions/14910785/ember-select-with-custom-select-plugin-how-to-bind-the-two)
    Ember.Select.reopen({
        didInsertElement: function() {
            this.$().select2();
        },
        contentChanged: function() {
            Ember.run.next(this, function() {
                this.$().select2();
            });
        }.observes('content')
    });
});

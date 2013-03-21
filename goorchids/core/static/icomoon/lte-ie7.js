/* Load this script using conditional IE comments if you need to support IE 7 and IE 6. */

window.onload = function() {
	function addIcon(el, entity) {
		var html = el.innerHTML;
		el.innerHTML = '<span style="font-family: \'icomoon\'">' + entity + '</span>' + html;
	}
	var icons = {
			'icon-search' : '&#x21;',
			'icon-plus' : '&#x22;',
			'icon-minus' : '&#x23;',
			'icon-checkmark' : '&#x24;',
			'icon-caret-up' : '&#x25;',
			'icon-caret-down' : '&#x26;',
			'icon-caret-left' : '&#x27;',
			'icon-caret-right' : '&#x28;',
			'icon-circle-arrow-up' : '&#x29;',
			'icon-circle-arrow-down' : '&#x2a;',
			'icon-cancel-circle' : '&#x2b;',
			'icon-close' : '&#x2c;'
		},
		els = document.getElementsByTagName('*'),
		i, attr, html, c, el;
	for (i = 0; i < els.length; i += 1) {
		el = els[i];
		attr = el.getAttribute('data-icon');
		if (attr) {
			addIcon(el, attr);
		}
		c = el.className;
		c = c.match(/icon-[^\s'"]+/);
		if (c && icons[c[0]]) {
			addIcon(el, icons[c[0]]);
		}
	}
};
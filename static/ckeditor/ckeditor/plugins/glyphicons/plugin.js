/*
	Author	: Michael Janea (http://michaeljanea.com)
	Version	: 2.2
*/

CKEDITOR.plugins.add('glyphicons', {
	requires: 'widget,colordialog',
    icons	: 'glyphicons',
    init	: function(editor){
		editor.widgets.add('Glyphicons', {
			button			: 'Glyphicons',
			template		: '<span class="" style=""></span>',
			dialog			: 'glyphiconsDialog',
			allowedContent	: 'span(*){*}',
			upcast			: function(element){
                return element.name == 'span' && element.hasClass('glyphicon');
            },
			init			: function(){
				this.setData('class', this.element.getAttribute('class'));
				this.setData('color', this.element.getStyle('color'));
				this.setData('size', this.element.getStyle('font-size'));
            },
			data			: function(){
				var istayl = '';
				this.element.setAttribute('class', this.data.class);
				istayl += this.data.color != '' ? 'color:' + this.data.color + ';' : '';
				istayl += this.data.size != '' ? 'font-size:' + parseInt(this.data.size) + 'px;' : '';
				istayl != '' ? this.element.setAttribute('style', istayl) : '';
			}
		});

		editor.ui.addButton('Glyphicons', {
	        command : 'glyphicons',
	        icon    : this.path + 'icons/glyphicons.png',
	    });

		CKEDITOR.dialog.add('glyphiconsDialog', this.path + 'dialogs/glyphicons.js');
		CKEDITOR.document.appendStyleSheet(CKEDITOR.plugins.getPath('glyphicons') + 'css/style.css');
    }
});

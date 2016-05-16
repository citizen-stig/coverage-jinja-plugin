Jinja Coverage Plugin
=====================

This is a draft of plugin for coverage.py for [Jinja2](http://jinja.pocoo.org/docs/dev/)

It doesn't work right now and it's possible, that it would not work at all.


How It Works
============
The main problem of this plugin is to map executed lines back to HTML lines

Jinja2 [Template](http://jinja.pocoo.org/docs/dev/api/#jinja2.Template) object has a not very much information about it,
only some data in ```_debug_info``` attribute.

It looks like this attribute is used for pretty printing traceback, 
so it only contains mapping to some parts of the template, which might cause  exception.

TBD
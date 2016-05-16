# -*- encoding: utf-8 -*-
import os.path
import unittest
import pdb
import coverage
import jinja2

from coverage.test_helpers import TempDirMixin
import dis


class JinjaPluginTestCase(TempDirMixin, unittest.TestCase):

    def do_jinja_coverage(self, template, context=None):
        context = context if context is not None else {}
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(self.temp_dir))
        jinja_template = env.get_template(template)
        # print(dis.dis(jinja_template))
        cov = coverage.Coverage(source=["."])
        cov.config.plugins.append("jinja_coverage")
        cov.start()
        text = jinja_template.render(**context)
        cov.stop()
        cov.save()
        line_data = cov.data.lines(os.path.realpath(template))
        return text, line_data

    def test_one_line(self):
        self.make_file("template.html", "Hello\n")
        text, line_data = self.do_jinja_coverage("template.html")
        # self.assertEqual(text, "Hello\n")
        self.assertEqual(line_data, [1])

    def test_several_lines(self):
        self.make_file("template.html", "Line1\nLine2\nLine3\n")
        text, line_data = self.do_jinja_coverage("template.html")
        # self.assertEqual(text, "Hello\n")
        self.assertEqual(line_data, [1, 2, 3])

    def test_empty_lines_at_the_end(self):
        self.make_file("template.html", "Line1\nLine2\nLine3\n\n\n\n")
        text, line_data = self.do_jinja_coverage("template.html")
        # self.assertEqual(text, "Hello\n")
        self.assertEqual(line_data, [1, 2, 3])

    def test_3_lines_with_block(self):
        text = """{% block content %}
        Hello
        {% endblock %}"""
        self.make_file("template.html", text)
        text, line_data = self.do_jinja_coverage("template.html")
        # self.assertEqual(text, "Hello\n")
        self.assertEqual(line_data, [1, 2, 3])

    def test_if(self):
        text = """{% block content %}
            {% if v1 == 2 %}
                Two!
            {% else %}:
                Not Two!
            {% endif %}
            {% endblock %}"""
        self.make_file("if.html", text)
        text, line_data = self.do_jinja_coverage("if.html", {'v1': 2})
        self.assertEqual(line_data, [1, 2, 3, 6, 7])

    def test_else(self):
        text = """{% block content %}
            {% if v1 == 2 %}
                Two!
            {% else %}:
                Not Two!
            {% endif %}
            {% endblock %}"""
        self.make_file("if.html", text)
        text, line_data = self.do_jinja_coverage("if.html", {'v1': 5})
        self.assertEqual(line_data, [1, 2, 4, 5, 6, 7])

    def test_if_intro_outro(self):
        text = """<html>
            <head>
                <title>Title</title>
            </head>
            {% block content %}
            <body>
            <p>In</p>
            {% if v3 == "v3" %}
                <p>{{ v1 }}</p>
            {% else %}
                <p>{{ v2 }}</p>
            {% endif %}
            {% endblock %}
            <p>Test</p>
            <p>Test2</p>
            </html>"""
        self.make_file("if.html", text)
        context = {x: x for x in ('v1', 'v2', 'v3')}
        text, line_data = self.do_jinja_coverage("if.html", context=context)
        expected = [x for x in range(1, 17) if x not in (10, 11)]
        self.assertEqual(sorted(line_data), expected)

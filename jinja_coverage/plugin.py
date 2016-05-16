# -*- encoding: utf-8 -*-
"""
Coverage Plugin for Jinja2 Template Engine
"""
import coverage.plugin

debug = True


class JinjaPlugin(coverage.plugin.CoveragePlugin):

    def file_tracer(self, filename):
        if filename.endswith('.html'):
            return FileTracer(filename)


class FileTracer(coverage.plugin.FileTracer):
    def __init__(self, filename):
        self.filename = filename

    def source_filename(self):
        return self.filename

    def line_number_range(self, frame):
        template = frame.f_globals.get('__jinja_template__')
        if template is None:
            return -1, -1
        lines_map = get_line_map(template)
        if not lines_map:
            return 1, get_template_lines_number(template)
        keys = sorted(list(lines_map.keys()))
        smallest = keys[0]
        largest = keys[-1]

        if frame.f_lineno < smallest:
            if debug:
                print('f_line no {0} < smallest {1}, return 1, {2}'.format(
                    frame.f_lineno, smallest, lines_map[smallest] - 1))
            return 1, lines_map[smallest] - 1
        elif frame.f_lineno > largest:
            start = lines_map[largest] + 1
            end = get_template_lines_number(template)
            if debug:
                print('f_line {0} > largest {2}, return {2}, {3}'.format(
                    frame.f_lineno, largest, start, end))
            return start, end
        elif smallest <= frame.f_lineno < largest:
            if frame.f_lineno in lines_map:
                start = lines_map[frame.f_lineno]
                next_key_index = keys.index(frame.f_lineno) + 1
                end = lines_map[keys[next_key_index]] - 1
                if debug:
                    print('f_line {0}, map {1}, return {2}, {3}'.format(
                        frame.f_lineno, lines_map, start, end))
                return start, end
        return -1, -1


def get_template_lines_number(template):
    with open(template.filename) as template_file:
        lines_count = sum(1 for _ in template_file)
    return lines_count


def get_line_map(template):
    lines_map = {}
    if template._debug_info:
        # _debug_info = '7=8&9=17'
        for pair in template._debug_info.split('&'):
            original, compiled = pair.split('=')
            original, compiled = int(original), int(compiled)
            lines_map[compiled] = original
    return lines_map

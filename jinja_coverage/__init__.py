# -*- encoding: utf-8 -*-
from .plugin import JinjaPlugin


def coverage_init(reg, options):
    reg.add_file_tracer(JinjaPlugin())

# -*- coding: utf-8 -*-
# !/usr/bin/env python
__author__ = 'maxwu'


from random import randint
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView


class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels."""
        #return ["January", "February", "March", "April", "May", "June", "July"]
        return ["4/20/2016",
                "4/23/2016",
                "4/25/2016",
                "5/2/2016",
                "5/9/2016",
                "5/16/2016"]

    def get_data(self):
        """Return 3 datasets to plot."""

        #return [[75, 44, 92, 11, 44, 95, 35],
        #        [41, 92, 18, 3, 73, 87, 92],
        #       [87, 21, 94, 3, 90, 13, 65]]
        return [
            [377, 377, 377, 467, 478, 431],
            [136, 139, 139, 142, 163, 234],
            [389, 389, 388, 413, 425, 498],
        ]

line_chart = TemplateView.as_view(template_name='line_chart.html')
line_chart_json = LineChartJSONView.as_view()

if __name__ == '__main__':
    pass
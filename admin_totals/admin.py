# coding=utf-8
from __future__ import division, print_function, unicode_literals

from django.contrib import admin
from django.contrib.admin.views.main import ChangeList


class ChangeListTotals(ChangeList):
    def get_results(self, *args, **kwargs):
        super(ChangeListTotals, self).get_results(*args, **kwargs)
        if hasattr(self.model_admin, 'list_totals'):
            self.aggregations = []
            list_totals = dict(self.model_admin.list_totals)
            for field in self.list_display:
                selector = self.aggregations if self.model_admin.limit_to_page else self.queryset
                if field in list_totals:
                    selector.append(
                        self.result_list.aggregate(agg=list_totals[field](field))['agg'])
                else:
                    selector.append('')


class ModelAdminTotals(admin.ModelAdmin):
    change_list_template = 'admin_totals/change_list_totals.html'
    limit_to_page = True

    def get_changelist(self, request, **kwargs):
        return ChangeListTotals

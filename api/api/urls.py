from django.urls import path, include
from django.urls import path, register_converter
from datetime import datetime
from dashboard.viewset import *
from api.views_teldafax import teldafax, Teldafax_status, GetStatusConnectionsTeldafax, \
    TeldafaxErrorTablesAndStatusInIt, GetConnectionsTeldafax, GetConnectionsVariablesTeldafax, \
    TeldafaxErrorArchiveTablesAndStatusInIt

from api.views_compressor_unit import davlenie_graf, statusError, State_color, StateTempPres, duration


class DateConverter:
    regex = '\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d')

    def to_url(self, value):
        return value

class DateUnix:
    regex = '\d{10}'

    def to_python(self, value):
        return datetime.fromtimestamp(int(value)).date()

    def to_url(self, value):
        return value


register_converter(DateConverter, 'yyyy')
register_converter(DateUnix, 'unixdate')

urlpatterns = [
    path('duration/<unixdate:date>/day/', DurationIntervalDayViews.as_view(), name="duration_day"),
    path('duration/<unixdate:date>/shift/<int:id>/', DurationIntervalShiftViews.as_view(), name="duration_shift"),
    path('remainder/<unixdate:date>/', RemainderViews.as_view(), name='remainder'),
    path('edition/<unixdate:date>/month/', EditionMonthViews.as_view(), name='edition_month'),
    path('edition/<unixdate:date>/day/', EditionDayViews.as_view(), name='edition_day'),
    path('edition/<unixdate:date>/shift/<int:id>/', EditionShiftViews.as_view(), name='edition_shift'),
    path('sumexpense/<unixdate:date>/month/', SumexpenseMonthViews.as_view(), name='sumexpense_month'),
    path('sumexpense/<unixdate:date>/day/', SumexpenseDayViews.as_view(), name='sumexpense_day'),
    path('sumexpense/<unixdate:date>/shift/<int:id>/', SumexpenseShiftViews.as_view(), name='sumexpense_shift'),
    path('energyconsumption/<unixdate:date>/month/', EnergyConsumptionMonthViews.as_view(), name='energyconsumption_month'),
    path('energyconsumption/<unixdate:date>/day/', EnergyConsumptionDayViews.as_view(), name='energyconsumption_day'),
    path('energyconsumption/<unixdate:date>/shift/<int:id>/', EnergyConsumptionShiftViews.as_view(), name='energyconsumption_shift'),
    path('specificconsumption/<unixdate:date>/month/', SpecificConsumptionMonthViews.as_view(), name='specificconsumption_month'),
    path('specificconsumption/<unixdate:date>/day/', SpecificConsumptionDayViews.as_view(), name='specificconsumption_day'),
    path('specificconsumption/<unixdate:date>/shift/<int:id>/', SpecificConsumptionShiftViews.as_view(), name='specificconsumption_shift'),
    path('comparison/month/<unixdate:date1>/<unixdate:date2>/', ComparisonMonthViews.as_view(), name='comparison_month'),
    path('comparison/day/<unixdate:date1>/<unixdate:date2>/', ComparisonDayViews.as_view(), name='comparison_day'),
    path('comparison/shift/<unixdate:date1>/<int:id1>/<unixdate:date2>/<int:id2>/', ComparisonShiftViews.as_view(), name='comparison_shift'),
    path('teldafax/value/', teldafax.as_view(), name='teldafax_value'),
    path('teldafax/status/', Teldafax_status.as_view(), name='teldafax_status'),

    path('teldafax/messages/alarms/', TeldafaxErrorTablesAndStatusInIt.as_view()),
    path('teldafax/messages/alarms/archive/', TeldafaxErrorArchiveTablesAndStatusInIt.as_view()),
    path('teldafax/status/connections/', GetStatusConnectionsTeldafax.as_view()),
    path('teldafax/connections/', GetConnectionsTeldafax.as_view()),
    path('teldafax/connections/variables/<int:id>/', GetConnectionsVariablesTeldafax.as_view()),
    path('user/', RoleViews.as_view()),


    path('compressor/davlenie_graph/', davlenie_graf.as_view()),
    path('compressor/statecolor/', State_color.as_view()),
    path('compressor/data/', StateTempPres.as_view()),
    path('compressor/statuserror/', statusError.as_view()),
    path('compressor/dur/', duration.as_view())

]

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .calculate_tool_dashboard import calculate_edition, calculate_edition_shift, calculate_sumexpense, calculate_sumexpense_shift, calculate_specific, calculate_specific_shift, calculate_duration_shift
from .serializer import *
from users.models import UserP
from datetime import datetime, timedelta, time
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from structure.models import Agreagat


#@permission_classes([IsAuthenticated])
class RoleViews(APIView):
    def get(self, request):
        role = UserP.objects.get(id=request.user.pk).role_set.all()
        are = [None, None, None, None, None, None]
        for i in role:
            for r in i.dashboard.all():
                if r.name == "DurationIntervalDay":
                    are[0] = r.name
                elif r.name == "Storehouse":
                    are[1] = r.name
                elif r.name == "EditionDay":
                    are[2] = r.name
                elif r.name == "SumexpenseDay":
                    are[3] = r.name
                elif r.name == "EnergyConsumptionDay":
                    are[4] = r.name
                elif r.name == "SpecificConsumptionDay":
                    are[5] = r.name
        a = are
        return Response(a)





#виджет «Продолжительность работы, ч», вкладка день
@permission_classes([IsAuthenticated])
class DurationIntervalDayViews(APIView):
    def get(self, request, date):
        role = UserP.objects.get(id=request.user.pk).role_set.all()
        for r in role:
            for d in r.dashboard.all():
                if d.name == 'DurationIntervalDay':
                    dash = d.name
        try:
            art = globals()[dash].objects.filter(date=date)
            if len(art) == 0:
                start = time(0,0,1)
                end = time(23,59,59)
                art = calculate_duration_shift(date, start, end)
            sum = 0
            format = "%H:%M:%S"
            data1 =[]
            for i in art:
                duration = datetime.strptime(str(i.end), format)-datetime.strptime(str(i.start), format)
                duration = duration.total_seconds() / 3600
                k = {
                        "start":i.start,
                        "end":i.end,
                        "duration":duration
                }
                data1.append(k)
                sum = sum + duration
            data = {
                "interval": data1,
                "sum":sum
            }
        except UnboundLocalError:
            data = {"error":'not Role'}
            return Response(data,status=status.HTTP_404_NOT_FOUND)
        return Response(data)


#виджет «Продолжительность работы, ч», вкладка смена
@permission_classes([IsAuthenticated])
class DurationIntervalShiftViews(APIView):
    def get(self, request, date, id):
        a = Agreagat.objects.get(pk=dist_table['id_agreagat']).parent.shift_set.all()#get(pk=id)
        a = a[id-1]
        if DurationIntervalDay.objects.filter(date=date, start__gte=a.start, end__lte=a.end).exists():
            k = DurationIntervalDay.objects.filter(date=date, start__gte=a.start, end__lte=a.end).order_by('start')
        else:
            calculate_duration_shift(date, a.start, a.end)
            k = DurationIntervalDay.objects.filter(date=date, start__gte=a.start, end__lte=a.end).order_by('start')
        sum = 0
        format = "%H:%M:%S"
        data = []
        for i in k:
            duration = datetime.strptime(str(i.end), format) - datetime.strptime(str(i.start), format)
            duration = duration.total_seconds() / 3600
            k = {
                "start": i.start,
                "end": i.end,
                "duration": duration
            }
            data.append(k)
            sum = sum + duration
        data = {
            "interval": data,
            "sum": sum
        }
        return Response(data)


#виджет «Остатки на складах»
@permission_classes([IsAuthenticated])
class RemainderViews(APIView):
    def get(self, request, date):
        role = UserP.objects.get(id=request.user.pk).role_set.all()
        for r in role:
            for d in r.dashboard.all():
                if d.name == 'Storehouse':
                    dash = d.name
        try:
            art = globals()[dash].objects.all()
            storehouse = []
            isosum =0
            polsum = 0
            pensum = 0
            for a in art:
                iso = []
                iso_prog = []
                pen = []
                pen_prog = []
                pol = []
                pol_prog = []
                for i in a.substance_set.filter(short_name='ISO'):
                    iso.append(i.value_date(date))
                    x = float('{:.1f}'.format((i.value_date(date)/39000)*100))
                    iso_prog.append(x)
                    isosum =isosum + i.value_date(date)
                for i in a.substance_set.filter(short_name='PEN'):
                    pen.append(i.value_date(date))
                    x = float('{:.1f}'.format((i.value_date(date)/39000)*100))
                    pen_prog.append(x)
                    pensum = pensum + i.value_date(date)
                for i in a.substance_set.filter(short_name='POL'):
                    pol.append(i.value_date(date))
                    x = float('{:.1f}'.format((i.value_date(date) / 39000) * 100))
                    pol_prog.append(x)
                    polsum = polsum + i.value_date(date)
                data = {
                    "name": a.name,
                    "iso": iso,
                    "iso_prog": iso_prog,
                    "pol": pol,
                    "pol_prog": pol_prog,
                    "pen": pen,
                    "pen_prog": pen_prog
                }
                storehouse.append(data)
            data = {
                "storehouse": storehouse,
                "in_total": {
                    "iso": isosum,
                    "pol": polsum,
                    "pen": pensum
                }
            }
        except UnboundLocalError:
            data = {"error":'not Role'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        return Response(data)

#виджет «Выпуск панелей» для вкладки «день»
@permission_classes([IsAuthenticated])
class EditionDayViews(APIView):
    def get(self, request, date):
        role = UserP.objects.get(id=request.user.pk).role_set.all()
        for r in role:
            for d in r.dashboard.all():
                if d.name == 'EditionDay':
                    dash = d.name
        try:
            if globals()[dash].objects.filter(date=date).exists():
                art = globals()[dash].objects.get(date=date)
            else:
                art = calculate_edition(date)
            delt = timedelta(days=1)
            date_del = date-delt
            if globals()[dash].objects.filter(date=date_del).exists():
                art_del = globals()[dash].objects.get(date=date_del)
            else:
                art_del = calculate_edition(date_del)
            if art_del.suitable != 0:
                change_suitable = (((art.suitable/art_del.suitable)-1)*100)
            else:
                change_suitable = 0
            if art_del.substandard != 0:
                change_substandard = (((art.substandard/art_del.substandard)-1)*100)
            else:
                change_substandard = 0
            if art_del.defect != 0:
                change_defect = (((art.defect/art_del.defect)-1)*100)
            else:
                change_defect = 0
            if art_del.flooded != 0:
                change_flooded = (((art.flooded/art_del.flooded)-1)*100)
            else:
                change_flooded = 0
            if art_del.sum != 0:
                change_sum = (((art.sum/art_del.sum)-1)*100)
            else:
                change_sum = 0
            if art.sum != 0:
                data = {
                    "suitable": float('{:.2f}'.format(art.suitable)),
                    # "change_suitable": round(change_suitable),
                    "change_suitable": round(art.suitable*100/art.sum),
                    "substandard": float('{:.2f}'.format(art.substandard)),
                    # "change_substandard": round(change_substandard),
                    "change_substandard": round(art.substandard*100/art.sum),
                    "defect": float('{:.2f}'.format(art.defect)),
                    # "change_defect": round(change_defect),
                    "change_defect": round(art.defect*100/art.sum),
                    "flooded": art.flooded,
                    # "change_flooded": round(change_flooded),
                    "sum": art.sum,
                    # "change_sum": round(change_sum)
                }
            else:
                data = {
                    "suitable": float('{:.2f}'.format(art.suitable)),
                    "change_suitable": round(change_suitable),
                    "substandard": float('{:.2f}'.format(art.substandard)),
                    "change_substandard": round(change_substandard),
                    "defect": float('{:.2f}'.format(art.defect)),
                    "change_defect": round(change_defect),
                    "flooded": art.flooded,
                    # "change_flooded": round(change_flooded),
                    "sum": art.sum,
                    # "change_sum": round(change_sum)
                }
        except UnboundLocalError:
            data = {"error":'not Role'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        return Response(data)


#виджет «Выпуск панелей» для вкладки «месяц»
@permission_classes([IsAuthenticated])
class EditionMonthViews(APIView):
    def get(self, request, date):
        role = UserP.objects.get(id=request.user.pk).role_set.all()
        for r in role:
            for d in r.dashboard.all():
                if d.name == 'EditionDay':
                    dash = d.name
        delt = timedelta(days=1)
        data_pred = date - timedelta(days=date.day)
        sh = date.day
        dat = date
        #текущий месяц
        suitable = 0
        substandard = 0
        defect = 0
        flooded = 0
        sum = 0
        try:
            while sh != 0:
                if globals()[dash].objects.filter(date=dat).exists():
                    art = globals()[dash].objects.get(date=dat)
                else:
                    art = calculate_edition(dat)
                suitable = suitable + art.suitable
                substandard = substandard + art.substandard
                defect = defect + art.defect
                flooded = flooded + art.flooded
                sum = sum + art.sum
                dat = dat - delt
                sh = sh - 1


            #пред. месяц
            sh = data_pred.day
            suitable_pr = 0
            substandard_pr = 0
            defect_pr = 0
            flooded_pr = 0
            sum_pr = 0
            while sh != 0:
                if globals()[dash].objects.filter(date=data_pred).exists():
                    art = globals()[dash].objects.get(date=data_pred)
                else:
                    art = calculate_edition(data_pred)
                suitable_pr = suitable_pr + art.suitable
                substandard_pr = substandard_pr + art.substandard
                defect_pr = defect_pr + art.defect
                flooded_pr = flooded_pr + art.flooded
                sum_pr = sum_pr + art.sum
                data_pred = data_pred - delt
                sh = sh - 1

            if suitable_pr != 0:
                change_suitable = (((suitable/suitable_pr)-1)*100)
            else:
                change_suitable = 0
            if substandard_pr != 0:
                change_substandard = (((substandard/substandard_pr)-1)*100)
            else:
                change_substandard = 0
            if defect_pr != 0:
                change_defect = (((defect/defect_pr)-1)*100)
            else:
                change_defect = 0
            if flooded_pr != 0:
                change_flooded = (((flooded/flooded_pr)-1)*100)
            else:
                change_flooded = 0
            if sum_pr != 0:
                change_sum = (((sum/sum_pr)-1)*100)
            else:
                change_sum = 0
            if sum != 0:
                # data = {
                #     "suitable": float('{:.2f}'.format(art.suitable)),
                #     # "change_suitable": round(change_suitable),
                #     "change_suitable": round(art.suitable*100/art.sum),
                #     "substandard": float('{:.2f}'.format(art.substandard)),
                #     # "change_substandard": round(change_substandard),
                #     "change_substandard": round(art.substandard*100/art.sum),
                #     "defect": float('{:.2f}'.format(art.defect)),
                #     # "change_defect": round(change_defect),
                #     "change_defect": round(art.defect*100/art.sum),
                #     "flooded": art.flooded,
                #     # "change_flooded": round(change_flooded),
                #     "sum": art.sum,
                #     # "change_sum": round(change_sum)
                # }
                data = {
                    "suitable": float('{:.2f}'.format(suitable)),
                    "change_suitable": round(suitable*100/sum),
                    "substandard": float('{:.2f}'.format(substandard)),
                    "change_substandard": round(substandard*100/sum),
                    "defect": float('{:.2f}'.format(defect)),
                    "change_defect": round(defect*100/sum),
                    "flooded": flooded,
                    # "change_flooded": round(change_flooded),
                    "sum": float('{:.2f}'.format(sum)),
                    # "change_sum": round(change_sum)
                }
            else:
                data = {
                    "suitable": float('{:.2f}'.format(suitable)),
                    "change_suitable": 0,
                    "substandard": float('{:.2f}'.format(substandard)),
                    "change_substandard": 0,
                    "defect": float('{:.2f}'.format(defect)),
                    "change_defect": 0,
                    "flooded": flooded,
                    # "change_flooded": round(change_flooded),
                    "sum": float('{:.2f}'.format(sum)),
                    # "change_sum": round(change_sum)
                }
        except UnboundLocalError:
            data = {"error":'not Role'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        return Response(data)




#виджет «Выпуск панелей» для вкладки «смена»
@permission_classes([IsAuthenticated])
class EditionShiftViews(APIView):
    def get(self, request, date, id):
        a = Agreagat.objects.get(pk=dist_table['id_agreagat']).parent.shift_set.all()
        c = a[id-1]
        k = calculate_edition_shift(date, c.start, c.end)
        if id == 1:
            k_pred = calculate_edition_shift(date, a[len(a)-1].start, a[len(a)-1].end)
        else:
            k_pred = calculate_edition_shift(date, a[id-2].start, a[id-2].end)

        if k_pred["suitable"] != 0:
            change_suitable = (((k["suitable"] / k_pred["suitable"]) - 1) * 100)
        else:
            change_suitable = 0
        if k_pred["substandard"] != 0:
            change_substandard = (((k["substandard"] / k_pred["substandard"]) - 1) * 100)
        else:
            change_substandard = 0
        if k_pred["defect"] != 0:
            change_defect = (((k["defect"] / k_pred["defect"]) - 1) * 100)
        else:
            change_defect = 0
        if k_pred["flooded"] != 0:
            change_flooded = (((k["flooded"] / k_pred["flooded"]) - 1) * 100)
        else:
            change_flooded = 0
        if k_pred["sum"] != 0:
            change_sum = (((k["sum"] / k_pred["sum"]) - 1) * 100)
        else:
            change_sum = 0
        if k["sum"] != 0:
            data = {
                "suitable": float('{:.2f}'.format(k["suitable"])),
                # "change_suitable": round(change_suitable),
                "change_suitable": round(k["suitable"]*100/k["sum"]),
                "substandard": float('{:.2f}'.format(k["substandard"])),
                # "change_substandard": round(change_substandard),
                "change_substandard": round(k["substandard"]*100/k["sum"]),
                "defect": float('{:.2f}'.format(k["defect"])),
                # "change_defect": round(change_defect),
                "change_defect": round(k["defect"]*100/k["sum"]),
                "flooded": k["flooded"],
                # "change_flooded": round(change_flooded),
                "sum": k["sum"],
                # "change_sum": round(change_sum)
            }
        else:
            data = {
                "suitable": float('{:.2f}'.format(k["suitable"])),
                "change_suitable": round(0),
                "substandard": float('{:.2f}'.format(k["substandard"])),
                "change_substandard": round(0),
                "defect": float('{:.2f}'.format(k["defect"])),
                "change_defect": round(0),
                "flooded": k["flooded"],
                # "change_flooded": round(change_flooded),
                "sum": k["sum"],
                # "change_sum": round(change_sum)
            }
        return Response(data)





#виджет «Суммарный расход» для вкладки «день»
@permission_classes([IsAuthenticated])
class SumexpenseDayViews(APIView):
    def get(self, request, date):
        role = UserP.objects.get(id=request.user.pk).role_set.all()
        for r in role:
            for d in r.dashboard.all():
                if d.name == 'SumexpenseDay':
                    dash = d.name
        try:
            if globals()[dash].objects.filter(date=date).exists():
                art = globals()[dash].objects.get(date=date)
            else:
                art = calculate_sumexpense(date)
            data = {
                "iso": art.iso,
                "pol": art.pol,
                "pen": art.pen,
                "kat1": art.kat1,
                "kat2": art.kat2,
                "kat3": art.kat3
            }
        except UnboundLocalError:
            data = {"error":'not Role'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        return Response(data)





#виджет «Суммарный расход» для вкладки «месяц»
@permission_classes([IsAuthenticated])
class SumexpenseMonthViews(APIView):
    def get(self, request, date):
        role = UserP.objects.get(id=request.user.pk).role_set.all()
        for r in role:
            for d in r.dashboard.all():
                if d.name == 'SumexpenseDay':
                    dash = d.name
        sh = date.day
        dat = date
        delt = timedelta(days=1)
        iso = 0
        pol = 0
        pen = 0
        kat1 = 0
        kat2 = 0
        kat3 = 0
        try:
            while sh != 0:
                if globals()[dash].objects.filter(date=dat).exists():
                    art = globals()[dash].objects.get(date=dat)
                else:
                    art = calculate_sumexpense(dat)
                iso = iso + art.iso
                pol = pol + art.pol
                pen = pen + art.pen
                kat1 = kat1 + art.kat1
                kat2 = kat2 + art.kat2
                kat3 = kat3 + art.kat3
                dat = dat - delt
                sh = sh - 1
            data = {
                "iso": iso,
                "pol": pol,
                "pen": pen,
                "kat1": kat1,
                "kat2": kat2,
                "kat3": kat3
            }
        except UnboundLocalError:
            data = {"error":'not Role'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        return Response(data)




#виджет «Суммарный расход» для вкладки «смена»
@permission_classes([IsAuthenticated])
class SumexpenseShiftViews(APIView):
    def get(self, request, date, id):
        a = Agreagat.objects.get(pk=dist_table['id_agreagat']).parent.shift_set.all()[id-1]
        k = calculate_sumexpense_shift(date, a.start, a.end)
        return Response(k)





#виджет «Расход энергоресурсов» для вкладки «день»
@permission_classes([IsAuthenticated])
class EnergyConsumptionDayViews(APIView):
    def get(self, request, date):
        role = UserP.objects.get(id=request.user.pk).role_set.all()
        for r in role:
            for d in r.dashboard.all():
                if d.name == 'EnergyConsumptionDay':
                    dash = d.name
        try:
            if globals()[dash].objects.filter(date=date).exists():
                art = globals()[dash].objects.get(date=date)
            else:
                art = calculate_energy_consumption(date)
            data = {
                "input1": art.input1,
                "input2": art.input2,
                "gas": art.gas
            }
        except UnboundLocalError:
            data = {"error":'not Role'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        return Response(data)





#виджет «Расход энергоресурсов» для вкладки «месяц»
@permission_classes([IsAuthenticated])
class EnergyConsumptionMonthViews(APIView):
    def get(self, request, date):
        role = UserP.objects.get(id=request.user.pk).role_set.all()
        for r in role:
            for d in r.dashboard.all():
                if d.name == 'EnergyConsumptionDay':
                    dash = d.name
        try:
            sh = date.day
            dat = date
            delt = timedelta(days=1)
            input1 = 0
            input2 = 0
            gas = 0
            while sh != 0:
                if globals()[dash].objects.filter(date=dat).exists():
                    art = globals()[dash].objects.get(date=dat)
                else:
                    art = calculate_energy_consumption(dat)
                input1 = input1 + art.input1
                input2 = input2 + art.input2
                gas = gas + art.gas
                dat = dat -delt
                sh = sh -1
            data = {
                "input1": input1,
                "input2": input2,
                "gas": gas
            }
        except UnboundLocalError:
            data = {"error":'not Role'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        return Response(data)





#виджет «Расход энергоресурсов» для вкладки «смена»
@permission_classes([IsAuthenticated])
class EnergyConsumptionShiftViews(APIView):
    def get(self, request, date, id):
        a = Agreagat.objects.get(pk=dist_table['id_agreagat']).parent.shift_set.all()[id-1]
        k = calculate_energy_consumption_shift(date, a.start, a.end)
        return Response(k)




#виджет «Удельный расход на км» для вкладки «день»
@permission_classes([IsAuthenticated])
class SpecificConsumptionDayViews(APIView):
    def get(self, request, date):
        role = UserP.objects.get(id=request.user.pk).role_set.all()
        for r in role:
            for d in r.dashboard.all():
                if d.name == 'SpecificConsumptionDay':
                    dash = d.name
        try:
            if globals()[dash].objects.filter(date=date).exists():
                art = globals()[dash].objects.get(date=date)
            else:
                art = calculate_specific(date)
            data = {
                "iso": art.iso,
                "pol": art.pol,
                "pen": art.pen,
                "kat1": art.kat1,
                "kat2": art.kat2,
                "kat3": art.kat3
            }
        except UnboundLocalError:
            data = {"error":'not Role'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        return Response(data)


#виджет «Удельный расход на км» для вкладки «месяц»
@permission_classes([IsAuthenticated])
class SpecificConsumptionMonthViews(APIView):
    def get(self, request, date):
        role = UserP.objects.get(id=request.user.pk).role_set.all()
        for r in role:
            for d in r.dashboard.all():
                if d.name == 'SpecificConsumptionDay':
                    dash = d.name
        sh = date.day
        dat = date
        delt = timedelta(days=1)
        iso = 0
        pol = 0
        pen = 0
        kat1 = 0
        kat2 = 0
        kat3 = 0
        try:
            while sh != 0:
                if globals()[dash].objects.filter(date=dat).exists():
                    art = globals()[dash].objects.get(date=dat)
                else:
                    art = calculate_specific(dat)
                iso = iso + art.iso
                pol = pol + art.pol
                pen = pen + art.pen
                kat1 = kat1 + art.kat1
                kat2 = kat2 + art.kat2
                kat3 = kat3 + art.kat3
                dat = dat -delt
                sh = sh -1
            data = {
                "iso": iso,
                "pol": pol,
                "pen": pen,
                "kat1": kat1,
                "kat2": kat2,
                "kat3": kat3
            }
        except UnboundLocalError:
            data = {"error":'not Role'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        return Response(data)



#виджет «Удельный расход на км» для вкладки «смена»
@permission_classes([IsAuthenticated])
class SpecificConsumptionShiftViews(APIView):
    def get(self, request, date, id):
        a = Agreagat.objects.get(pk=dist_table['id_agreagat']).parent.shift_set.all()[id-1]
        k = calculate_specific_shift(date, a.start, a.end)
        return Response(k)


#виджет «Модуль сравнения» для вкладки «день»
@permission_classes([IsAuthenticated])
class ComparisonDayViews(APIView):
    def get(self, request, date1, date2):
        role = UserP.objects.get(id=request.user.pk).role_set.all()
        for r in role:
            for d in r.dashboard.all():
                if d.name == 'EditionDay':
                    dash = d.name
        try:
            if globals()[dash].objects.filter(date=date1).exists():
                art1 = globals()[dash].objects.get(date=date1)
            else:
                art1 = calculate_edition(date1)
                # art1 = globals()[dash].objects.get(date=date1)
            if globals()[dash].objects.filter(date=date2).exists():
                art2 = globals()[dash].objects.get(date=date2)
            else:
                art2 = calculate_edition(date2)
                # art2 = globals()[dash].objects.get(date=date2)
            if art2.suitable != 0:
                change_suitable = (((art1.suitable/art2.suitable)-1)*100)
            else:
                change_suitable = 0
            if art2.substandard != 0:
                change_substandard = (((art1.substandard/art2.substandard)-1)*100)
            else:
                change_substandard = 0
            if art2.defect != 0:
                change_defect = (((art1.defect/art2.defect)-1)*100)
            else:
                change_defect = 0
            if art2.flooded != 0:
                change_flooded = (((art1.flooded/art2.flooded)-1)*100)
            else:
                change_flooded = 0
            if art2.sum != 0:
                change_sum = (((art1.sum/art2.sum)-1)*100)
            else:
                change_sum = 0

            data = {
                "suitable1": art1.suitable,
                "sui1_ch": round(change_suitable),
                "suitable2": art2.suitable,
                "substandard1": art1.substandard,
                "sub1_ch": round(change_substandard),
                "substandard2": art2.substandard,
                "defect1": art1.defect,
                "def1_ch": round(change_defect),
                "defect2": art2.defect,
                "flooded1": art1.flooded,
                "flo_ch": round(change_flooded),
                "flooded2": art2.flooded,
                "sum1": art1.sum,
                "sum1_ch": round(change_sum),
                "sum2": art2.sum
            }
        except UnboundLocalError:
            data = {"error":'not Role'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        return Response(data)



#виджет «Модуль сравнения» для вкладки «месяц»
@permission_classes([IsAuthenticated])
class ComparisonMonthViews(APIView):
    def get(self, request, date1, date2):
        role = UserP.objects.get(id=request.user.pk).role_set.all()
        for r in role:
            for d in r.dashboard.all():
                if d.name == 'EditionDay':
                    dash = d.name
        try:
            sh1 = date1.day
            dat1 = date1
            sh2 = date2.day
            dat2 = date2
            delt = timedelta(days=1)
            suitable1 = 0
            suitable2 = 0
            substandard1 = 0
            substandard2 = 0
            defect1 = 0
            defect2 = 0
            flooded1 = 0
            flooded2 = 0
            sum1 = 0
            sum2 = 0
            while sh1 != 0:
                if globals()[dash].objects.filter(date=dat1).exists():
                    art = globals()[dash].objects.get(date=dat1)
                else:
                    art = calculate_edition(dat1)
                suitable1 = suitable1 + art.suitable
                substandard1 = substandard1 + art.substandard
                defect1 = defect1 + art.defect
                flooded1 = flooded1 + art.flooded
                sum1 = sum1 + art.sum
                dat1 = dat1 -delt
                sh1 = sh1 -1
            while sh2 != 0:
                if globals()[dash].objects.filter(date=dat2).exists():
                    art = globals()[dash].objects.get(date=dat2)
                else:
                    art = calculate_edition(dat2)
                suitable2 = suitable2 + art.suitable
                substandard2 = substandard2 + art.substandard
                defect2 = defect2 + art.defect
                flooded2 = flooded2 + art.flooded
                sum2 = sum2 + art.sum
                dat2 = dat2 -delt
                sh2 = sh2 -1
                if suitable2 != 0:
                    sui1_ch = ((suitable1/suitable2)-1)*100
                else:
                    sui1_ch = 0
                if substandard2 != 0:
                    sub1_ch = ((substandard1/substandard2)-1)*100
                else:
                    sub1_ch = 0
                if defect2 != 0:
                    def1_ch = ((defect1 / defect2) - 1) * 100
                else:
                    def1_ch = 0
                if flooded2 != 0:
                    flo_ch = ((flooded1 / flooded2) - 1) * 100
                else:
                    flo_ch = 0
                if sum2 != 0:
                    sum1_ch = ((sum1 / sum2) - 1) * 100
                else:
                    sum1_ch = 0
            data = {
                "suitable1": suitable1,
                "sui1_ch": round(sui1_ch),
                "suitable2": suitable2,
                "substandard1": substandard1,
                "sub1_ch": round(sub1_ch),
                "substandard2": substandard2,
                "defect1": defect1,
                "def1_ch": round(def1_ch),
                "defect2": defect2,
                "flooded1": flooded1,
                "flo_ch": round(flo_ch),
                "flooded2": flooded2,
                "sum1": sum1,
                "sum1_ch": round(sum1_ch),
                "sum2": sum2
            }
        except UnboundLocalError:
            data = {"error":'not Role'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        return Response(data)


#виджет «Модуль сравнения» для вкладки «смена»
@permission_classes([IsAuthenticated])
class ComparisonShiftViews(APIView):
    def get(self, request, date1, date2, id1, id2):
        a1 = Agreagat.objects.get(pk=dist_table['id_agreagat']).parent.shift_set.all()[id1-1]
        a2 = Agreagat.objects.get(pk=dist_table['id_agreagat']).parent.shift_set.all()[id2-1]
        k1 = calculate_edition_shift(date1, a1.start, a1.end)
        k2 = calculate_edition_shift(date2, a2.start, a2.end)
        if k2['suitable'] != 0:
            sui1_ch = ((k1['suitable'] / k2['suitable']) - 1) * 100
        else:
            sui1_ch = 0
        if k2['substandard'] != 0:
            sub1_ch = ((k1['substandard'] / k2['substandard']) - 1) * 100
        else:
            sub1_ch = 0
        if k2['defect'] != 0:
            def1_ch = ((k1['defect'] / k2['defect']) - 1) * 100
        else:
            def1_ch = 0
        if k2['flooded'] != 0:
            flo_ch = ((k1['flooded'] / k2['flooded']) - 1) * 100
        else:
            flo_ch = 0
        if k2['sum'] != 0:
            sum1_ch = ((k1['sum'] / k2['sum']) - 1) * 100
        else:
            sum1_ch = 0
        data = {
            "suitable1": k1['suitable'],
            "sui1_ch": round(sui1_ch),
            "suitable2": k2['suitable'],
            "substandard1": k1['substandard'],
            "sub1_ch": round(sub1_ch),
            "substandard2": k2['substandard'],
            "defect1": k1['defect'],
            "def1_ch": round(def1_ch),
            "defect2": k2['defect'],
            "flooded1": k1['flooded'],
            "flo_ch": round(flo_ch),
            "flooded2": k2['flooded'],
            "sum1": k1['sum'],
            "sum1_ch": round(sum1_ch),
            "sum2": k2['sum']
        }
        return Response(data)
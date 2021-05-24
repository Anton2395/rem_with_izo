from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
import datetime
from dashboard.models import StatePressureRange
from project_v_0_0_1.settings import dist_table


class GetStatusConnectionsRemeza(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            sql = """SELECT * FROM connections"""
            cursor.execute(sql)
            connections = cursor.fetchall()
            data = {}
            for i in connections:
                data[f'{i[1]}'] = [i[8], i[1], i[2]]
        return Response(data)


class GetConnectionsRemeza(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            sql = """SELECT * FROM connections"""
            cursor.execute(sql)
            connections = cursor.fetchall()
            data = []
            for index, val in enumerate(connections):
                k = {
                    "connection_name": val[1],
                    "ip": val[2],
                    "key": val[0]
                }
                data.append(k)
            return Response(data)



class GetConnectionsVariablesRemeza(APIView):
    def get(self, request, id):
        data = []
        with connection.cursor() as cursor:
            sql = f"""SELECT name FROM listvalue WHERE connections_id={id}"""
            cursor.execute(sql)
            names = cursor.fetchall()
            for i in names:
                k = {
                    "name": i[0]
                }
                data.append(k)
        return Response(data)





class State_color(APIView):
    def get(self, request):
        data = StatePressureRange.objects.all()
        rang = []
        for i in data:
            rang.append(i.get_struc())
        data = {
            "state": rang
        }
        return Response(data)


class StateTempPres(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            sql1 = '''SELECT value, now_time FROM '''
            table_name = dist_table['Remeza']['status']
            sql2 = ''' ORDER BY now_time DESC LIMIT 1'''
            sql = sql1 + table_name + sql2
            cursor.execute(sql)
            status = cursor.fetchone()
            if status[0] == 1:
                st = "Выключен"
            elif status[0] == 2:
                st = "Инициализация"
            elif status[0] == 3:
                st = "Запрет запуска"
            elif status[0] == 4:
                st = "Готов к запуску"
            elif status[0] == 5:
                st = "Продувка"
            elif status[0] == 6:
                st = "Ожидание"
            elif status[0] == 7:
                st = "Запуск двигателя"
            elif status[0] == 8:
                st = "Запуск двигателя"
            elif status[0] == 9 or status[0] == 10:
                st = "Работа"
            elif status[0] == 12:
                st = "Остановлен"
            elif status[0] == 13:
                st = "Работа"
            elif status[0] == 14:
                st = "Тестирование главного двигателя"
            elif status[0] == 11:
                st = "Работа под нагрузкой"
            else:
                st = "Неизвестный статус"
            sql1 = '''SELECT value, now_time FROM '''
            table_name = dist_table['Remeza']['temp']
            sql2 = ''' ORDER BY now_time DESC LIMIT 1'''
            sql = sql1 + table_name + sql2
            cursor.execute(sql)
            temp = cursor.fetchone()
            te = temp[0]
            sql1 = '''SELECT value, now_time FROM '''
            table_name = dist_table['Remeza']['davlenie']
            sql2 = ''' ORDER BY now_time DESC LIMIT 1'''
            sql = sql1 + table_name + sql2
            cursor.execute(sql)
            davlenie = cursor.fetchone()
            data = {
                "current_pressure": davlenie[0],
                "current_temp": te,
                "current_state": st
            }
        return Response(data)




class duration(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            sql1 = '''SELECT value, now_time FROM '''
            table_name = dist_table['Remeza']['status']
            now = datetime.datetime.now()
            now_start_day = datetime.datetime(now.year, now.month, now.day)
            sql2 = f''' WHERE now_time>='{now_start_day}' ORDER BY now_time ASC'''
            sql = sql1 + table_name + sql2
            cursor.execute(sql)
            status = cursor.fetchall()
            rab = 0
            time = {}
            duration = []
            max = 0
            for i in status:
                if i[0] == 9:
                   rab += 1
                   if rab == 1:
                       time['start_time'] = i[1] + datetime.timedelta(hours=3)
                elif (i[0] != 9) and (i[0] != 11) and (i[0] != 10) and ('start_time' in time):
                    time['end_time'] = i[1] + datetime.timedelta(hours=3)
                    rab = 0
                if (status[-1][0] == 9 or status[-1][0] == 11 or status[-1][0] == 10) and (status[-1][1] == i[1]):
                    time['end_time'] = i[1] + datetime.timedelta(hours=3)
                if 'start_time' in time and 'end_time' in time:
                    hor = (time['end_time'] - time['start_time']).total_seconds() / 3600
                    min = int((hor % 1) * 60)/100
                    time ['work_time'] = int(hor) + min
                    if max < time['work_time']:
                        max = time['work_time']
                    duration.append(time)
                    time = {}
            for i in duration:
                i['progress'] = (i['work_time']/max)*100
            return Response(duration)


class statusError(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            sql1 = '''SELECT value, now_time FROM '''
            table_name = dist_table['Remeza']['error']
            sql2 = ''' ORDER BY now_time DESC LIMIT 1'''
            sql = sql1 + table_name + sql2
            cursor.execute(sql)
            error_status = cursor.fetchone()
            k = {
                "error": error_status[0]
            }
        return Response(k)



class davlenie_graf(APIView):
    def get(self, format=None):
        result = {}
        keys = self.request.query_params.get('key', None)
        start = self.request.query_params.get('start', None)
        end = self.request.query_params.get('end', None)
        data = self.__choice_method(keys=keys, start=start, end=end)
        # data['state'] = []
        # diapoz = StatePressureRange.objects.all()
        # for i in diapoz:
        #     down = i.from_data
        #     up = i.to_data
        #     k = {
        #         'name_state': i.name,
        #         'color': i.color,
        #         'data': []
        #     }
        #     length = len(data['data'])
        #     diap = {
        #         "y": 0
        #     }
        #     for index, point in enumerate(data['data']):
        #         if point['y'] == None:
        #             continue
        #         if point['y']>=down and point['y']<up:
        #             if not 'x1' in diap:
        #                 diap['x1'] = point['x']
        #             if index != length-1:
        #                 if data['data'][index+1]['y'] == None:
        #                     continue
        #                 if not ((data['data'][index + 1]['y'] >= down) and  (data['data'][index + 1]['y'] < up)):
        #                     diap['x2'] = point['x']
        #                 else:
        #                     continue
        #                 if ('x1' in diap) and ('x2' in diap):
        #                     k['data'].append(diap)
        #                     diap = {
        #                         "y": 0
        #                     }
        #             else:
        #                 diap['x2'] = point['x']
        #                 if ('x1' in diap) and ('x2' in diap):
        #                     k['data'].append(diap)
        #                     diap = {
        #                         "y": 0
        #                     }
        #     data['state'].append(k)
        return Response(data)

    def __choice_method(self, keys=None, start=None, end=None):
        """метод для выбора вывода данных за период по фильтру"""
        res = {}
        if keys != None:
            if (keys == "hour"):
                res['data'] = self.get_last_hour()
                res['state'] = self.get_color_stat_hour()
            elif (keys == "day"):
                st1 = datetime.datetime.now()
                res['data'] = self.get_last_day()
                end1 = datetime.datetime.now()
                print('tochki: ', (end1 - st1).total_seconds() / 60, 'min')
                res['state'] = self.get_color_stat_day()
                end2 = datetime.datetime.now()
                print('interval: ', (end2 - end1).total_seconds() / 60, 'min')
            elif (keys == "week"):
                res['data'] = self.get_last_week()
                res['state'] = self.get_color_stat_week()
            elif (keys == "month"):
                res['data'] = self.get_last_month()
                res['state'] = self.get_color_stat_month()
        else:
            if start is not None and end is not None:
                res['data'] = self.get_period(start=start, end=end)
                res['state'] = self.get_color_stat_period(start=start, end=end)
            else:
                res['data'] = self.get_last_hour()
                res['state'] = self.get_color_stat_hour()
        return res


    def get_last_day(self):
        """метод возвращает данные за последний день"""
        now = datetime.datetime.now()
        end = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, 0)
        start = now - datetime.timedelta(days=1)
        return self._time_conversion(start=start, end=end)


    def get_color_stat_day(self):
        """метод возвращает цвета статуса за последний день"""
        now = datetime.datetime.now()
        end = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, 0)
        start = now - datetime.timedelta(days=1)
        return self._time_conversion_color(start=start, end=end)


    def get_last_week(self):
        """метод возвращает данные за последнию неделю"""
        now = datetime.datetime.now()
        end = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, 0)
        start = now - datetime.timedelta(days=7)
        return self._time_conversion(start=start, end=end)


    def get_color_stat_week(self):
        """метод возвращает цвета статуса за последнюю неделю"""
        now = datetime.datetime.now()
        end = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, 0)
        start = now - datetime.timedelta(days=7)
        return self._time_conversion_color(start=start, end=end)


    def get_last_month(self):
        """метод возвращает данные за последний месяц"""
        now = datetime.datetime.now()
        end = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, 0)
        start = now - datetime.timedelta(days=30)
        return self._time_conversion(start=start, end=end)


    def get_color_stat_month(self):
        """метод возвращает цвета статуса за последний месяц"""
        now = datetime.datetime.now()
        end = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, 0)
        start = now - datetime.timedelta(days=30)
        return self._time_conversion_color(start=start, end=end)


    def get_last_hour(self):
        now = datetime.datetime.now()
        end = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, 0)
        start = end - datetime.timedelta(hours=1)
        return self._time_conversion(start=start, end=end)


    def get_color_stat_hour(self):
        """метод возвращает цвета статуса за последний час"""
        now = datetime.datetime.now()
        end = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, 0)
        start = end - datetime.timedelta(hours=1)
        return self._time_conversion_color(start=start, end=end)


    def _time_conversion_color(self, start, end):
        """
        преобразование времени к формату
        :param datetime start: начало периода
        :param datetime end: конец периода

        """
        f = '%Y-%m-%d %H:%M:%S'
        start = start.strftime(f)
        end = end.strftime(f)
        return self.get_color_stat_period(start=start, end=end)


    def _time_conversion(self, start, end):
        """
        преобразование времени к формату
        :param datetime start: начало периода
        :param datetime end: конец периода

        """
        f = '%Y-%m-%d %H:%M:%S'
        start = start.strftime(f)
        end = end.strftime(f)
        return self.get_period(start=start, end=end)


    def get_color_stat_period(self, start, end):
        f = '%Y-%m-%d %H:%M:%S'
        curs = connection.cursor()
        # stringer = f"""SELECT now_time, value FROM {str(dist_table['Remeza']['status'])} where now_time >= '{str(datetime.datetime.fromisoformat(start)-datetime.timedelta(hours=3))}' and now_time <
        # '{str(datetime.datetime.fromisoformat(end)-datetime.timedelta(hours=3))}' ORDER BY now_time ASC"""
        # stringer = f"""SELECT now_time, value, LEAD(now_time) OVER(ORDER BY now_time) next_time FROM
        # {str(dist_table['Remeza']['status'])} WHERE now_time >= '{str(datetime.datetime.fromisoformat(start)-datetime.timedelta(hours=3))}' and now_time <
        # '{str(datetime.datetime.fromisoformat(end)-datetime.timedelta(hours=3))}' ORDER BY now_time ASC"""
        list = {}
        a = 0
        for i in range(1, 15):
            stringer = f"""WITH t as (SELECT now_time, value, LEAD(now_time) OVER(ORDER BY now_time) next_time FROM 
            {str(dist_table['Remeza']['status'])} WHERE now_time >= '{str(datetime.datetime.fromisoformat(start)-datetime.timedelta(hours=3))}' and now_time < 
            '{str(datetime.datetime.fromisoformat(end)-datetime.timedelta(hours=3))}')
            SELECT now_time, next_time FROM t WHERE value = {i} ORDER BY now_time ASC"""
            curs.execute(stringer)
            query = curs.fetchall()
            if len(query) == 0:
                a += 1
            list[f'{i}'] = query
        if a == 14:
            stringer = f"""SELECT now_time, value FROM {str(dist_table['Remeza']['status'])} where now_time < 
            '{str(datetime.datetime.fromisoformat(start)-datetime.timedelta(hours=3))}' ORDER BY now_time DESC LIMIT 1"""
            curs.execute(stringer)
            query = curs.fetchone()
            list[f'{query[1]}'] = [(query[0], datetime.datetime.now())]
        return self.convert_data_color(list=list)


    def convert_data_color(self, list):
        res = []
        for i in range(1, 15):
            state = {}
            if i == 1:
                state['name_state'] = "Выключен"
                state['color'] = "#5A5A5A"
            elif i == 2:
                state['name_state'] = "Инициализация"
                state['color'] = "#FF986B"
            elif i == 3:
                state['name_state'] = "Запрет запуска"
                state['color'] = "#F86E6E"
            elif i == 4:
                state['name_state'] = "Готов к запуску"
                state['color'] = "#4BBEAA"
            elif i == 5:
                state['name_state'] = "Продувка"
                state['color'] = "#9FAED8"
            elif i == 6:
                state['name_state'] = "Ожидание"
                state['color'] = "#FF986B"
            elif i == 7:
                state['name_state'] = "Запуск двигателя"
                state['color'] = "#2D9AD8"
            elif i == 8:
                state['name_state'] = "Запуск двигателя"
                state['color'] = "#2D9AD8"
            elif i == 9:
                state['name_state'] = "Работа"
                state['color'] = "#588C64"
            elif i == 10:
                state['name_state'] = "Работа"
                state['color'] = "#588C64"
            elif i == 12:
                state['name_state'] = "Остановлен"
                state['color'] = "#7A6F6D"
            elif i == 13:
                state['name_state'] = "Работа"
                state['color'] = "#588C64"
            elif i == 14:
                state['name_state'] = "Тестирование главного двигателя"
                state['color'] = "#EEB82D"
            elif i == 11:
                state['name_state'] = "Работа под нагрузкой"
                state['color'] = "#3d5943"
            if f'{i}' in list:
                state['data'] = []
                for j in list[f'{i}']:
                    appp = {
                        'x': j[0],
                        'x2': j[1],
                        'y': 0
                    }
                    if j[1] == None:
                        appp['x2'] = datetime.datetime.now()
                    state['data'].append(appp)
            res.append(state)
        return res


    def get_period(self, start, end):
        """метод возвращает данные за период start - end

        :param datetime start: начало периода
        :param datetime end: конец периода
        :return: list
        """
        f = '%Y-%m-%d %H:%M:%S'
        if (((datetime.datetime.strptime(end,f) - datetime.datetime.strptime(start,f))) < datetime.timedelta(hours=6)):
            curs = connection.cursor()
            curs.execute(
                f"""SELECT (now_time +('180 minute'::interval))::timestamp as now_time, value FROM {str(dist_table['Remeza']['davlenie'])} WHERE now_time >= '{
                str(datetime.datetime.fromisoformat(start)-datetime.timedelta(hours=3))}' AND now_time<'{datetime.datetime.fromisoformat(end)-datetime.timedelta(hours=3)}' ORDER BY now_time desc;""")
            query = curs.fetchall()
            fieldnames = ['x', 'y']
            result = []
            for row in query:
                rowset = []
                for field in zip(fieldnames, row):
                    rowset.append(field)
                result.append(dict(rowset))
            return result
        else:
            a = self._generate_period_min(start, end)
            # return self._get_mode_by_periods(var=a['var'], periods=a['periods'])
            return self.get_mode_by_periods_interval(start=start, end=end, interval=a['var'])


    def _generate_period_min(self, start, end):
        """
        пересчитывает время в интервалы для метода моды и среднего исходя из заданного количество точек points

        :param real start: начало периода
        :param real end: конец периода
        :return: dict {'var':real,'periods':real}
        """
        f = '%Y-%m-%d %H:%M:%S'
        points = 200  # количество точек
        minutes = (datetime.datetime.strptime(end,f)- datetime.datetime.strptime(start,f)).total_seconds() / 60
        interval = minutes / points
        return {'var': interval, 'periods': minutes}


    def get_mode_by_periods_interval(self, start, end, interval=20):
        curs = connection.cursor()
        sql = "with period_t as (SELECT n as ti from generate_series('" + str(start) + "'::timestamp,'" + str(
                end) + "'::timestamp,'" + str(interval) + " minute'::interval) n)" \
            "SELECT ti as now_time, COALESCE((SELECT mode() WITHIN GROUP (ORDER BY value) as modevar" \
            " FROM " + dist_table['Remeza']['davlenie'] + \
            " r WHERE  (r.now_time +('180 minute'::interval))::timestamp>=ti and (r.now_time +('180 minute'::interval))::timestamp<(ti+('"+str(interval)+ \
            " minutes'::interval))),NULL) as value from " \
              + dist_table['Remeza']['davlenie'] + " b right join " \
            "period_t a ON (b.now_time +('180 minute'::interval))::timestamp>=ti AND (b.now_time +('180 minute'::interval))::timestamp<(ti+('"+str(interval)+" minutes'::interval)) GROUP BY ti" \
            " ORDER BY ti desc"
        try:
            curs.execute(sql)
        except Exception as a:
            return a.__str__()
        query = curs.fetchall()
        fieldnames = ['x', 'y']
        result = []
        for row in query:
            rowset = []
            for field in zip(fieldnames, row):
                rowset.append(field)
            result.append(dict(rowset))
        if(result[0]['y']==None):
            result[0]['y'] = 0
        return result

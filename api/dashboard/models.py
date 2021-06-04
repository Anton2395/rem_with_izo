from django.db import models
from users.models import *
from django.db import connection
import datetime
from structure.models import Agreagat
from project_v_0_0_1.settings import dist_table
from rest_framework.exceptions import ValidationError





class Dashboard(models.Model):
    '''
    Сущность для определения виджетов

      Attributes
    ===========
    - name - str - название для записи

     Methods
    =============
    - None
    '''
    name = models.CharField(max_length=255, default='no name')

    def __str__(self):
        return self.name




class Role(models.Model):
    '''
        Сущность для определения роли пользователя

          Attributes
        ===========
        - name - str - название для записи
        - user - MtM - связь с сущностью UserP
        - dashboard - MtM - связь с сущностью Dashboard

         Methods
        =============
        - None
    '''
    name = models.CharField(max_length=255, default='no name')
    user = models.ManyToManyField(UserP)
    dashboard = models.ManyToManyField(Dashboard)


def calculate_duration_shift(date, start, end):
    with connection.cursor() as cursor:
        sql1 = '''SELECT value, now_time FROM '''
        sql2 = ''' WHERE now_time>=%s and now_time<%s ORDER BY now_time'''
        sql = sql1 + dist_table['DurationIntervalDay'][0] + sql2
        date_start = datetime.datetime(date.year, date.month, date.day, start.hour, start.minute, start.second)
        date_end = datetime.datetime(date.year, date.month, date.day, end.hour, end.minute, end.second)
        cursor.execute(sql, [date_start, date_end])
        a = cursor.fetchall()
        k = 0
        for i in a:
            if i[0] == 1 and k == 0:
                k += 1
                date_start1 = datetime.time(i[1].hour, i[1].minute, i[1].second)
            if i[0] == 0 and k == 1:
                k = 0
                date_end1 = datetime.time(i[1].hour, i[1].minute, i[1].second)
                obj = DurationIntervalDay(start=date_start1, end=date_end1, date=date)
                obj.save()
        return 0


# для виджета продолжительность работы
class DurationIntervalDay(models.Model):
    '''
        Сущность для определения начало и времени работы

          Attributes
        ===========
        - start - Time - начало работы
        - end - Time - конец работы
        - date - Date - дата работы

         Methods
        =============
        - None
    '''
    start = models.TimeField('start work')
    end = models.TimeField('end work')
    date = models.DateField(auto_now=False, auto_now_add=False)

    def __exists_table(self, text):
        with connection.cursor() as cursor:
            engine = connection.vendor
            if engine == 'sqlite':
                sql = '''SELECT count(*) FROM sqlite_master WHERE type="table" AND name="'''
            elif engine == 'postgresql':
                sql = '''SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_name ="'''
            sql = sql + text + '"'
            cursor.execute(sql)
            a = cursor.fetchall()[0][0]
        return a

    # def save(self):
    #     a = self.__exists_table(dist_table['DurationIntervalDay'][0])
    #     if a:
    #         super(DurationIntervalDay, self).save()
    #     else:
    #         raise ValidationError('did not find the agreagat table')

# def calculate_duration_day()





class Storehouse(models.Model):
    '''
    Сущность для названия склада

          Attributes
        ===========
        - name - str - название склада

         Methods
        =============
        - None
    '''
    name = models.CharField(max_length=255, default='no name')


    def __str__(self):
        return self.name


class Substance(models.Model):
    '''
    Сущность для названия хранящегося вещества

          Attributes
        ===========
        - name - str - название вещества
        - short_name - str - короткая название вещества
        - parent - FK - внешний ключь с Storehouse

         Methods
        =============
        - calculate - Забись данных в таблицу Django остатка по дате
        - value_date - Возвращает велечину остатка на складе
    '''
    name = models.CharField(max_length=255, default='no name')
    short_name = models.CharField(max_length=255, default='no name')
    table_name = models.CharField(max_length=255, default='no name')
    parent = models.ForeignKey(Storehouse, on_delete=models.CASCADE)

    def __str__(self):
        data = self.name + '(' + self.parent.name + ')'
        return data

    def calculate(self, date):
        '''
        Запись данных в таблицу Django остатка по дате

        :param date date: дата за которую извлекаются данные
        '''
        with connection.cursor() as cursor:
            sql1 = '''SELECT value, now_time FROM '''
            sql2 = ''' WHERE now_time>=%s and now_time<%s ORDER BY now_time DESC LIMIT 1'''
            sql = sql1 + self.table_name + sql2
            date_now = date + datetime.timedelta(days=1)
            cursor.execute(sql, [date, date_now])
            a = cursor.fetchone()
            if a == None:
                a = [0]
            k = DateValue(date=date, value=a[0], parent=self)
            if date != datetime.datetime.now().date():
                k.save()
        return a


    def value_date(self, date):
        '''
        Возвращает велечину остатка на складе

        :param date date: дата за которую извлекаются данные
        '''
        if date == datetime.datetime.now().date():
            try:
                k = self.calculate(date)[0]
            except TypeError:
                k = 0
        else:
            if self.datevalue_set.filter(date=date).exists():
                k = self.datevalue_set.get(date=date).value
            else:
                self.calculate(date)
                k = self.datevalue_set.get(date=date).value
        return k



class DateValue(models.Model):
    '''
    Сущность для количество вещества по времени

          Attributes
        ===========
        - date - date - дата
        - value - float - количество вещества
        - parent - FK - внешний ключь с Substance

         Methods
        =============
        - None
    '''
    date = models.DateField(auto_now=False, auto_now_add=False)
    value = models.FloatField()
    parent = models.ForeignKey(Substance, on_delete=models.CASCADE)

    def __str__(self):
        data = str(self.date) + ':  ' + self.parent.name + '-' + str(self.value)
        return data


def calculate_edition(date):
    '''
    извлекание и запись данных для виджета Выпуск панелей

    :param date date: дата за которую извлекаются данные

    '''
    with connection.cursor() as cursor:
        sql = f"""
        SELECT COALESCE(sum(len), 0)  FROM
            (SELECT i.now_time, i."value", (
                SELECT a.value
                FROM {dist_table["EditionDay1"]["len"]} a
                WHERE a.now_time<=i.now_time
                ORDER BY a.now_time DESC LIMIT 1
                ) as len , ( 
                    SELECT t.value
                    FROM {dist_table["EditionDay1"]["type"]} as t
                    WHERE i.now_time>=t.now_time
                    ORDER BY t.now_time DESC LIMIT 1
                ) as type
        from {dist_table["EditionDay1"]["impuls"]} i
        where i.value=1 and date_trunc('day', i.now_time) = '{date}') t
        WHERE t.type=
        """

        sql_br = f"""
        SELECT COALESCE(sum(len), 0)
        FROM (
        SELECT t.now_time , t."value", (
            SELECT l."value"
            FROM {dist_table['EditionDay1']['len']} l
            WHERE t.now_time=l.now_time) as len
        FROM mvlab_izospan_edition_type_cut t
        WHERE date_trunc('day', now_time)='{date}' and t."value"=1
        ORDER BY now_time DESC) k
        """
        sql_nek = f"""
        SELECT COALESCE(sum(len), 0)
        FROM (
        SELECT t.now_time , t."value", (
            SELECT l."value"
            FROM {dist_table['EditionDay1']['len']} l
            WHERE t.now_time=l.now_time) as len
        FROM mvlab_izospan_edition_type_cut t
        WHERE date_trunc('day', now_time)='{date}' and t."value"=2
        ORDER BY now_time DESC) k
                """
        cursor.execute(sql_br)
        brak1 = cursor.fetchone()


        cursor.execute(sql_nek)
        ne_kond1 = cursor.fetchone()


        cursor.execute(sql + "0")
        godno1 = cursor.fetchone()

        sql_zalito = f"""
        SELECT value 
        from {dist_table['EditionDay1']['flooded']}
        WHERE date_trunc('day', now_time)='{date}'
        ORDER BY now_time
        """
        cursor.execute(sql_zalito)
        zalito_array = cursor.fetchall()
        zalito1 = 0
        flag = 0
        leng = len(zalito_array)
        for i,d in enumerate(zalito_array):
            if d[0]!=0:
                flag = 0
            if flag==0 and d[0]==0 and i!=0:
                zalito1 = zalito1 + zalito_array[i-1][0]
                flag = 1
            if flag==0 and i==(leng-1):
                zalito1 = zalito1 + d[0]
        zalito1 = [zalito1]

        if brak1 == None:
            brak1 = [0]
        if ne_kond1 == None:
            ne_kond1 = [0]
        if godno1 == None:
            godno1 = [0]
        k = EditionDay(date=date, suitable=godno1[0]/1000, substandard=ne_kond1[0]/1000, defect=brak1[0]/1000, flooded=zalito1[0], sum=(brak1[0]+ne_kond1[0]+godno1[0])/1000)
        if datetime.datetime.now().date() != date:
            k.save()
    return k


def calculate_edition_shift(date, start, end):
    sql = '''SELECT value, now_time, status FROM ''' + dist_table['EditionDay'] + ''' WHERE now_time>=%s and now_time<%s and status=%s ORDER BY now_time DESC LIMIT 1'''
    with connection.cursor() as cursor:
        date_start = datetime.datetime(date.year, date.month, date.day, start.hour, start.minute, start.second)
        date_end = datetime.datetime(date.year, date.month, date.day, end.hour, end.minute, end.second)
        cursor.execute(sql, [date_start, date_end, 0])
        brak = cursor.fetchone()
        if brak == None:
            brak = [0]
        cursor.execute(sql, [date_start, date_end, 1])
        godno = cursor.fetchone()
        if godno == None:
            godno = [0]
        cursor.execute(sql, [date_start, date_end, 2])
        ne_kond = cursor.fetchone()
        if ne_kond == None:
            ne_kond = [0]
        cursor.execute(sql, [date_start, date_end, 3])
        zalito = cursor.fetchone()
        if zalito == None:
            zalito = [0]
        a = {
            "suitable": godno[0],
            "substandard": ne_kond[0],
            "defect": brak[0],
            "flooded": zalito[0],
            "sum": brak[0]+ne_kond[0]+godno[0]
        }
    return a

# для виджета Выпуск панелей
class EditionDay(models.Model):
    '''
        Сущность для определения выпуска

          Attributes
        ===========
        - suitable - float - количество годного
        - substandard - float - количество некондиции
        - defect - float - количество брака
        - flooded - float - количество залитого
        - sum - float - сумма годного, некондиции, брака
        - date - Date - дата

         Methods
        =============
        - None

    '''
    suitable = models.FloatField()
    substandard = models.FloatField()
    defect = models.FloatField()
    flooded = models.FloatField()
    sum = models.FloatField()
    date = models.DateField(auto_now=False, auto_now_add=False, unique=True)

    def __str__(self):
        return str(self.date)


def calculate_sumexpense(date):
    """
    извлекание и запись данных для виджета Суммарный расход

    :param date date: дата за которую извлекаются данные

    """
    iso = 0
    pen = 0
    pol = 0
    kat1 = 0
    kat2 = 0
    kat3 = 0
    for i in dist_table['SumexpenseDay']['iso']:
        with connection.cursor() as cursor:
            sql_new = f"""
                    SELECT value 
                    from {i}
                    WHERE date_trunc('day', now_time)='{date}'
                    ORDER BY now_time
                """
            cursor.execute(sql_new)
            iso_array = cursor.fetchall()
            iso_temp = 0
            flag = 0
            leng = len(iso_array)
            for i, d in enumerate(iso_array):
                if d[0] != 0:
                    flag = 0
                if flag == 0 and d[0] == 0 and i != 0:
                    iso_temp = iso_temp + iso_array[i - 1][0]
                    flag = 1
                if flag == 0 and i == (leng - 1):
                    iso_temp = iso_temp + d[0]
            iso = iso + iso_temp
    for i in dist_table['SumexpenseDay']['pol']:
        with connection.cursor() as cursor:
            sql_new = f"""
                    SELECT value 
                    from {i}
                    WHERE date_trunc('day', now_time)='{date}'
                    ORDER BY now_time
                            """
            cursor.execute(sql_new)
            pol_array = cursor.fetchall()
            pol_temp = 0
            flag = 0
            leng = len(pol_array)
            for i, d in enumerate(pol_array):
                if d[0] != 0:
                    flag = 0
                if flag == 0 and d[0] == 0 and i != 0:
                    pol_temp = pol_temp + pol_array[i - 1][0]
                    flag = 1
                if flag == 0 and i == (leng - 1):
                    pol_temp = pol_temp + d[0]
            pol = pol + pol_temp
    for i in dist_table['SumexpenseDay']['pen']:
        with connection.cursor() as cursor:
            sql_new = f"""
                    SELECT value 
                    from {i}
                    WHERE date_trunc('day', now_time)='{date}'
                    ORDER BY now_time
                                        """
            cursor.execute(sql_new)
            pen_array = cursor.fetchall()
            pen_temp = 0
            flag = 0
            leng = len(pen_array)
            for i, d in enumerate(pen_array):
                if d[0] != 0:
                    flag = 0
                if flag == 0 and d[0] == 0 and i != 0:
                    pen_temp = pen_temp + pen_array[i - 1][0]
                    flag = 1
                if flag == 0 and i == (leng - 1):
                    pen_temp = pen_temp + d[0]
            pen = pen + pen_temp
    for i in dist_table['SumexpenseDay']['kat1']:
        with connection.cursor() as cursor:
            sql_new = f"""
                    SELECT value 
                    from {i}
                    WHERE date_trunc('day', now_time)='{date}'
                    ORDER BY now_time
                                        """
            cursor.execute(sql_new)
            kat1_array = cursor.fetchall()
            kat1_temp = 0
            flag = 0
            leng = len(kat1_array)
            for i, d in enumerate(kat1_array):
                if d[0] != 0:
                    flag = 0
                if flag == 0 and d[0] == 0 and i != 0:
                    kat1_temp = kat1_temp + kat1_array[i - 1][0]
                    flag = 1
                if flag == 0 and i == (leng - 1):
                    kat1_temp = kat1_temp + d[0]
            kat1 = kat1 + kat1_temp
    for i in dist_table['SumexpenseDay']['kat2']:
        with connection.cursor() as cursor:
            sql_new = f"""
                    SELECT value 
                    from {i}
                    WHERE date_trunc('day', now_time)='{date}'
                    ORDER BY now_time
                                        """
            cursor.execute(sql_new)
            kat2_array = cursor.fetchall()
            kat2_temp = 0
            flag = 0
            leng = len(kat2_array)
            for i, d in enumerate(kat2_array):
                if d[0] != 0:
                    flag = 0
                if flag == 0 and d[0] == 0 and i != 0:
                    kat2_temp = kat2_temp + kat2_array[i - 1][0]
                    flag = 1
                if flag == 0 and i == (leng - 1):
                    kat2_temp = kat2_temp + d[0]
            kat2 = kat2 + kat2_temp
    for i in dist_table['SumexpenseDay']['kat3']:
        with connection.cursor() as cursor:
            sql_new = f"""
                    SELECT value 
                    from {i}
                    WHERE date_trunc('day', now_time)='{date}'
                    ORDER BY now_time
                                        """
            cursor.execute(sql_new)
            kat3_array = cursor.fetchall()
            kat3_temp = 0
            flag = 0
            leng = len(kat3_array)
            for i, d in enumerate(kat3_array):
                if d[0] != 0:
                    flag = 0
                if flag == 0 and d[0] == 0 and i != 0:
                    kat3_temp = kat3_temp + kat3_array[i - 1][0]
                    flag = 1
                if flag == 0 and i == (leng - 1):
                    kat3_temp = kat3_temp + d[0]
            kat3 = kat3 + kat3_temp
    data = SumexpenseDay(date=date, iso=iso, pol=pol, pen=pen, kat1=kat1, kat2=kat2, kat3=kat3)
    if datetime.datetime.now().date() != date:
        data.save()
    return data

def calculate_sumexpense_shift(date, start, end):
    date_start = datetime.datetime(date.year, date.month, date.day, start.hour, start.minute, start.second)
    date_end = datetime.datetime(date.year, date.month, date.day, end.hour, end.minute, end.second)
    sql1 = '''SELECT value, now_time FROM '''
    sql2 = ''' WHERE now_time>=%s and now_time<%s ORDER BY now_time DESC LIMIT 1'''
    iso = 0
    pol = 0
    pen = 0
    kat1 = 0
    kat2 = 0
    kat3 = 0
    with connection.cursor() as cursor:
        for i in dist_table['SumexpenseDay']['iso']:
            sql = sql1 + i + sql2
            cursor.execute(sql, [date_start, date_end])
            data = cursor.fetchone()
            if data == None:
                data = [0]
            iso += data[0]
        for i in dist_table['SumexpenseDay']['pol']:
            sql = sql1 + i + sql2
            cursor.execute(sql, [date_start, date_end])
            data = cursor.fetchone()
            if data == None:
                data = [0]
            pol += data[0]
        for i in dist_table['SumexpenseDay']['pen']:
            sql = sql1 + i + sql2
            cursor.execute(sql, [date_start, date_end])
            data = cursor.fetchone()
            if data == None:
                data = [0]
            pen += data[0]
        for i in dist_table['SumexpenseDay']['kat1']:
            sql = sql1 + i + sql2
            cursor.execute(sql, [date_start, date_end])
            data = cursor.fetchone()
            if data == None:
                data = [0]
            kat1 += data[0]
        for i in dist_table['SumexpenseDay']['kat2']:
            sql = sql1 + i + sql2
            cursor.execute(sql, [date_start, date_end])
            data = cursor.fetchone()
            if data == None:
                data = [0]
            kat2 += data[0]
        for i in dist_table['SumexpenseDay']['kat3']:
            sql = sql1 + i + sql2
            cursor.execute(sql, [date_start, date_end])
            data = cursor.fetchone()
            if data == None:
                data = [0]
            kat3 += data[0]
    a = {
        "iso": iso,
        "pol": pol,
        "pen": pen,
        "kat1": kat1,
        "kat2": kat2,
        "kat3": kat3
    }
    return a





# для виджета Суммарный расход
class SumexpenseDay(models.Model):
    '''
        Сущность для определения сумарного расхода

          Attributes
        ===========
        - iso - float - количество расхода изоцианата
        - pol - float - количество расхода полиола
        - pen - float - количество расхода пентана
        - kat1 - float - количество расхода катализатора 1
        - kat2 - float - количество расхода катализатора 2
        - kat3 - float - количество расхода катализатора 3
        - date - Date - дата

         Methods
        =============
        - None
    '''
    iso = models.FloatField()
    pol = models.FloatField()
    pen = models.FloatField()
    kat1 = models.FloatField()
    kat2 = models.FloatField()
    kat3 = models.FloatField()
    date = models.DateField(auto_now=False, auto_now_add=False, unique=True)


def calculate_energy_consumption(date):
    """

    извлекание и запись данных для виджета сумарного расхода энергоресурсов

    :param date date: дата за которую извлекаются данные

    """
    with connection.cursor() as cursor:
        sql1 = '''SELECT value, now_time FROM '''
        sql21 = ''' WHERE now_time>=%s and now_time<%s ORDER BY now_time DESC LIMIT 1'''
        sql22 = ''' WHERE now_time>=%s and now_time<%s ORDER BY now_time ASC LIMIT 1'''
        sql = sql1 + dist_table['EnergyConsumptionDay']['input1'] + sql21
        date_now = date + datetime.timedelta(days=1)
        cursor.execute(sql, [date, date_now])
        data1 = cursor.fetchone()
        if data1 == None:
            data1 = [0]
        sql = sql1 + dist_table['EnergyConsumptionDay']['input1'] + sql22
        cursor.execute(sql, [date, date_now])
        data2 = cursor.fetchone()
        if data2 == None:
            data2 = [0]
        data_in_1 = data1[0]-data2[0]
        sql = sql1 + dist_table['EnergyConsumptionDay']['input2'] + sql21
        date_now = date + datetime.timedelta(days=1)
        cursor.execute(sql, [date, date_now])
        data1 = cursor.fetchone()
        if data1 == None:
            data1 = [0]
        sql = sql1 + dist_table['EnergyConsumptionDay']['input2'] + sql22
        cursor.execute(sql, [date, date_now])
        data2 = cursor.fetchone()
        if data2 == None:
            data2 = [0]
        data_in_2 = data1[0]-data2[0]
        sql = sql1 + dist_table['EnergyConsumptionDay']['gas'] + sql21
        date_now = date + datetime.timedelta(days=1)
        cursor.execute(sql, [date, date_now])
        data1 = cursor.fetchone()
        if data1 == None:
            data1 = [0]
        sql = sql1 + dist_table['EnergyConsumptionDay']['gas'] + sql22
        cursor.execute(sql, [date, date_now])
        data2 = cursor.fetchone()
        if data2 == None:
            data2 = [0]
        data_gas = data1[0] - data2[0]

        k = EnergyConsumptionDay(input1=data_in_1, input2=data_in_2, gas=data_gas, date=date)
        if datetime.datetime.now().date() != date:
            k.save()
        return k


def calculate_energy_consumption_shift(date, start, end):
    date_start = datetime.datetime(date.year, date.month, date.day, start.hour, start.minute, start.second)
    date_end = datetime.datetime(date.year, date.month, date.day, end.hour, end.minute, end.second)
    sql1 = '''SELECT value, now_time FROM '''
    sql21 = ''' WHERE now_time>=%s and now_time<%s ORDER BY now_time DESC LIMIT 1'''
    sql22 = ''' WHERE now_time>=%s and now_time<%s ORDER BY now_time ASC LIMIT 1'''
    with connection.cursor() as cursor:
        sql = sql1 + dist_table['EnergyConsumptionDay']['input1'] + sql21
        cursor.execute(sql, [date_start, date_end])
        data_end = cursor.fetchone()
        if data_end == None:
            data_end = [0]
        sql = sql1 + dist_table['EnergyConsumptionDay']['input1'] + sql22
        cursor.execute(sql, [date_start,date_end])
        data_start = cursor.fetchone()
        if data_start == None:
            data_start = [0]
        data_in1 = data_end[0] - data_start[0]
        sql = sql1 + dist_table['EnergyConsumptionDay']['input2'] + sql21
        cursor.execute(sql, [date_start, date_end])
        data_end = cursor.fetchone()
        if data_end == None:
            data_end = [0]
        sql = sql1 + dist_table['EnergyConsumptionDay']['input2'] + sql22
        cursor.execute(sql, [date_start, date_end])
        data_start = cursor.fetchone()
        if data_start == None:
            data_start = [0]
        data_in2 = data_end[0] - data_start[0]
        sql = sql1 + dist_table['EnergyConsumptionDay']['gas'] + sql21
        cursor.execute(sql, [date_start, date_end])
        data_end = cursor.fetchone()
        if data_end == None:
            data_end = [0]
        sql = sql1 + dist_table['EnergyConsumptionDay']['gas'] + sql22
        cursor.execute(sql, [date_start, date_end])
        data_start = cursor.fetchone()
        if data_start == None:
            data_start = [0]
        data_gas = data_end[0] - data_start[0]
        data = {
            "input1": data_in1,
            "input2": data_in2,
            "gas": data_gas
        }
    return data









# для виджета Расход энергоресурсов
class EnergyConsumptionDay(models.Model):
    '''
        Сущность для определения сумарного расхода энергоресурсов

          Attributes
        ===========
        - input1 - float - расход эл.энергии ввода 1
        - input2 - float - расход эл.энергии ввода 2
        - gas - float - расход газа
        - date - Date - дата

         Methods
        =============
        - None

    '''
    input1 = models.FloatField()
    input2 = models.FloatField()
    gas = models.FloatField()
    date = models.DateField(auto_now=False, auto_now_add=False, unique=True)

    def __str__(self):
        return 'i1:'+str(self.input1)+' i2:'+str(self.input2)+' g:'+str(self.gas)


def calculate_specific(date):
    """
    извлекание и запись данных для виджета удельный расход на км

    :param date date: дата за которую извлекаются данные

    """
    iso = 0
    pen = 0
    pol = 0
    kat1 = 0
    kat2 = 0
    kat3 = 0
    ################
    sql_zalito = f"""
            SELECT value 
            from {dist_table['EditionDay1']['flooded']}
            WHERE date_trunc('day', now_time)='{date}'
            ORDER BY now_time
            """
    cursor.execute(sql_zalito)
    zalito_array = cursor.fetchall()
    zalito1 = 0
    flag = 0
    leng = len(zalito_array)
    for i, d in enumerate(zalito_array):
        if d[0] != 0:
            flag = 0
        if flag == 0 and d[0] == 0 and i != 0:
            zalito1 = zalito1 + zalito_array[i - 1][0]
            flag = 1
        if flag == 0 and i == (leng - 1):
            zalito1 = zalito1 + d[0]
    ################
    for i in dist_table['SumexpenseDay']['iso']:
        with connection.cursor() as cursor:
            sql_new = f"""
                    SELECT value 
                    from {i}
                    WHERE date_trunc('day', now_time)='{date}'
                    ORDER BY now_time
                """
            cursor.execute(sql_new)
            iso_array = cursor.fetchall()
            iso_temp = 0
            flag = 0
            leng = len(iso_array)
            for i, d in enumerate(iso_array):
                if d[0] != 0:
                    flag = 0
                if flag == 0 and d[0] == 0 and i != 0:
                    iso_temp = iso_temp + iso_array[i - 1][0]
                    flag = 1
                if flag == 0 and i == (leng - 1):
                    iso_temp = iso_temp + d[0]
            iso = iso + iso_temp
    for i in dist_table['SumexpenseDay']['pol']:
        with connection.cursor() as cursor:
            sql_new = f"""
                    SELECT value 
                    from {i}
                    WHERE date_trunc('day', now_time)='{date}'
                    ORDER BY now_time
                            """
            cursor.execute(sql_new)
            pol_array = cursor.fetchall()
            pol_temp = 0
            flag = 0
            leng = len(pol_array)
            for i, d in enumerate(pol_array):
                if d[0] != 0:
                    flag = 0
                if flag == 0 and d[0] == 0 and i != 0:
                    pol_temp = pol_temp + pol_array[i - 1][0]
                    flag = 1
                if flag == 0 and i == (leng - 1):
                    pol_temp = pol_temp + d[0]
            pol = pol + pol_temp
    for i in dist_table['SumexpenseDay']['pen']:
        with connection.cursor() as cursor:
            sql_new = f"""
                    SELECT value 
                    from {i}
                    WHERE date_trunc('day', now_time)='{date}'
                    ORDER BY now_time
                                        """
            cursor.execute(sql_new)
            pen_array = cursor.fetchall()
            pen_temp = 0
            flag = 0
            leng = len(pen_array)
            for i, d in enumerate(pen_array):
                if d[0] != 0:
                    flag = 0
                if flag == 0 and d[0] == 0 and i != 0:
                    pen_temp = pen_temp + pen_array[i - 1][0]
                    flag = 1
                if flag == 0 and i == (leng - 1):
                    pen_temp = pen_temp + d[0]
            pen = pen + pen_temp
    for i in dist_table['SumexpenseDay']['kat1']:
        with connection.cursor() as cursor:
            sql_new = f"""
                    SELECT value 
                    from {i}
                    WHERE date_trunc('day', now_time)='{date}'
                    ORDER BY now_time
                                        """
            cursor.execute(sql_new)
            kat1_array = cursor.fetchall()
            kat1_temp = 0
            flag = 0
            leng = len(kat1_array)
            for i, d in enumerate(kat1_array):
                if d[0] != 0:
                    flag = 0
                if flag == 0 and d[0] == 0 and i != 0:
                    kat1_temp = kat1_temp + kat1_array[i - 1][0]
                    flag = 1
                if flag == 0 and i == (leng - 1):
                    kat1_temp = kat1_temp + d[0]
            kat1 = kat1 + kat1_temp
    for i in dist_table['SumexpenseDay']['kat2']:
        with connection.cursor() as cursor:
            sql_new = f"""
                    SELECT value 
                    from {i}
                    WHERE date_trunc('day', now_time)='{date}'
                    ORDER BY now_time
                                        """
            cursor.execute(sql_new)
            kat2_array = cursor.fetchall()
            kat2_temp = 0
            flag = 0
            leng = len(kat2_array)
            for i, d in enumerate(kat2_array):
                if d[0] != 0:
                    flag = 0
                if flag == 0 and d[0] == 0 and i != 0:
                    kat2_temp = kat2_temp + kat2_array[i - 1][0]
                    flag = 1
                if flag == 0 and i == (leng - 1):
                    kat2_temp = kat2_temp + d[0]
            kat2 = kat2 + kat2_temp
    for i in dist_table['SumexpenseDay']['kat3']:
        with connection.cursor() as cursor:
            sql_new = f"""
                    SELECT value 
                    from {i}
                    WHERE date_trunc('day', now_time)='{date}'
                    ORDER BY now_time
                                        """
            cursor.execute(sql_new)
            kat3_array = cursor.fetchall()
            kat3_temp = 0
            flag = 0
            leng = len(kat3_array)
            for i, d in enumerate(kat3_array):
                if d[0] != 0:
                    flag = 0
                if flag == 0 and d[0] == 0 and i != 0:
                    kat3_temp = kat3_temp + kat3_array[i - 1][0]
                    flag = 1
                if flag == 0 and i == (leng - 1):
                    kat3_temp = kat3_temp + d[0]
            kat3 = kat3 + kat3_temp
    if zalito1!=0:
        iso = iso/zalito1
        pol = pol/zalito1
        pen = pen/zalito1
        kat1 = kat1/zalito1
        kat2 = kat2/zalito1
        kat3 = kat3/zalito1
    else:
        iso = 0
        pol = 0
        pen = 0
        kat1 = 0
        kat2 = 0
        kat3 = 0
    data = SpecificConsumptionDay(date=date, iso=iso, pol=pol, pen=pen, kat1=kat1, kat2=kat2, kat3=kat3)
    if datetime.datetime.now().date() != date:
        data.save()
    return data



def calculate_specific_shift(date, start, end):
    date_start = datetime.datetime(date.year, date.month, date.day, start.hour, start.minute, start.second)
    date_end = datetime.datetime(date.year, date.month, date.day, end.hour, end.minute, end.second)
    sql1 = '''SELECT value, now_time FROM '''
    sql2 = ''' WHERE now_time>=%s and now_time<%s ORDER BY now_time DESC LIMIT 1'''
    iso = 0
    pol = 0
    pen = 0
    kat1 = 0
    kat2 = 0
    kat3 = 0
    with connection.cursor() as cursor:
        for i in dist_table['SpecificConsumptionDay']['iso']:
            sql = sql1 + i + sql2
            cursor.execute(sql, [date_start, date_end])
            data = cursor.fetchone()
            if data == None:
                data = [0]
            iso += data[0]
        for i in dist_table['SpecificConsumptionDay']['pol']:
            sql = sql1 + i + sql2
            cursor.execute(sql, [date_start, date_end])
            data = cursor.fetchone()
            if data == None:
                data = [0]
            pol += data[0]
        for i in dist_table['SpecificConsumptionDay']['pen']:
            sql = sql1 + i + sql2
            cursor.execute(sql, [date_start, date_end])
            data = cursor.fetchone()
            if data == None:
                data = [0]
            pen += data[0]
        for i in dist_table['SpecificConsumptionDay']['kat1']:
            sql = sql1 + i + sql2
            cursor.execute(sql, [date_start, date_end])
            data = cursor.fetchone()
            if data == None:
                data = [0]
            kat1 += data[0]
        for i in dist_table['SpecificConsumptionDay']['kat2']:
            sql = sql1 + i + sql2
            cursor.execute(sql, [date_start, date_end])
            data = cursor.fetchone()
            if data == None:
                data = [0]
            kat2 += data[0]
        for i in dist_table['SpecificConsumptionDay']['kat3']:
            sql = sql1 + i + sql2
            cursor.execute(sql, [date_start, date_end])
            data = cursor.fetchone()
            if data == None:
                data = [0]
            kat3 += data[0]
    a = {
        "iso": iso,
        "pol": pol,
        "pen": pen,
        "kat1": kat1,
        "kat2": kat2,
        "kat3": kat3
    }
    return a




# для виджета Удельный расход на км
class SpecificConsumptionDay(models.Model):
    '''
        Сущность для определения удельного расхода

          Attributes
        ===========
        - iso - float - количество удельного расхода изоцианата
        - pol - float - количество удельного расхода полиола
        - pen - float - количество удельного расхода пентана
        - kat1 - float - количество удельного расхода катализатора 1
        - kat2 - float - количество удельного расхода катализатора 2
        - kat3 - float - количество удельного расхода катализатора 3
        - date - Date - дата

         Methods
        =============
        - None
    '''
    iso = models.FloatField()
    pol = models.FloatField()
    pen = models.FloatField()
    kat1 = models.FloatField()
    kat2 = models.FloatField()
    kat3 = models.FloatField()
    date = models.DateField(auto_now=False, auto_now_add=False, unique=True)



class StatePressureRange(models.Model):
    '''
    Сущность для хранение границ и названия давления данного диапазона

      Attributes
    ===========
    - name - str - имя диапазона давления
    - from_data - int - начала диапазона давления
    - to_data - int - конец диапазона давления
    - color - str - цвет отображения данного диапазона


     Methods
    =============
    - get_struc - вазвращает все параметры запеси в dict


    '''
    name = models.CharField(max_length=255, default='no name')
    from_data = models.IntegerField()
    to_data = models.IntegerField()
    color = models.CharField(max_length=255, default='#ffffff')


    def get_struc(self) -> dict:
        k = {
                "name": self.name,
                "from": self.from_data,
                "to": self.to_data,
                "color": self.color
            }
        return k


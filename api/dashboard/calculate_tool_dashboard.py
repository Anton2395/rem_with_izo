from django.db import connection
import datetime
from project_v_0_0_1.settings import dist_table
from .models import EditionDay, SumexpenseDay, SpecificConsumptionDay, DurationIntervalDay

def calculate_duration_shift(date, start, end):
    with connection.cursor() as cursor:
        art = []
        for i in dist_table['DurationIntervalDay']:
            date_start = datetime.datetime(date.year, date.month, date.day, start.hour, start.minute, start.second)
            date_end = datetime.datetime(date.year, date.month, date.day, end.hour, end.minute, end.second)
            sql = f'''select now_time, value from {i} 
                        WHERE now_time>='{date_start}' and now_time<'{date_end}'
                        order by now_time
                        '''
            cursor.execute(sql)
            a = cursor.fetchall()
            k = 0
            for i in a:
                if i[1] == 1 and k == 0:
                    k += 1
                    date_start1 = datetime.time(i[0].hour, i[0].minute, i[0].second)
                if i[1] == 0 and k == 1:
                    k = 0
                    date_end1 = datetime.time(i[0].hour, i[0].minute, i[0].second)
                    obj = DurationIntervalDay(start=date_start1, end=date_end1, date=date)
                    art.append(obj)
                    if date != datetime.datetime.now().date():
                        obj.save()
    return art

def calculate_edition(date):
    '''
    извлекание и запись данных для виджета Выпуск панелей

    :param date date: дата за которую извлекаются данные

    '''
    with connection.cursor() as cursor:
        # запрос в базу который возвращает сумму длин реза от всех импульсов за день
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

        #запрос в базу который возвращает ыумму длин реза браковон типа
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

        #запрос в базу который возвращает сумму длин реза типа некондиция
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

        #запрос в базу который возвращает все записи "метров запенено" за сутки отсортированные по возрастанию времени
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
        #перебор записей для суммы последних дли
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
    date_start = datetime.datetime(date.year, date.month, date.day, start.hour, start.minute, start.second)
    date_end = datetime.datetime(date.year, date.month, date.day, end.hour, end.minute, end.second)
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
            where i.value=1 and now_time>='{date_start}' and now_time<'{date_end}') t
            WHERE t.type=0
            """
    sql_br = f"""
            SELECT COALESCE(sum(len), 0)
            FROM (
            SELECT t.now_time , t."value", (
                SELECT l."value"
                FROM {dist_table['EditionDay1']['len']} l
                WHERE t.now_time=l.now_time) as len
            FROM mvlab_izospan_edition_type_cut t
            WHERE now_time>='{date_start}' and now_time<'{date_end}' and t."value"=1
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
            WHERE now_time>='{date_start}' and now_time<'{date_end}' and t."value"=2
            ORDER BY now_time DESC) k
                    """
    sql_zalito = f"""
            SELECT value 
            from {dist_table['EditionDay1']['flooded']}
            WHERE now_time>='{date_start}' and now_time<'{date_end}'
            ORDER BY now_time
            """
    with connection.cursor() as cursor:
        cursor.execute(sql)
        godno1 = cursor.fetchone()

        cursor.execute(sql_nek)
        ne_kond1 = cursor.fetchone()

        cursor.execute(sql_br)
        brak1 = cursor.fetchone()

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
        zalito1 = [zalito1]
        a = {
            "suitable": godno1[0]/1000,
            "substandard": ne_kond1[0]/1000,
            "defect": brak1[0]/1000,
            "flooded": zalito1[0],
            "sum": (brak1[0]+ne_kond1[0]+godno1[0])/1000
        }
    return a



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
    for j in dist_table['SumexpenseDay']['iso']:
        with connection.cursor() as cursor:
            sql_new = f"""
                    SELECT value 
                    from {j}
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
    for j in dist_table['SumexpenseDay']['pol']:
        with connection.cursor() as cursor:
            sql_new = f"""
                    SELECT value 
                    from {j}
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
    for j in dist_table['SumexpenseDay']['pen']:
        with connection.cursor() as cursor:
            sql_new = f"""
                    SELECT value 
                    from {j}
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
    for j in dist_table['SumexpenseDay']['kat1']:
        with connection.cursor() as cursor:
            sql_new = f"""
                    SELECT value 
                    from {j}
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
    for j in dist_table['SumexpenseDay']['kat2']:
        with connection.cursor() as cursor:
            sql_new = f"""
                    SELECT value 
                    from {j}
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
    for j in dist_table['SumexpenseDay']['kat3']:
        with connection.cursor() as cursor:
            sql_new = f"""
                    SELECT value 
                    from {j}
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
    iso = 0
    pol = 0
    pen = 0
    kat1 = 0
    kat2 = 0
    kat3 = 0
    with connection.cursor() as cursor:
        for j in dist_table['SumexpenseDay']['iso']:
            sql_new = f"""
                    SELECT value 
                    from {j}
                    WHERE now_time >= '{date_start}' and now_time < '{date_end}'
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
            sql_new = sql_new + ''' limit 1'''
            cursor.execute(sql_new)
            iso_first = cursor.fetchone()
            iso = iso - iso_first[0]
        for j in dist_table['SumexpenseDay']['pol']:
            sql_new = f"""
                    SELECT value 
                    from {j}
                    WHERE now_time >= '{date_start}' and now_time < '{date_end}'
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
            sql_new = sql_new + ''' limit 1'''
            cursor.execute(sql_new)
            pol_first = cursor.fetchone()
            pol = pol - pol_first[0]
        for j in dist_table['SumexpenseDay']['pen']:
            sql_new = f"""
                    SELECT value 
                    from {j}
                    WHERE now_time >= '{date_start}' and now_time < '{date_end}'
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
            sql_new = sql_new + ''' limit 1'''
            cursor.execute(sql_new)
            pen_first = cursor.fetchone()
            pen = pen - pen_first[0]
        for j in dist_table['SumexpenseDay']['kat1']:
            sql_new = f"""
                    SELECT value 
                    from {j}
                    WHERE now_time >= '{date_start}' and now_time < '{date_end}'
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
            sql_new = sql_new + ''' limit 1'''
            cursor.execute(sql_new)
            kat1_first = cursor.fetchone()
            kat1 = kat1 - kat1_first[0]
        for j in dist_table['SumexpenseDay']['kat2']:
            sql_new = f"""
                    SELECT value 
                    from {j}
                    WHERE now_time >= '{date_start}' and now_time < '{date_end}'
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
            sql_new = sql_new + ''' limit 1'''
            cursor.execute(sql_new)
            kat2_first = cursor.fetchone()
            kat2 = kat2 - kat2_first[0]
        for j in dist_table['SumexpenseDay']['kat3']:
            sql_new = f"""
                    SELECT value 
                    from {j}
                    WHERE now_time >= '{date_start}' and now_time < '{date_end}'
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
            sql_new = sql_new + ''' limit 1'''
            cursor.execute(sql_new)
            kat3_first = cursor.fetchone()
            kat3 = kat3 - kat3_first[0]
    a = {
        "iso": iso,
        "pol": pol,
        "pen": pen,
        "kat1": kat1,
        "kat2": kat2,
        "kat3": kat3
    }
    return a

def calculate_specific(date):
    """
    извлекание и запись данных для виджета удельный расход на км

    :param date date: дата за которую извлекаются данные

    """
    date_del = date - datetime.timedelta(days=1)
    iso = 0
    pen = 0
    pol = 0
    kat1 = 0
    kat2 = 0
    kat3 = 0
    ################
    with connection.cursor() as cursor:
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
        sql_zalito = f''' 
                SELECT value 
                from {dist_table['EditionDay1']['flooded']}
                WHERE date_trunc('day', now_time)='{date_del}'
                ORDER BY now_time DESC limit 1'''
        cursor.execute(sql_zalito)
        zalito1_first = cursor.fetchone()
        zalito1 = zalito1 - zalito1_first[0]
    ################
    for j in dist_table['SumexpenseDay']['iso']:
        with connection.cursor() as cursor:
            sql_new = f"""
                    SELECT value 
                    from {j}
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
            sql_new = f''' 
                SELECT value 
                from {j}
                WHERE date_trunc('day', now_time)='{date_del}'
                ORDER BY now_time DESC limit 1'''
            cursor.execute(sql_new)
            iso_first = cursor.fetchone()
            iso = iso - iso_first[0]
    for j in dist_table['SumexpenseDay']['pol']:
        with connection.cursor() as cursor:
            sql_new = f"""
                    SELECT value 
                    from {j}
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
            sql_new = f''' 
                            SELECT value 
                            from {j}
                            WHERE date_trunc('day', now_time)='{date_del}'
                            ORDER BY now_time DESC limit 1'''
            cursor.execute(sql_new)
            pol_first = cursor.fetchone()
            pol = pol - pol_first[0]
    for j in dist_table['SumexpenseDay']['pen']:
        with connection.cursor() as cursor:
            sql_new = f"""
                    SELECT value 
                    from {j}
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
            sql_new = f''' 
                            SELECT value 
                            from {j}
                            WHERE date_trunc('day', now_time)='{date_del}'
                            ORDER BY now_time DESC limit 1'''
            cursor.execute(sql_new)
            pen_first = cursor.fetchone()
            pen = pen - pen_first[0]
    for j in dist_table['SumexpenseDay']['kat1']:
        with connection.cursor() as cursor:
            sql_new = f"""
                    SELECT value 
                    from {j}
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
            sql_new = f''' 
                            SELECT value 
                            from {j}
                            WHERE date_trunc('day', now_time)='{date_del}'
                            ORDER BY now_time DESC limit 1'''
            cursor.execute(sql_new)
            kat1_first = cursor.fetchone()
            kat1 = kat1 - kat1_first[0]
    for j in dist_table['SumexpenseDay']['kat2']:
        with connection.cursor() as cursor:
            sql_new = f"""
                    SELECT value 
                    from {j}
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
            sql_new = f''' 
                            SELECT value 
                            from {j}
                            WHERE date_trunc('day', now_time)='{date_del}'
                            ORDER BY now_time DESC limit 1'''
            cursor.execute(sql_new)
            kat2_first = cursor.fetchone()
            kat2 = kat2 - kat2_first[0]
    for j in dist_table['SumexpenseDay']['kat3']:
        with connection.cursor() as cursor:
            sql_new = f"""
                    SELECT value 
                    from {j}
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
            sql_new = f''' 
                            SELECT value 
                            from {j}
                            WHERE date_trunc('day', now_time)='{date_del}'
                            ORDER BY now_time DESC limit 1'''
            cursor.execute(sql_new)
            kat3_first = cursor.fetchone()
            kat3 = kat3 - kat3_first[0]
    if zalito1!=0:
        iso = float('{:.3f}'.format(iso/zalito1))
        pol = float('{:.3f}'.format(pol / zalito1))
        pen = float('{:.3f}'.format(pen / zalito1))
        kat1 = float('{:.3f}'.format(kat1 / zalito1))
        kat2 = float('{:.3f}'.format(kat2 / zalito1))
        kat3 = float('{:.3f}'.format(kat3 / zalito1))
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
    date_del = date_start - datetime.timedelta(hours=1)
    iso = 0
    pen = 0
    pol = 0
    kat1 = 0
    kat2 = 0
    kat3 = 0
    with connection.cursor() as cursor:
        sql_zalito = f"""
                SELECT value, now_time
                from {dist_table['EditionDay1']['flooded']}
                WHERE now_time>='{date_start}' and now_time<'{date_end}'
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
        sql_zalito = sql_zalito + """ limit 1"""
        cursor.execute(sql_zalito)
        first_zalito = cursor.fetchone()
        zalito1 = zalito1 - first_zalito[0]
        for t in zalito_array:
            print(t[1], "||", t[0])
    ################
    for j in dist_table['SumexpenseDay']['iso']:
        with connection.cursor() as cursor:
            sql_new = f"""
                    SELECT value 
                    from {j}
                    WHERE now_time>='{date_start}' and now_time<'{date_end}'
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
            sql_new = sql_new + """ limit 1"""
            cursor.execute(sql_new)
            first_iso = cursor.fetchone()
            iso = iso - first_iso[0]
    for j in dist_table['SumexpenseDay']['pol']:
        with connection.cursor() as cursor:
            sql_new = f"""
                    SELECT value 
                    from {j}
                    WHERE now_time>='{date_start}' and now_time<'{date_end}'
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
            sql_new = sql_new + """ limit 1"""
            cursor.execute(sql_new)
            first_pol = cursor.fetchone()
            pol = pol - first_pol[0]
    for j in dist_table['SumexpenseDay']['pen']:
        with connection.cursor() as cursor:
            sql_new = f"""
                    SELECT value 
                    from {j}
                    WHERE now_time>='{date_start}' and now_time<'{date_end}'
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
            sql_new = sql_new + """ limit 1"""
            cursor.execute(sql_new)
            first_pen = cursor.fetchone()
            pen = pen - first_pen[0]
    for j in dist_table['SumexpenseDay']['kat1']:
        with connection.cursor() as cursor:
            sql_new = f"""
                    SELECT value 
                    from {j}
                    WHERE now_time>='{date_start}' and now_time<'{date_end}'
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
            sql_new = sql_new + """ limit 1"""
            cursor.execute(sql_new)
            first_kat1 = cursor.fetchone()
            kat1 = kat1 - first_kat1[0]
    for j in dist_table['SumexpenseDay']['kat2']:
        with connection.cursor() as cursor:
            sql_new = f"""
                    SELECT value 
                    from {j}
                    WHERE now_time>='{date_start}' and now_time<'{date_end}'
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
            sql_new = sql_new + """ limit 1"""
            cursor.execute(sql_new)
            first_kat2 = cursor.fetchone()
            kat2 = kat2 - first_kat2[0]
    for j in dist_table['SumexpenseDay']['kat3']:
        with connection.cursor() as cursor:
            sql_new = f"""
                    SELECT value 
                    from {j}
                    WHERE now_time>='{date_start}' and now_time<'{date_end}'
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
            sql_new = sql_new + """ limit 1"""
            cursor.execute(sql_new)
            first_kat3 = cursor.fetchone()
            kat3 = kat3 - first_kat3[0]
    if zalito1 != 0:
        iso = float('{:.3f}'.format(iso / zalito1))
        pol = float('{:.3f}'.format(pol / zalito1))
        pen = float('{:.3f}'.format(pen / zalito1))
        kat1 = float('{:.3f}'.format(kat1 / zalito1))
        kat2 = float('{:.3f}'.format(kat2 / zalito1))
        kat3 = float('{:.3f}'.format(kat3 / zalito1))
    else:
        iso = 0
        pol = 0
        pen = 0
        kat1 = 0
        kat2 = 0
        kat3 = 0
    a = {
        "iso": iso,
        "pol": pol,
        "pen": pen,
        "kat1": kat1,
        "kat2": kat2,
        "kat3": kat3
    }
    return a

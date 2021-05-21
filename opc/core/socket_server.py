import json
import math
import socket
import threading
import time

from cprint import cprint

from opc.core.teldafax_dashboard_data import PlcRemoteUse
from opc.data import list_connections, statuses_connection, PLC_init, result_query
from opc.settings import SOCKET_PORT


def start_socket():
    cprint.err('run socket ')
    get_dat_from_plc_thread = threading.Thread(target=get_data_from_plc)
    get_dat_from_plc_thread.start()



def get_data_from_plc():
    while True:
        time.sleep(2)
        try:
            data = PlcRemoteUse(PLC_init["address"], PLC_init["rack"], PLC_init["slot"], PLC_init["port"])
            data1 = data.get_dashboard_teldafax_value_power()
            data2 = data.get_status_machine()
            data = {"data1": data1, "data2": data2}
            globals()['result_query'] = data
            # return data
        except:
            globals()['result_query'] = [{"error": 0}]
            # return json.dumps({"error": "no connection"}).encode('utf-8')

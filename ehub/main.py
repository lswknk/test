# -*- coding:utf-8 -*-
from core.classes import *
from draw import *
from config import *
from draw_stable import *

timer = Timer()
# source, user and devices
source, user, devices = {}, {}, {}
source['s1'] = Source('s1')
user['u1'] = User('u1')
devices['gsb01'] = GasSteamBoiler('gsb01')
devices['gsb02'] = GasSteamBoiler('gsb02')
devices['gsb03'] = GasSteamBoiler('gsb03')
devices['chp01'] = CHP('chp01')
devices['chp02'] = CHP('chp02')
devices['pv01'] = Photovoltaic('pv01')
# devices['wg01'] = WindGenerator('wg01')
devices['stg01'] = Storage('stg01')



flag1 = int(get_config_values('flag','flag_pv'))
flag2 = int(get_config_values('flag','flag_stg'))
flag3 = int(get_config_values('flag','flag_price'))
flag_good = int(get_config_values('flag','flag_good'))
# topology
topology = {('s1', 'gas', ('gsb01', 'gsb02', 'gsb03', 'chp01', 'chp02')),
            ('s1', 'water', ('gsb01', 'gsb02', 'gsb03', 'chp01', 'chp02')),
            ('s1', 'elec', ('u1',)),
            ('u1', 'elec', ('s1',)),
            ('gsb01', 'steam', ('u1',)),
            ('gsb02', 'steam', ('u1',)),
            ('gsb03', 'steam', ('u1',)),
            ('chp01', 'steam', ('u1',)),
            ('chp01', 'elec', ('u1','stg01')),
            ('chp02', 'steam', ('u1',)),
            ('chp02', 'elec', ('u1','stg01')),
            ('pv01', 'elec', ('stg01', 'u1')),
            ('stg01', 'elec', ('u1',))
            }

# future loads corresponding to users (here we have one user)
# tem_ = np.array([2000, 1300, 3200, 3600, 3500, 2800, 2000, 1300, 3200, 3600, 3500, 2800, 2000, 1300, 3200, 3600, \
#                  3500, 2800, 2000, 1300, 3200, 3600, 3500, 2800]) * 3.0

tem_good = np.array(
    [5773, 8625, 8105, 8165, 7414, 6884, 6240, 5910, 8426, 6641, 6114, 5349, 6040, 5979, 6490, 7239, 9740, 9222, 8786,
     9702, 6091, 9470, 9607, 7122])

tem_bad = np.array(
    [2914, 2946, 2914, 2978, 3173, 3011, 3237, 5180, 5827, 5924, 6475, 8093, 7446, 7122, 6151, 7737, 11007, 12885,
     13597, 15863, 14244, 9065, 6475, 4856])

if 0 == flag_good :
    loads = {'steamLoads': {'u1': [13.16, 13.69, 13.49, 11.51, 13.34, 13.43, 12.77, 13.78, 14.12, 12.55, 12.36, 12.28, \
                               13.08, 12.41, 13.27, 14.89, 14.90, 14.63, 14.99, 14.37, 14.69, 14.87, 12.54, 10.89]}, \
         'elecLoads': {'u1': list(tem_bad)}}
elif 1 == flag_good:
    loads = {'steamLoads': {'u1': [13.16, 13.69, 13.49, 11.51, 13.34, 13.43, 12.77, 13.78, 14.12, 12.55, 12.36, 12.28, \
                                   13.08, 12.41, 13.27, 14.89, 14.90, 14.63, 14.99, 14.37, 14.69, 14.87, 12.54, 10.89]}, \
             'elecLoads': {'u1': list(tem_good)}}

# device on-off map
onOffMap = {'gsb01': 0, 'gsb02': 1, 'gsb03': 1, 'pv01': 1, 'chp01': 1, 'chp02': 1, 'stg01': 1}

# photovoltaic
devices['pv01'].maxOutputPower = [3500 for i in range(24)]  # 逆变器最大功率或预测功率值
tem = np.array([0, 0, 0, 0, 143.547, 695.859, 1038.65, 1718.30, 2216.88, 2661.77, 3748.71, 4154.78, 3719.69,
                3118.82, 2172.23, 1098.60, 312.203, 25.67, 0, 0, 0, 0, 0, 0])*flag1
devices['pv01'].maxOutputPower = list(tem)
devices['pv01'].maxCap = 3500

# init SOC of Storage
devices['stg01'].initSOC = 1000*flag2
devices['stg01'].maxCap = 1000*flag2 *10
devices['stg01'].maxSOC = 2000*flag2*10

for i in range(24):
    if flag3 and (i <=8 or 21<i<24):
        source['s1'].pElecSell[i] = source['s1'].pElecSell[i] + 0.1 ##if i <= 8 or 21 < i < 24:
        source['s1'].pPurchase[i] = source['s1'].pPurchase[i] + 0.1

devices['chp02'].maxCap = 2000
devices['chp02'].elec_vs_steam = 1850.48
devices['chp02'].pointList = [{"y": 956.6, "x": 273.3142857},
                              {"y": 1005.0, "x": 287.965616},
                              {"y": 1113.4, "x": 313.6338028},
                              {"y": 1269.2, "x": 350.6077348},
                              {"y": 1321.8, "x": 363.1318681},
                              {"y": 1420.0, "x": 385.8695652},
                              {"y": 1523.6, "x": 411.7837838},
                              {"y": 1638.6, "x": 439.3029491},
                              {"y": 1753.2, "x": 467.52},
                              {"y": 1801.8, "x": 477.9310345}]

timer.start()
# create energy hub
model = EnergyHub(source, devices, user, topology, onOffMap, loads)
model.solver = 'CPLEX_CMD'
model.solve()
draw()
#draw_stable()
timer.stop()

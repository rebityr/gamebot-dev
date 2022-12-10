from workwithdb import workDB
from config import buildings_info, VK_TOKEN, farm_open, convoy_open

import time
from datetime import datetime
import vk_api

bh = vk_api.VkApi(token=VK_TOKEN)
bh.get_api()
DB = workDB('db.db')


def mess(id, text):
    bh.method('messages.send', {'user_id' : id, 'message' : text, 'random_id': 0})

def give_res():
    for data in DB.get_all('users', ret='lst'):
        new_gold = DB.get_row('economic', buildings_info['castle'][1] + data[7])[3]
        DB.set_cell('users', data[1], 'res_gol', data[3] + new_gold * data[24])
        new_ore = DB.get_row('economic', buildings_info['mine'][1] + data[8])[3]
        DB.set_cell('users', data[1], 'res_ore', data[5] + new_ore * data[24])
        new_wood = DB.get_row('economic', buildings_info['sawmill'][1] + data[9])[3]
        DB.set_cell('users', data[1], 'res_wod', data[4] + new_wood * data[24])
        if data[7] >= 4:
            new_food = DB.get_row('economic', buildings_info['farm'][1] + data[10])[3]
            DB.set_cell('users', data[1], 'res_fod', data[6] + new_food * data[24])


def reset_convoy():
    for data in DB.get_all('users', ret='lst'):
        DB.set_cell('users', data[1], 'send_today', 0)


def events():
    dt = DB.get_all_event()
    if dt:
        for t in dt:
            if t[2] - 1:
                DB.set_cell_event('time', t[2] - 1, t[0], t[1])
            else:
                if 'up' in t[1]:
                    if t[1].split('_')[1] == 'castle':
                        data = DB.get_row_users(t[0])
                        if data[7] + 1 == 4:
                            DB.set_cell('users', t[0], 'lvl_far', data[10] + 1)
                            mess(t[0], farm_open)
                        elif data[7] + 1 == 5:
                            DB.set_cell('users', t[0], 'lvl_con', data[11] + 1)
                            mess(t[0], convoy_open)
                            mess(t[0], 'Игрок Король прислал вам 100 💎Кристаллов')
                            mess(t[0], 'Игрок Король прислал вам 25k 💰Золота')
                            DB.set_cell('users', t[0], 'res_cry', data[2] + 100)
                            DB.set_cell('users', t[0], 'res_gol', data[3] + 25000)
                        else:
                            mess(t[0], 'Уровень замка повышен!')
                        DB.set_cell('users', t[0], 'lvl_cas', data[7] + 1)
                        DB.set_cell('users', t[0], 'builders', data[15] + 1)
                    elif t[1].split('_')[1] == 'mine':
                        mess(t[0], 'Уровень шахты повышен!')
                        data = DB.get_row_users(t[0])
                        DB.set_cell('users', t[0], 'lvl_min', data[8] + 1)
                        DB.set_cell('users', t[0], 'builders', data[15] + 1)
                    elif t[1].split('_')[1] == 'sawmill':
                        mess(t[0], 'Уровень лесопилки повышен!')
                        data = DB.get_row_users(t[0])
                        DB.set_cell('users', t[0], 'lvl_saw', data[9] + 1)
                        DB.set_cell('users', t[0], 'builders', data[15] + 1)
                    elif t[1].split('_')[1] == 'farm':
                        mess(t[0], 'Уровень фермы повышен!')
                        data = DB.get_row_users(t[0])
                        DB.set_cell('users', t[0], 'lvl_far', data[10] + 1)
                        DB.set_cell('users', t[0], 'builders', data[15] + 1)
                    elif t[1].split('_')[1] == 'convoy':
                        mess(t[0], 'Уровень каравана повышен!')
                        data = DB.get_row_users(t[0])
                        DB.set_cell('users', t[0], 'lvl_con', data[11] + 1)
                        DB.set_cell('users', t[0], 'builders', data[15] + 1)
                
                DB.delete_row_from_check(t[1], t[0])


def shild():
    u = [i for i in DB.get_all('users', ret='lst') if i[23]]
    for i in u:
        DB.set_cell('users', i[1], 'shild', i[23] - 1)


if __name__ == '__main__':
    print('--- UPDATER ON ---')
    reset_flag = True

    time_for_res = 60
    while True:
        time_for_res -= 1
        dt = datetime.now()

        if not time_for_res:
            give_res()
            print('--- UPDATER give_res FUNC DONE ---')
            time_for_res = 60
        
        if not dt.hour:
            if reset_flag:
                reset_convoy()
                print('--- UPDATER reset_convoy FUNC DONE ---')
                reset_flag = False
        else:
            reset_flag = True
        
        events()
        shild()

        time.sleep(1)
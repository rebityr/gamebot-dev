from vkbottle import Keyboard, KeyboardButtonColor, Text, Callback

COLORS = {
    'BLUE': KeyboardButtonColor.PRIMARY,
    'WHITE': KeyboardButtonColor.SECONDARY,
    'RED': KeyboardButtonColor.NEGATIVE,
    'GREEN': KeyboardButtonColor.POSITIVE
}

def keyboard_start(step=1):
    keyboard = Keyboard()

    if step == 1:
        keyboard.add(Text('Основать поселение'), color=COLORS['GREEN'])
    elif step == 2:
        keyboard.add(Text('Построить здания'), color=COLORS['GREEN'])
    elif step == 3:
        keyboard.add(Text('Начать путь Завоевателя.'), color=COLORS['GREEN'])
    
    return keyboard

def keyboard_menu(lvl_cas=1):
    keyboard = Keyboard()

    btns = [
        ['📖Инфо', '🕍Здания'],
        ['🔥Война', '🥇Рейтинг'],
        ['📜Помощь']
    ]

    for i in btns[:-1]:
        for j in i:
            if j in ('🔥Война', '🥇Рейтинг') and lvl_cas < 8:
                keyboard.add(Text(j), color=COLORS['RED'])
            else:
                keyboard.add(Text(j), color=COLORS['BLUE'])
        keyboard.row()
    
    keyboard.add(Text(btns[-1][0]), color=COLORS['BLUE'])
    
    return keyboard

def keyboard_btn(menu, lvl_cas=1, war=0, enemy='', skip=0):
    keyboard = Keyboard()

    btns = []

    if menu == 'buildings':
        btns = [
            ['🕍Замок', '⛏Шахта'],
            ['🌲Лесопилка', '🌻Ферма'],
            ['⚖Караван']
        ]
        if skip:
            btns.insert(0, [f'Пропустить за {skip}💎'])
    elif menu in ['🕍Замок', '⛏Шахта', '🌲Лесопилка', '🌻Ферма', '⚖Караван']:
        btns = [
            ['📖Инфо', '⚒Улучшить']
        ]
    elif menu == 'war':
        btns = [
            ['⚔Пехота', '🏹Лучники', '🏇Конница'],
            ['🔎Разведка (1000💰)']
        ]
    elif menu == 'war_attack':
        btns = [
            ['Напасть🔥', '🔎Разведка (1000💰)']
        ]
    elif menu == 'war_enemy':
        btns = [
            [f'5{enemy}', f'50{enemy}', f'500{enemy}'],
            [f'1000{enemy}', f'2000{enemy}', f'5000{enemy}']
        ]
    
    for i in btns:
        for j in i:
            if j == '🌻Ферма' and lvl_cas < 4:
                keyboard.add(Text(j), color=COLORS['RED'])
            elif j == '⚖Караван' and lvl_cas < 5:
                keyboard.add(Text(j), color=COLORS['RED'])
            elif j == 'Напасть🔥':
                keyboard.add(Callback(j, {'cmd': war}))
            elif 'Пропустить за ' in j:
                keyboard.add(Text(j), color=COLORS['GREEN'])
            else:
                keyboard.add(Text(j), color=COLORS['BLUE'])
        keyboard.row()

    for j in ['👈Назад', '🏕Домой','📜Помощь']:
        keyboard.add(Text(j), color=COLORS['WHITE'])

    return keyboard

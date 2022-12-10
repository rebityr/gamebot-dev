VK_TOKEN = '' # Вставить токен из ВК

buildings_info = {
    'castle': ['🕍Замок', 0, '💰'],
    'mine': ['⛏Шахта', 60, '⛏'],
    'sawmill': ['🌲Лесопилка', 30, '🌲'],
    'farm': ['🌻Ферма', 90, '🍖'],
    'convoy': ['⚖Караван', 120, '💎']
}

"""сообщения"""
msg_start_1 = 'Представь, что ты - крестьянин, только что сбежавший от своего хозяина-тирана. Что делать, куда бежать? Выхода нет, чтобы выжить, ты с другими крестьянами основываешь свое поселение. Теперь только на тебе лежит ответственность за остальных. Воздвигнешь несокрушимую империю или падешь под гнетом врагов - зависит только от твоих действий'

msg_start_2 = 'Первым делом каждый правитель должен задуматься об экономике. В твоем распоряжении есть здания, необходимые для добычи ценных ресурсов. Чтобы увеличить добычу, тебе нужно улучшать эти здания. После этого можно будет задумываться о войне. Ты сможешь обучать и нанимать войска, с помощью которых будешь нападать на других игроков. Но будь на готове - другие тоже могут напасть.'

msg_start_3 = 'Ну вот ты и готов начать свой путь. Удачи тебе!'

msg_start_4 = 'Экономика - это основа любого государства. Сейчас у тебя есть три вида ресурсов 💰Золото, ⛏Руда и 🌲Дерево, они нужны для строительства зданий, для найма армии, для развития науки в твоем государстве.\n\nИх добычей занимаются здания, а именно 🕍Замок, ⛏Шахта и 🌲Лесопилка. Улучшай их, чтобы они производили больше ресурсов.'

msg_start_5 = 'Пока вы искали место, чтобы обосновать свое государство, вы наткнулись на склад с оставшимися ресурсами! Видимо, это был покинутый военный лагерь:\n\n+50 💰Золота\n+140 🌲Дерева\n+90 ⛏Руды\n\nНо на эти ресурсы великую империю не построить! Скорее зайди в 🕍Здания, нажми на 🕍Замок, а затем Улучшить. Это позволит увеличить производство 💰Золота.'

msg_help = 'Завоеватель - это игровой бот, в котором ты можешь взять в руки управление целым средневековым государством. Построишь ли ты несокрушимую экономику или станешь искусным воином, встречи с которым будут бояться все остальные Завоеватели - зависит только от тебя.\n\nИгра строится на ресурсах, необходимых для развития своего государства: 💰Золота, 🌲Дерева, ⛏Руды, 🍖Еды. Все они добываются в 🕍Зданиях твоего государства. Кроме того, их можно получить при атаке на другого Завоевателя. Первые три нужны для улучшения 🕍Зданий. 🍖Еда же необходима для найма ⚔Воинов.\n\nТак же есть особый вид ресурсов - 💎Кристаллы. Это ценнейший ресурс, на них можно купить Щит от нападений, Смену никнейма или Чары для ускорения добычи ресурсов. Их можно попробовать выиграть в Турнире короля, или купить за реальные деньги.'

msg_war_den = 'Доступ к 🔥Войнe открывается с 8 уровня 🕍Замка'

msg_top_den = 'Доступ к 🥇Рейтингу открывается с 8 уровня 🕍Замка'

msg_buildings_help = 'В этом разделе отображены все 🏘Постройки в твоих владениях и их уровни. Выбери здание, чтобы узнать информацию или улучшить его.\n\nКаждое здание улучшается определенное количество времени. Процесс можно ускорить с помощью 💎Кристаллов. Один кристалл ускоряет строительство на три минуты.'

msg_buildings = 'bname\n\nУровень: blevel\nДоход: +income в минуту\n\nУлучшить:\nnext_gold💰\nnext_wood🌲\nnext_ore⛏\n\nДоход улучшения:\n+next_income в минуту\n\nВремя улучшения:\n⌛time'

msg_build_max_level = 'bname\n\nУровень: blevel - максимальный\nДоход: +income в минуту'

msg_buildings_convoy = 'bname\n\nПеревезено сегодня: send_today\n\nУровень: blevel\nДоход: +income в минуту\nЛимит перевозок: limit ресурсов/день\n\nУлучшить:\nnext_gold💰\nnext_wood🌲\nnext_ore⛏\n\nДоход улучшения:\n+next_income в минуту\nЛимит перевозок: next_limit ресурсов/день\n\nВремя улучшения:\n⌛time'

msg_convoy_max_level = 'bname\n\nПеревезено сегодня: send_today\n\nУровень: blevel - максимальный\nДоход: +income в минуту\nЛимит перевозок: limit ресурсов/день'

msg_convoy_error = 'Что-то не так, проверь, что ввел все правильно'

msg_convoy_limit = 'Такое количество ресурсов превышает лимит ресурсов в день. Введи меньшее количество ресурсов или дождись обновления лимита.'

msg_convoy_needmore = 'Твоих ресурсов недостаточно, чтобы отправить караван.'

msg_castle_help = 'Замок занимается сбором налогов с твоих владений. Чем выше уровень 🕍Замка тем больше 💰Золота ты получаешь в минуту.'

msg_mine_help = '⛏Шахта нужна для добычи ⛏Руды. Чем выше уровень ⛏Шахты тем больше ⛏Руды ты получаешь в минуту.'

msg_sawmill_help = '🌲Лесопилка нужна для добычи 🌲Дерева. Чем выше уровень 🌲Лесопилки тем больше 🌲Дерева ты получаешь в минуту.'

msg_farm_help = '🌻Ферма нужна для производства 🍖Еды. Чем выше уровень 🌻Фермы тем больше 🍖Еды ты получаешь в минуту.'

msg_farm_den = 'Доступ к 🌻Ферме открывается с 4 уровня 🕍Замка'

msg_con_help = '⚖Караван в вашем королевстве занимаются перевозками ресурсов. От их уровня зависит количество ресурсов, которое вы можете отправлять за день, и скорость их доставки.\n\nИногда бывает намного выгоднее сторговаться с другим Завоевателем, чем терять комиссию на 🎪Рынке.\n\nДля отправки ресурсов союзнику используйте команду "Отправить <количество> <золота/руды/дерева/еды> <ID Завоевателя>". Например чтобы отправить 1000 Золота Завоевателю с ID 1, нужно написать "Отправить 1000 золота 1"'

msg_con_den = 'Доступ к ⚖Каравану открывается с 5 уровня 🕍Замка'

msg_error = 'Вижу у тебя есть какие-то проблемы с клавиатурой, вывел меню'

msg_war_help = 'Ты находишься в разделе 🔥Война. Здесь ты можешь посмотреть состояние армии, заняться Наймом войск. При нажатии на 🔎Разведка, твои разведчики постараются найти Поселение с примерно такими же 🌍Территориями. Каждая разведка стоит 1000💰.\nСуществует три типа войск:\n\n⚔Пехота - способна укрываться щитами, поэтому сильнее чем 🏹Лучники, но проигрывают Коннице на поле боя.\n🏹Лучники - атакуют со стен, поэтому на поле боя эффективнее чем 🏇Конница, но проигрывают Пехоте\n🏇Конница - сильнее ⚔Пехоты, но проигрывают 🏹Лучникам'

farm_open = 'Твое поселение сильно развилось! Теперь твоим жителям нужна 🍖еда, поэтому они построили 🌻Ферму. Она будет приносить тебе 🍖еду, которую ты сможешь продать в дальнейшем на 🎪Рынке, или использовать для содержания твоей собственной ⚔Армии.'

convoy_open = 'Уже 5 уровень 🕍Замка! Такому большому государству просто необходим 🎪Рынок, поэтому вы повелеваете построить его. На нем вы сможете покупать и продавать ресурсы за 💰Золото.\n\nВместе с 🎪Рынком вы получили ⚖Караван. С помощью них можно отправлять ресурсы другим игрокам. Для этого зайдите в 🕍Здания, в ⚖Караван и нажмите 📜Помощь.\n\nКороль заметил, как быстро растет ваше поселение, и решил помочь вам ресурсами!'

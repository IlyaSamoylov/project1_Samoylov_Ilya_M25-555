# labyrinth_game/constants.py
ROOMS = {
    'entrance': {
        'description': 'Вы в темном входе лабиринта. Стены покрыты мхом. '
                       'На полу лежит старый факел.',
        'exits': {'north': 'hall', 'east': 'trap_room'},
        'items': ['torch'],
        'puzzle': None
    },
    'hall': {
        'description': 'Большой зал с эхом. По центру стоит пьедестал с запечатанным '
                       'сундуком.',
        'exits': {'south': 'entrance', 'west': 'library', 'north': 'treasure_room'},
        'items': [],
        'puzzle': ('На пьедестале надпись: "Назовите число, которое идет после девяти".'
                   ' Введите ответ цифрой или словом.',
                   ['10', 'десять', 'ten', 'b1010'], 'small_budda_statue')
    },
    'trap_room': {
          'description': 'Комната с хитрой плиточной поломкой. На стене видна надпись:'
                         ' "Осторожно — ловушка".',
          'exits': {'west': 'entrance'},
          'items': ['rusty_key'],
          'puzzle': ('Система плит активна. Чтобы пройти, назовите слово "шаг" три раза'
                     ' подряд (введите "шаг шаг шаг")', ['шаг шаг шаг'],
                     'protective_charm')
    },
    'library': {
          'description': 'Пыльная библиотека. На полках старые свитки. Где-то здесь '
                         'может быть ключ от сокровищницы.',
          'exits': {'east': 'hall', 'north': 'armory'},
          'items': ['ancient_book'],
          'puzzle': ('В одном свитке загадка: "Что растет, когда его съедают?"'
                     ' (ответ одно слово)',
                     ['резонанс', 'resonance', 'аппетит', 'appetite', 'голод', 'hunger']
                         , 'wisdom_script')
    },
    'armory': {
          'description': 'Старая оружейная комната. На стене висит меч, рядом — '
                         'небольшая бронзовая шкатулка.',
          'exits': {'south': 'library', 'east': 'secret_garden'},
          'items': ['sword', 'bronze_box'],
          'puzzle': None
    },
    'treasure_room': {
          'description': 'Комната, на столе большой сундук. Дверь заперта — нужен '
                         'особый ключ.',
          'exits': {'south': 'hall'},
          'items': ['treasure_chest'],
          'puzzle': ('Дверь защищена кодом. Введите код (подсказка: это число '
                     'пятикратного шага, 2*5= ? )',
                     ['10', 'десять', 'ten', 'b1010'], 'tons_of_gold')
    },
    'secret_garden': {
            'description': 'Заброшенный сад с искрящимся фонтаном. В воздухе пахнет'
                           ' магией.',
            'exits': {'west': 'armory', 'south': 'observatory'},
            'items': ['magic_flower'],
            'puzzle': ('Фонтан шепчет: "В центре парка или сада, \nНикому я не '
                       'преграда; \nМой цветок подобен раю, \nЯ — водою расцветаю,"',
                       ['фонтан', 'fountain', 'источник', 'source'], 'magic_seeds')
    },
    'observatory': {
            'description': 'Круглая комната с куполом из хрусталя. Телескоп направлен '
                           'на звезды.',
            'exits': {'north': 'secret_garden'},
            'items': ['star_map'],
            'puzzle': ('На табличке написано: "Сколько планет в Солнечной системе?"'
                       ' (ответ цифрой)',
                       ['8', 'восемь', 'eight', 'b1000'], 'crystal_lens')
    }
}

COMMANDS = {
    "go <direction>": "перейти в направлении (north/south/east/west)",
    "look": "осмотреть текущую комнату",
    "take <item>": "поднять предмет",
    "use <item>": "использовать предмет из инвентаря",
    "inventory": "показать инвентарь",
    "solve": "попытаться решить загадку в комнате",
    "quit": "выйти из игры",
    "help": "показать это сообщение"
}

# TODO: поменять комнаты возможно
import math

from labyrinth_game.constants import ROOMS


def describe_current_room(game_state):
    '''
    Функция для описания текущей комнаты

    Parameters:
        game_state: dict, словарь игрового состояния
    '''
    cur_room_name = game_state['current_room'] # название комнаты
    cur_room_dict = ROOMS[cur_room_name] # словарь текущей комнаты из ROOMS
    print(f'== {cur_room_name.upper()} ==')
    print(f'{ROOMS[cur_room_name]['description']}')
    if cur_room_dict['items']:
        print(f'Заметные предметы: {cur_room_dict['items']}')
    print(f'Выходы: {list(cur_room_dict['exits'].keys())}')
    if cur_room_dict['puzzle']:
        print('"Кажется, здесь есть загадка (используйте команду solve)."')

def show_help(commands):
    '''
    Функция выводит справку доступных команд
    '''
    print("\nДоступные команды:")
    for command, description in commands.items():
        # Форматируем строку: команда занимает 16 символов, выровнена по левому краю
        print(f"  {command:<16} - {description}")

def solve_puzzle(game_state):
    '''
    Функция для решения загадок. Выводит сообщение об отсутствии загадок, если их нет
    в комнате. Иначе выводит вопрос и получает ответ с консоли. Если ответ правильный
    - удаляет загадку из комнаты и награждает игрока, иначе - выводит сообщение.

    Parameters:
        game_state: dict, словарь игрового состояния
    '''
    cur_room_name = game_state['current_room']
    cur_room_dict = ROOMS[cur_room_name]

    if not cur_room_dict['puzzle']:
        print("Загадок здесь нет")

    else:
        # Выводим вопрос и получаем ответ
        question, correct_answer, reward = cur_room_dict['puzzle']
        print(f"\n{question}")
        user_answer = input()
        print(f"Ваш ответ: {user_answer}")
        if user_answer in correct_answer:
            print("Правильно")
            print(f"В награду вы получаете: {reward}")

            cur_room_dict['puzzle'] = None

            # должна ли функция возвращать game_state?
            # Нехорошо же функцией изменять переменную
            game_state['player_inventory'].extend(reward)

        else:
            if cur_room_name == 'trap_room':
                trigger_trap(game_state)
                return
            print("\nНеверно. Попробуйте снова (solve).")

def attempt_open_treasure(game_state):
    """
    Функция попытки открыть сундук с сокровищами в комнате treasure_room. Если игрок
    не в комнате сокровищ и сундук не на месте,вывести сообщение об отсутствии сундука.
    Если у игрока есть ключ - игра выигран. Если ключа нет - можно решить загадку

    Args:
        game_state (dict): Текущее состояние игры

    Returns:
        dict: Обновленное состояние игры
    """
    current_room_name = game_state['current_room']
    current_room = ROOMS[current_room_name]

    # сценарий 1: у игрока есть ключ
    # treasure_key или rusty_key?
    if  'treasure_key' in game_state['player_inventory']:
        print("Вы делаете поворот ключом и замок щёлкает. Сундук открыт!")

        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True

    # сценарий 2: попытка взлома кодом
    else:
        print("Сундук заперт. У вас нет ключа, но есть возможность ввести код.")
        print(f'Загадка на сундуке: {current_room['puzzle'][0]}')

        choice = input("Ввести код? (да/нет): ").strip().lower()

        if choice == 'да':
            code = input("Введите код: ").strip()

            # проверка кода
            if code in current_room['puzzle'][1]:
                print("Код верный! Сундук открыт.")
                print("В сундуке сокровище! Вы победили!")

                game_state['game_over'] = True
            else:
                print("Неверный код. Сундук не открылся.")
        else:
            print("Вы отступаете от сундука.")

def pseudo_random(seed, modulo):
    '''
    Псевдослучайный генератор на основе числа шагов
    Args:
        seed: int, сид, например, число шагов
        modulo: int, верхняя граница диапазона результата

    Returns:
        rand_val: int, целое в диапазоне [0, modulo)
    '''
    value = math.sin(seed * 12.9898) * 43758.5453
    value = (value - math.floor(value))
    rand_val = int(value * modulo)
    return rand_val

def trigger_trap(game_state):
    '''
    Функции срабатывания ловушки. Если инвентарь пуст - с помощью генератора чисел
    выбирается урон. Если он больше или равен threshold, игра окончена.
    Если меньше - игрок выживает. Если в инвентаре были предметы - случайный удаляется.
    Args:
        game_state (dict): Текущее состояние игры

    Returns:

    '''
    threshold = 6
    print("Ловушка активирована, пол стал дрожжать")

    if game_state['player_inventory']:
        missing_item_idx = pseudo_random(game_state['steps_taken'],
                                         len(game_state['player_inventory']))
        print(f'{game_state['player_inventory'][missing_item_idx]} безвозвратно утерян')
        game_state['player_inventory'].pop(missing_item_idx)
    else:
        injure = pseudo_random(game_state['steps_taken'], 11)
        print(f'Урон = {injure}')
        if injure <= threshold:
            print("Удача, вы смогли уцелеть!")
        else:
            print("Ловушка захлопнулась. К сожалению, это конец")
            game_state['game_over'] = True

def random_event(game_state):
    '''
    Функция для инициации случайных событий при перемещении игрока. Случайное
    число сравнивается с потолком. Если оно меньше - случайным образом происходит
    один из трех сценариев.
    Args:
        game_state (dict): Текущее состояние игры

    Returns:

    '''
    threshold = 7
    event_prob = pseudo_random(game_state['steps_taken'], 11)

    if event_prob < threshold:
        event_scenario = pseudo_random(game_state['steps_taken'], 3)
        match event_scenario:
            case 0:
                print("Что это блестит? Монета!")
                ROOMS[game_state['current_room']]['items'].append("coin")
            case 1:
                print("Неподалеку слышен подозрительный шорох")
                if 'sword' in game_state['player_inventory']:
                    print("Существо испугалось вашего меча")
                else:
                    print("Кажется, что-то наблюдает за вами")
            case 2:
                if game_state['current_room'] == 'trap_room' and \
                    'torch' not in game_state['player_inventory']:
                    print("Осторожно, ловушки!")
                    trigger_trap(game_state)


# TODO: разобраться с treasure key - его нигде нет
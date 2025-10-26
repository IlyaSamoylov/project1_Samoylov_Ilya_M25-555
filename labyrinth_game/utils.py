from labyrinth_game.constants import ROOMS
from labyrinth_game.player_actions import get_input

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
        print(f'"Кажется, здесь есть загадка (используйте команду solve)."')

def show_help():
    '''
    Функция выводит справку доступных команд
    '''
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")

def solve_puzzle(game_state):
    '''
    Функция для решения загадок. Выводит сообщение об отсутствии загадок, если их нет в комнате.
    Иначе выводит вопрос и получает ответ с консоли. Проверяет правильность ответа,
    если правильно - удаляет загадку из комнаты и награждает игрока. Если ответ неверен - выводит сообщение.

    Parameters:
        game_state: dict, словарь игрового состояния
    '''

    cur_room_dict = ROOMS[game_state['current_room']]

    if not cur_room_dict['puzzle']:
        print("Загадок здесь нет")

    else:
        # Выводим вопрос и получаем ответ
        question, correct_answer = cur_room_dict['puzzle']
        print(f"\n{question}")
        user_answer = get_input()
        print(f"Ваш ответ: {user_answer}")
        if user_answer == correct_answer:
            print("Правильно")

            cur_room_dict['puzzle'] = None

            # изменить награду
            game_state['coins'] += 1 # должна ли функция возвращать game_state? Нехорошо же функцией изменять переменную

        else:
            print("\nНеверно. Попробуйте снова (solve).")

def attempt_open_treasure(game_state):
    """
    TODO: проверить, не избыточна ли функа
    Функция попытки открыть сундук с сокровищами в комнате treasure_room. Если игрок не в комнате сокровищ и сундук не
    на месте,вывести сообщение об отсутствии сундука. Если у игрока есть ключ - игра выигран. Если ключа нет - можно
    решить загадку

    Args:
        game_state (dict): Текущее состояние игры

    Returns:
        dict: Обновленное состояние игры
    """
    current_room_name = game_state['current_room']
    current_room = ROOMS[current_room_name]

    # проверка, что игрок в комнате с сокровищами и сундук еще есть
    if current_room_name != 'treasure_room' or 'treasure_chest' not in current_room['items']:
        print("Здесь нет сундука с сокровищами.")
        # return game_state

    # сценарий 1: у игрока есть ключ
    # treasure_key или rusty_key?
    elif 'rusty_key' in game_state['player_inventory']:
        print("Вы делаете поворот ключом и замок щёлкает. Сундук открыт!")

        # удалить сундук из комнаты
        current_room['items'].remove('treasure_chest')

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
            if current_room['puzzle'] and code == current_room['puzzle'][1]:
                print("Код верный! Сундук открыт.")

                # удалить сундук из комнаты
                current_room['items'].remove('treasure_chest')

                print("В сундуке сокровище! Вы победили!")
                game_state['game_over'] = True
            else:
                print("Неверный код. Сундук не открылся.")
        else:
            print("Вы отступаете от сундука.")

# TODO: разобраться с rusty/treasure key - один нигде не используется, второй не подобрать
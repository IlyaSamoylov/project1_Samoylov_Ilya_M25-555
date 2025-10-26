#!/usr/bin/env python3
import labyrinth_game.utils as utils
import labyrinth_game.player_actions as player_actions

def main():

    # словарь состояния
    game_state = {
        'player_inventory': [],  # инвентарь
        'current_room': 'entrance',  # текущая комната
        'game_over': False,  # игра окончена
        'steps_taken': 0 , # количество пройденных шагов
        'coins': 0  # монетки в награду  TODO: придумать награду за решение загадок
    }

    print("Добро пожаловать в Лабиринт сокровищ!")

    # описание текущей комнаты
    utils.describe_current_room(game_state)

    # цикл игры
    while not game_state['game_over']:
       command = player_actions.get_input()
       process_command(game_state, command)

def process_command(game_state, command):
    '''
    Функция для реакции на команды игрока

    Parameters:
        game_state: dict, словарь состояния игры
        command: str, команда с консоли
    '''

    com_parts = command.strip().lower().split() # предварительная обработка

    # разделение команды на тело и аргументы
    command_body = com_parts[0]
    argument = ' '.join(com_parts[1:]) if len(com_parts) > 1 else None

    match command_body:
        case 'осмотреть' | 'осмотреться' | 'look' | 'examine':
            utils.describe_current_room(game_state)

        case 'использовать' | 'use' if argument:
            player_actions.use_item(game_state, argument)

        case 'идти' | 'перейти' | 'go' | 'move' if argument:
            player_actions.move_player(game_state, argument)

        case 'взять' | 'take' | 'grab' if argument:
            player_actions.take_item(game_state, argument)

        case 'инвентарь' | 'inventory' | 'inv':
            player_actions.show_inventory(game_state)

        case 'выход' | 'exit' | 'quit':
            print("Спасибо за игру!")
            game_state['game_over'] = True

        case 'помощь' | 'help' | '?':
            utils.show_help()

        case 'solve':
            if game_state['current_room'] == 'treasure_room':
                utils.attempt_open_treasure(game_state)
            else:
                utils.solve_puzzle(game_state)

        case _:
            print('Неправильная команда. Вызовите справку с help')

if __name__ == "__main__":
    main()

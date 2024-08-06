import os
import sys

def board(state):
    print("Current State:")
    for i, pile in enumerate(state['piles']):
        print(f"Pile {i + 1}: Red: {pile['red']} | Blue: {pile['blue']}")

def is_terminal(state):
    return all(p['red'] == 0 and p['blue'] == 0 for p in state['piles'])

def evaluate(color_removed, marbles_removed):
    if color_removed == 'red':
        return marbles_removed * 2
    elif color_removed == 'blue':
        return marbles_removed * 3
    else:
        return 0

ft = None
def first():
    global ft
    print("\n")
    while True:
        ft = input("Who has the first turn, Human or AI: ")
        if ft.lower() == "human":
            return True
        elif ft.lower() == "ai":
            return False
        else:
            print("Enter a valid choice!")
            continue

def player(state):
    print("\nPlayer Turn:")
    while True:
        pile = int(input("Which pile do you want to take from: ")) - 1
        if pile >= 0 and pile < 3:
            if state['piles'][pile]['red'] == 0 and state['piles'][pile]['blue'] == 0:
                print("Pile is empty!\nChoose another Pile.")
                continue

            while True:
                c = input("Enter 'r' for red and 'b' for blue: ").lower()
                if c == "r":
                    if state['piles'][pile]['red'] <= 0:
                        print("No red marbles left!\nChoose another color.")
                        continue
                    elif state['piles'][pile]['red'] > 0:
                        print(f"There are {state['piles'][pile]['red']} red marbles in this Pile.")
                        while True:
                            s = int(input("Enter how many red marbles you want to remove: "))
                            if s <= state['piles'][pile]['red'] and s != 0:
                                state['piles'][pile]['red'] -= s
                                print(f"You have removed {s} red marbles from the pile.")
                                return state, 'red', s
                            elif s == 0:
                                print("You have to remove at least 1 marble to change the turn!")
                                continue
                            else:
                                print("Enter a valid number of marbles.")
                                continue
                elif c == "b":
                    if state['piles'][pile]['blue'] <= 0:
                        print("No blue marbles left!\nChoose another color.")
                        continue
                    elif state['piles'][pile]['blue'] > 0:
                        print(f"There are {state['piles'][pile]['blue']} blue marbles in this Pile.")
                        while True:
                            s = int(input("Enter how many blue marbles you want to remove: "))
                            if s <= state['piles'][pile]['blue'] and s != 0:
                                state['piles'][pile]['blue'] -= s
                                print(f"You have removed {s} blue marbles from the pile.")
                                return state, 'blue', s
                            elif s == 0:
                                print("You have to remove at least 1 marble to change the turn!")
                                continue
                            else:
                                print("Enter a valid number of marbles.")
                                continue
                else:
                    print("Invalid choice!\nChoose either 'r' or 'b'.")
                    continue

        else:
            print("Invalid Input!\nChoose pile according to numbers.")
            continue

def allmoves(state):
    moves = []
    for i, pile in enumerate(state['piles']):
        if pile['red'] > 0:
            for r in range(1, pile['red'] + 1):
                new_state = {'piles': [{'red': p['red'], 'blue': p['blue']} for p in state['piles']]}
                new_state['piles'][i]['red'] -= r
                moves.append((new_state, 'red', r))
        if pile['blue'] > 0:
            for b in range(1, pile['blue'] + 1):
                new_state = {'piles': [{'red': p['red'], 'blue': p['blue']} for p in state['piles']]}
                new_state['piles'][i]['blue'] -= b
                moves.append((new_state, 'blue', b))
    return moves

def AB(state, depth, alpha, beta, maximizing_player):
    if depth == 0 or is_terminal(state):
        current_player = "ai" if maximizing_player else "human"
        return evaluate(state, current_player)

    if maximizing_player:
        max_eval = float('-inf')
        for child, _, _ in allmoves(state):
            eval = AB(child, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for child, _, _ in allmoves(state):
            eval = AB(child, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval) 
            if beta <= alpha:
                break
        return min_eval

def computermove(state, depth):
    best_eval = float('-inf')
    best_move = None
    best_color_removed = None
    best_marbles_removed = 0

    for move, color_removed, marbles_removed in allmoves(state):
        eval = AB(move, depth - 1, float('-inf'), float('inf'), False)
        if eval > best_eval:
            best_eval = eval
            best_move = move
            best_color_removed = color_removed
            best_marbles_removed = marbles_removed

    return best_move, best_color_removed, best_marbles_removed

def score_counter(winner, final_score):
    global comp_score, player_score
    if winner == "Computer":
        comp_score += final_score
    else:
        player_score += final_score

def Standard(state):
    if first():
        current_player = "human"
    else:
        current_player = "ai"

    last_move_color = None
    marbles_removed = 0

    while not is_terminal(state):
        os.system("cls")
        board(state)

        if current_player == "human":
            state, last_move_color, marbles_removed = player(state)
            current_player = "ai"
        else:
            state, last_move_color, marbles_removed = computermove(state, depth=3)
            os.system("cls")
            board(state)
            print(f"\nComputer moved. {last_move_color.capitalize()} marbles removed: {marbles_removed}")
            input("\nPress Enter to continue...")
            current_player = "human"

    final_score = evaluate(last_move_color, marbles_removed)
    winner = "Computer" if current_player == "human" else "Human"

    os.system("cls")
    print("\n\tGame Over!")
    print(f"\n\t{winner} wins the round\n")
    score_counter(winner, final_score)
    input("Press Enter to continue .....")

def Misere(state):
    if first():
        current_player = "human"
    else:
        current_player = "ai"

    last_move_color = None
    marbles_removed = 0

    while not is_terminal(state):
        os.system("cls")
        board(state)

        if current_player == "human":
            state, last_move_color, marbles_removed = player(state)
            current_player = "ai"
        else:
            state, last_move_color, marbles_removed = computermove(state, depth=3)
            os.system("cls")
            board(state)
            print(f"\nComputer moved. {last_move_color.capitalize()} marbles removed: {marbles_removed}")
            input("\nPress Enter to continue...")
            current_player = "human"

    final_score = evaluate(last_move_color, marbles_removed)
    winner = "Computer" if current_player == "ai" else "Human"

    os.system("cls")
    print("\n\tGame Over!")
    print(f"\n\t{winner} wins the round\n")
    score_counter(winner, final_score)
    input("Press Enter to continue .....")

print("\n\t\tWelcome to the Red-Blue NIM\n")
state = {'piles': [{'red': 3, 'blue': 3}, {'red': 2, 'blue': 4}, {'red': 1, 'blue': 5}]}
board(state)

comp_score = 0
player_score = 0

while True:
    print("\nEnter which version you want to play:\n\n1)Standard \t\t2)Misère ")
    ch = input("\nSelect: ")

    if(ch=="1" or ch.lower() == "standard"):
        os.system("cls")
        print("\n\t\tStandard Red Blue NIM\n")
        print("Rules:\n• You can remove marble only from one row at a time.")
        print("• You can remove the number of marbles of your own choice but of same colour Red or Blue.")
        print("• Marble removed at last turn will give the score to winner Blue gives three points while Red gives two points.")
        print("• Remember, the player who removes the last marble will win the game.")

        input("\nPlease Enter to Start .....")
        os.system("cls")
        Standard(state)
        while True:
            os.system("cls")
            print("\nDo you want to play more rounds or you want to exit:\n\n1)More\t\t2)Exit")
            em = input("\nWhat's your decision: ")
            if em == "1" or em.lower() == "more":
                os.system("cls")
                break
            elif em == "2" or em.lower() == "exit":
                os.system("cls")
                print("\t\tFINAL SCORE")
                print(f"\nComputer: {comp_score}\t\tPlayer: {player_score}\n")
                sys.exit(0)
            else:
                print("Answer according to given options to continue!")
                continue

    elif(ch=="2" or ch.lower() in ["misère", "misere"]):
        os.system("cls")
        print("\n\t\tMisère Red Blue NIM\n")
        print("Rules:\n• You can remove marble only from one row at a time.")
        print("• You can remove the number of marbles of your own choice but of same colour Red or Blue.")
        print("• Marble removed at last turn will give the score to winner Blue gives three points while Red gives two points.")
        print("• Remember, the player who removes the last marble will lose the game.")

        input("\nPlease Enter to Start .....")
        os.system("cls")
        Misere(state)
        while True:
            os.system("cls")
            print("\nDo you want to play more rounds or you want to exit:\n\n1)More\t\t2)Exit")
            em = input("\nWhat's your decision: ")
            if em == "1" or em.lower() == "more":
                break
            elif em == "2" or em.lower() == "exit":
                os.system("cls")
                print("\t\tFINAL SCORE")
                print(f"\nComputer: {comp_score}\t\tPlayer: {player_score}\n")
                sys.exit(0)
            else:
                print("Answer according to given options to continue!")
                continue

    else:
        print("Enter the right choice to play!")
        continue


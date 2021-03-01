# Coding utf-8
import getpass
import threading
import json
import random

# Load the words list file 
# To play in single mode - words.json -

# Default
fails = 6
Player = 1
tries = 7
wrong_words = []
remainings = {}
empty_spaces = {}
theword = {}

# Game options
game_options = {
    1: 'Single Player',
    2: 'Two Players',
    3: 'Close the game'
}

lose = """█▄█ █▀█ █░█   █░░ █▀█ █▀ █▀▀ █
░█░ █▄█ █▄█   █▄▄ █▄█ ▄█ ██▄ ▄"""

win = """█▄█ █▀█ █░█   █░█░█ █ █▄░█ █
░█░ █▄█ █▄█   ▀▄▀▄▀ █ █░▀█ ▄"""

# Drawing hangman
def draw_hangman(tries):
    hangman = [
        """
        ---------
        |       |
        O       |
                |
                |
                |
        -
        """,
        """
        ---------
        |       |
        O       |
        |       |
        |       |
                |
        -
        """,
        """
        ---------
        |       |
        O       |
       \\|       |
        |       |
                |
        -
        """,
        """
        ---------
        |       |
        O       |
       \\|/      |
        |       |
                |
        -
        """,
        """
        ---------
        |       |
        O       |
       \\|/      |
        |       |
       /        |
        -
        """,
        """
        ---------
        |       |
        O       |
       \\|/      |
        |       |
       / \\      |
        -
        """
    ]

    return hangman[tries]

def wrong_letters():
    if not wrong_words: 
            print('')
    else:
        i = 0
        print('\nWrong letters: ')
        for i in range(len(wrong_words)):
            print(wrong_words[i], end= ' ')
                
        print('\n\n||||| Hangman |||||')
        print(draw_hangman(i) + '\n' )
        
        for r, v in remainings.items():
            print(f'{r} times: {v}\n')

def correct_letters(letter):
    for k, v in theword.items():
        if v == letter or v.upper() == letter.upper():
            for i in empty_spaces:
                if k == i:
                    if letter.upper() == v:
                        empty_spaces[i] = letter.upper()
                    else:
                        empty_spaces[i] = letter
            
def hide_word(word):
    w = 0
    s = 0
    try:
        letters = len(word)
        spaces_letters = '_'
        for l in word:
            if l.isdigit():
                raise ValueError
            else:
                theword.update({w: l})
                w += 1
        while s < letters:
            empty_spaces.update({s: spaces_letters})
            s += 1
    except ValueError:
        print('The word must be only letters.')
        main()

def unhide_word():
    for i in empty_spaces.values():
        print(i, end=' ')

def play_again():  
    global fails
    q = input('\n\nDo yo want to play again? (Yes/No) ')
    if q == upperlowerstring('Yes'):
        fails = 6
        wrong_words.clear()
        main()
    else:
        if q == upperlowerstring('No'):
            quit()

# Upper or lower string
def upperlowerstring(letter):
    if letter.upper() in theword.values():
        l = letter.upper()
    else:
        l = letter.lower()
    return l

def player_mode(player):
    global fails

    while True:
        print('---------')
        print('The Word:')
        print('---------\n\n')
        unhide_word()
        guess_letters = input('\n\nThink of a letter: ')
        try: 
            if guess_letters.isdigit() or guess_letters == '':
                raise ValueError
            else:
                letter = upperlowerstring(guess_letters)
                if Player == 1:
                    if letter in theword.values():
                        print('Correct! Letter: ' + letter)
                        correct_letters(letter)
                        if empty_spaces == theword:
                            print(player)    
                            print(win)
                            print('the game.\n')
                            print('Congratulations! The word is:')
                            threading.Thread(target=unhide_word).start()
                            play_again()
                    else:
                        if tries > 0:
                            wrong_words.append(letter)
                        wrong = len(wrong_words)
                        if wrong > 0:
                            remaining = fails - 1
                            remainings.update({'Remaining': remaining})
                            fails -= 1
                            for i in range(len(wrong_words)):
                                if i == 5:
                                    print(player)
                                    print(lose)
                                    print('the game.')
                                    print('\nThe correct word was: ')
                                    for w in theword:
                                        # Correct word if you fail all letters
                                        print(theword[w], end = '')
                                    print('\nTry again!\n')
                                    threading.Thread(target=wrong_letters).start()
                                    play_again()
                else:
                    print('Just for fun!')
                wrong_letters()
        except ValueError:
            print('Make sure you\'re typing only letters.')

def main():

    print('******************************')
    print('Welcome to Hangman Game Python')
    print('*** Made by Luis Salamanca ***')
    print('******************************\n')

    # Display game options
    for n, d in game_options.items():
        print(f'{n}: {d}')

    option = input('\nSelect an option: ')

    try:
        if int(option) == 1:
            # Random word from a file
            word = ''
            # Single player mode
            player = input('Single Player name: ')
            # Loading the words list file
            try:
                # If the words list file has another name
                wordsfile = open('words.json')
                data = json.load(wordsfile)
                for i in data:
                    word = random.choice(data[i])
                hide_word(word)
                player_mode(player) 
            except FileNotFoundError:
                print('The file does not exist.')
 
        elif int(option) == 2:
            # Two player mode
            player1 = input('Name Player 1: ')
            player2 = input('Name Player 2: ')

            # Secrect word
            try:
                while True:
                    word = getpass.getpass(player1 + ' Write a simple word please: ')
                    try: 
                        if word.isdigit() or word == '':
                            raise ValueError
                        else:
                            hide_word(word)
                            player_mode(player2)
                    except ValueError:
                        print('Wrong value. Must be an string.')
            except EOFError:
                print('Invalid input.')
            except KeyboardInterrupt:
                print('The game was interrupted.')

        elif int(option) == 3:
            print('You quit the game. Bye Bye!')
            quit()

        else:
            print('Wrong option, select an option from the list.')
            main()

    except ValueError:
            print('Only accepts options from the list.')
            main()
    
if __name__ == '__main__':
    main()

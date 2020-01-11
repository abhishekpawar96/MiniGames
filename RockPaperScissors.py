import random

# TODO:
# "Scissors cuts paper, paper covers rock, rock crushes lizard, lizard poisons Spock, Spock smashes scissors,
# scissors decapitates lizard, lizard eats paper, paper disproves Spock, Spock vaporizes rock,
# and as it always has, rock crushes scissors."

while True:
    print("Make your choice")
    choice = str(input())
    choice = choice.lower()
    print("Your Choice is: ", choice)
    choices = ['rock', 'paper', 'scissors']
    computer_choice = random.choice(choices)
    print("Computer's Choice is: ", computer_choice)
    if choice in choices:
        if choice == computer_choice:
            print("It's a Tie!")
        if choice == 'rock':
            if computer_choice == 'paper':
                print('you lose, sorry :(')
            elif computer_choice == 'scissors':
                print('You win!!!!! congrats :)')
        if choice == 'paper':
            if computer_choice == 'scissors':
                print('you lose, sorry :(')
            elif computer_choice == 'rock':
                print('You win!!!!! congrats :)')
        if choice == 'scissors':
            if computer_choice == 'rock':
                print('you lose, sorry :(')
            elif computer_choice == 'paper':
                print('You win!!!!! congrats :)')
        else:
            print('invalid choice, try again')

        print()



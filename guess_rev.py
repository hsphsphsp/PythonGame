from random import randint

guessesTaken = 0

myName = input('Hello! What is your name?')

number = randint(1, 20)
print('Well,' + myName + ', I am thinking of a number between 1 and 20.')

while guessesTaken < 6:
    guess = int(input('Take a guess.'))
    guessesTaken += 1
    if guess < number:
        print('Your guess is too low.')
    elif guess > number:
        print('Your guess is too high.')
    else:
        break

if guess == number:
    print('Good job, ' + myName + '! You guessed my number in ' + str(guessesTaken) + ' guesses!')
else:
    print('Nope. The number I was thinking of was', number)

import os

def test_square():
    print("Square Main Test")
    # compile main
    os.system('python3 ./source/JackAnalyzer.py ./Square/Main.jack')
    # check main
    os.system('../../tools/TextComparer.sh ./res/Main.xml ./Square/Main.xml')

    print("Square Square Test")
    # compile square
    os.system('python3 ./source/JackAnalyzer.py ./Square/square.jack')
    # check square
    os.system('../../tools/TextComparer.sh ./res/Square.xml ./Square/Square.xml')

    print("Square SquareGame Test")
    # compile square_game
    os.system('python3 ./source/JackAnalyzer.py ./Square/SquareGame.jack')
    # check square_game
    os.system('../../tools/TextComparer.sh ./res/SquareGame.xml ./Square/SquareGame.xml')

test_square()

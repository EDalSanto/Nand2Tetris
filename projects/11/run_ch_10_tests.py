import os

def test_square():
    print("TEST SQUARE\n")

    print("MAIN")
    # compile main
    os.system('python3 ./source/JackCompiler.py ./Square10/Main.jack')
    # check main
    os.system('../../tools/TextComparer.sh ./compiled/Square10/Main.xml ./Square10/Main.xml')
    print("\n")

    print("SQUARE")
    # compile square
    os.system('python3 ./source/JackCompiler.py ./Square10/square.jack')
    # check square
    os.system('../../tools/TextComparer.sh ./compiled/Square10/Square.xml ./Square10/Square.xml')
    print("\n")

    print("SQUAREGAME")
    # compile square_game
    os.system('python3 ./source/JackCompiler.py ./Square10/SquareGame.jack')
    # check square_game
    os.system('../../tools/TextComparer.sh ./compiled/Square10/SquareGame.xml ./Square10/SquareGame.xml')

test_square()

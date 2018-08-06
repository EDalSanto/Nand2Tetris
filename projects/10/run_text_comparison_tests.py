import os

def test_square():
    print("TEST SQUARE\n")

    print("MAIN")
    # compile main
    os.system('python3 ./source/JackAnalyzer.py ./Square/Main.jack')
    # check main
    os.system('../../tools/TextComparer.sh ./compiled/Square/Main.xml ./Square/Main.xml')
    print("\n")

    print("SQUARE")
    # compile square
    os.system('python3 ./source/JackAnalyzer.py ./Square/square.jack')
    # check square
    os.system('../../tools/TextComparer.sh ./compiled/Square/Square.xml ./Square/Square.xml')
    print("\n")

    print("SQUAREGAME")
    # compile square_game
    os.system('python3 ./source/JackAnalyzer.py ./Square/SquareGame.jack')
    # check square_game
    os.system('../../tools/TextComparer.sh ./compiled/Square/SquareGame.xml ./Square/SquareGame.xml')

def test_array():
    print("TEST ARRAY\n")

    print("MAIN")
    # compile main
    os.system('python3 ./source/JackAnalyzer.py ./ArrayTest/Main.jack')
    # check main
    os.system('../../tools/TextComparer.sh ./compiled/ArrayTest/Main.xml ./ArrayTest/Main.xml')

test_square()
print("\n")
test_array()

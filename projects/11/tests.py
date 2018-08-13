import os

def test_seven():
    print("TESTING SEVEN\n")

    print("MAIN")
    # compile main
    os.system('python3 ./source/JackCompiler.py ./Seven/Main.jack')
    # check main
    os.system('../../tools/TextComparer.sh ./compiled/Seven/Main.vm ./expected/Seven/Main.vm')
    print("\n")

def test_square():
    print("TESTING SQUARE\n")

    print("MAIN")
    # compile main
    os.system('python3 ./source/JackCompiler.py ./Square/Main.jack')
    # check main
    os.system('../../tools/TextComparer.sh ./compiled/Seven/Main.vm ./expected/Seven/Main.vm')
    print("\n")

test_seven()
test_square()

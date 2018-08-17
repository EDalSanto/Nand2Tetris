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
    os.system('../../tools/TextComparer.sh ./compiled/Square/Main.vm ./expected/Square/Main.vm')
    #print("SQUARE")
    #os.system('python3 ./source/JackCompiler.py ./Square/Square.jack')
    #os.system('../../tools/TextComparer.sh ./compiled/Square/Square.vm ./expected/Square/Square.vm')
    #print("SQUAREGAME")
    #os.system('python3 ./source/JackCompiler.py ./Square/SquareGame.jack')
    #os.system('../../tools/TextComparer.sh ./compiled/Square/SquareGame.vm ./expected/Square/SquareGame.vm')


    print("\n")

def test_average():
    print("TESTING AVERAGE\n")

    print("MAIN")
    # compile main
    os.system('python3 ./source/JackCompiler.py ./Average/Main.jack')
    # check main
    os.system('../../tools/TextComparer.sh ./compiled/Average/Main.vm ./expected/Average/Main.vm')
    print("\n")

def test_complex_arrays():
    print("TESTING COMPLEX ARRAYS\n")

    print("MAIN")
    # compile main
    os.system('python3 ./source/JackCompiler.py ./ComplexArrays/Main.jack')
    # check main
    os.system('../../tools/TextComparer.sh ./compiled/ComplexArrays/Main.vm ./expected/ComplexArrays/Main.vm')
    print("\n")

def test_convert_to_bin():
    print("TESTING CONVERT TO BIN\n")

    print("MAIN")
    # compile main
    os.system('python3 ./source/JackCompiler.py ./ConvertToBin/Main.jack')
    # check main
    os.system('../../tools/TextComparer.sh ./compiled/ConvertToBin/Main.vm ./expected/ConvertToBin/Main.vm')
    print("\n")

test_seven()
test_square()
test_average()
test_convert_to_bin()
test_complex_arrays()

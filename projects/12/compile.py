import os

print("COMPILING MATH\n")
os.system('compiled=../../tools/JackCompiler.sh')
os.system("$compiled MathTest/*.jack")

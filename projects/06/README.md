# Assembler
* every computer has **binary machine language** of 1s and 0s and a **symbolic machine language, aka assembly language**

### Assembly Languages and Assemblers
* Assembler -> translates symbolic machine language to binary 0s and 1s; essentially "text-processing program"
  * usually **first software layer** in computer
  * **2 flavors of symbols** in general:
  ![SymbolResolution](./SymbolResolution)
    * Variables
      * automatically **assigned to memory addresses** by translator
        * actual values of these addresses is insignificant so long as each **symbol** is **resolved to the same address throughout the program's translation**
    * Labels
      * marking locations in program with symbols
      * i.e., label loop that a program can goto later conditionally or unconditionally
  * looks up symbols in symbol table with **symbols mapped to phsyical addresses in RAM**
  * **assembly command** may translate into **several machine instructions** and thus end up occupying **several memory locations**
    * assembler keeps **track** of **how many words** each source command generates
  * when **allocating memory space for variables**, translator must take into **account** both their **data type and the word width (i.e., 16 bits) of target hardware**
* instead of having to write program in Machine Language on Hack computer, can write program on our computers
  * **cross-compiler** -> program running on 1 computer **producing code for another computer**
* full documentation must be given of assembly syntax / api and respective binary codes

### Hack Assembly

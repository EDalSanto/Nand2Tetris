# Machine Language
* overview of computer from user's point of view before finishing building computer

##### Overview
![overview](https://camo.githubusercontent.com/135d2f3a0c3b6109edbeeee4f38bea42a7c7d481/687474703a2f2f6765656b72657365617263686c61622e6e65742f636f7572736572612f6e32742f6d616368696e652d6c616e672d312e6a7067)
* most machines only do 1 thing, i.e., a washing machine doesn't cook spaghetti
* universal turing machine -> same hardward can run many different software programs
* **machine language** enables **directly manipulating machine** and **highly specific optimizations** but not useful for most programmers
* Mnemonics
  * Machine language is really all binary, but too difficult for humans
  * Assembly Language makes much easier for humans to reason about manipulating machine
    * this "symbolic form" doesn't really exist but is just a convenient mnemonic to present machine language instructions to humans
    * assembler -> converts from assembly language to bits

##### Machine Language Elements
* Machine Language most important interface -> communication between software and hardware
  * designed to **manipulate** a **memory** using a **processor** and a set of **registers**
* Machines
  * Memory -> collection of hardware devices that store data and instructions in a computer
    * from a programmer's perspective, **all memories** have **same structure**: **continuous array of cells of some fixed width**, also called words or locations, each having a **unique address**
  * Processor -> usually known as Central Processing Unit, device capable of performing a fixed set of elementary options
    * arithmetic and logic operations, memory access operations, and control (branching)
    * operands are binary values that come from registers and selected memory locations
    * likewise, results of the operations (processor's output) can be stored in either registers or selected memory location
  * Registers
    * CPUs contain a few, easily accessed, "registers"
    * location in processor's immediate proximity enables high-speed data manipulation
    * number and functions are a central part of the architecture
      * **Data Registers** -> contain **values**
        * Add R1, R2
      * **Address Registers** -> contain **address** where to load a value
        * Store R1, @A

* Memory Hierarchy
![Memory Hierarchy](https://camo.githubusercontent.com/072f6d0db3b10401c17a03a24a7ad3c63989676e/687474703a2f2f6765656b72657365617263686c61622e6e65742f636f7572736572612f6e32742f6d616368696e652d6c616e672d352e6a7067)
  * **accessing memory** is **expensive**
    * need to supply long address to get value at memory location
    * then need to get the memory contents into CPU, which is expensive
  * **Solution** -> series of increasing memory sizes starting from Registers in CPU to Cache to Main Memory to Disk
    * at each level, distance from CPU, memory size, and overall performance time increases
  * Addressing Modes
    * Register
      * Add R1, R2 -> R2 + R1
    * Direct
      * Add R1, M[200] -> Mem[200] + R1
    * Indirect
      * Add R1, @A -> Mem[A] + R1
    * Immediate
      * Add 73, R1 -> R1 + 73
  * Input / Output
    * CPU needs some kind of protocol to talk to each of them
    * **Software "Drivers" know protocols to enable communication between input / output**
      * one general method of interaction uses "memory mapping"
        * Memory Location 12345 holds the direction of the last movement of the mouse
  * Flow Control -> loops

##### The Hack Computer and Machine Language
![hack](./HackComputer.png)
* 16-bit machine -> atomic unit of machine is 16 bits
  * everything consists of chunks of 16 bits
  * if you want to store / retrieve / move, etc. need to do it in units of 16 bits
  * CPU can only execute programs that reside in instruction memory (ROM)
    * program can be "pre-burned" with required program
    * **loading a new program** is done by **replacing entire ROM chip**, **similar to replacing a cartridge in a game console**
* Hack Machine Language
  * two 16-bit registers, D and A
    * D -> solely stores data values
    * A -> doubles as **both a data register and address register**, depending on instruction context
  * Hack instructions are 16 bits wides and addresses are specified with 15 bits -> impossible to pack both operations in one instruction
    * each instruction has symbolic and binary representation
    * every operation that involves memory location requires two Hack commands
      * address instruction, or A-Instruction
        * @value -> stores value in Register A
          * leading binary 0 tells computer this is an A instruction -> opt code
            * next 15 bits represent value
          * value is either a number or symbol representing a number
      * compute instruction, or C-Instruction
        ![CInstruction](./CInstruction.png)
        * dest = comp ; jump
    * memory access instructions operate on an implicit memory location labeled "M"
      * M -> always refers to the memory word whose address is the current value of the A register

##### Input / Output
![IO](./IO.png)
* Output
  * Screen memory map
    * designated memory area dedicated to manage a display unit
    * phsyical display is continuously **refreshed** from the memory map many times per second
    * output effect by writing code that manipulates the screen memory map ^^
      * write binary values to into memory segment associated with screen
* Input
  * phsyical keyboard associated with keyboard memory map in RAM
  * ASCII code sent to RAM[24576] and value read from their

##### Hack Programming
* use CPU emulator
* CPU will continue to evaluate instructions at memory locations beyond program end
  * end all programs in **infinite loop** to control memory locations that program operates on
* Hack is case sensitive
* Best Practices
  * Design the program using pseudo code
  * Translate to assembly
  * Test program on paper using a variable-value trace table
* variables that store memory addresses -> pointers
  * whenever we have to access memory using a pointer, we need an instruction like A=M
* **compiler** -> translate high level language, like C, to assembly
  * building compiler in 2nd part of course

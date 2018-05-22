// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// High-Level Algorithm
// load register to 0 for sum
// loop R1 times and add R0 to sum each time
// set R2 to sum either at end or throughout?

// Initialize sum
@0   // load 0 into A register
D=A  // set D to value of A address (0)
@sum // some register which will hold sum
M=D  // set value at this register to D (0)

// Initialize i for iteration
@1   // load 1 into A Register
D=A  // set D to value of A address (1)
@i   // sum register which hold i
M=D  // set value to to register D (1)

(LOOP)
  @i   // load register i
  D=M // set D to value at i
(END)

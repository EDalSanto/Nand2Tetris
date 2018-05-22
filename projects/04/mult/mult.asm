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
@R2  // R2 which will hold sum
M=D  // set value at this register to D (0)

// Initialize i for iteration
@1   // load 1 into A Register
D=A  // set D to value of A address (1)
@i   // sum register which hold i
M=D  // set value to to register D (1)

(LOOP)
  // Set up conditions
  @i     // load register i address to A
  D=M    // set D to value at i
  @R1    // load register 1 to A
  D=M-D  // D = value at R1 - i
  @END
  D;JLT  // if i > R1 (D < 0 specifically) end

  // Do an addition to R2
  @R0    // Load R0 value
  D=M    // Place in D
  @R2   // Load sum register
  M=D+M  // Add value at R0 which should be in D

  // increment i
  @i
  M=M+1

  // Jump back to top of LOOP
  @LOOP
  0;JMP
(END)
  @END
  0;JMP  // Infinite Loop

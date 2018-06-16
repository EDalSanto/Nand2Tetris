// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

@i
M=1 // initialize i to 1
@R2
M=0 // initialize sum to 0

(LOOP)
  // check if should jump to end
  @R1
  D=M     // load R1, number of times to iterate
  @i      // load current iteration
  D=D-M
  @END
  D;JLE // check if iterations over

  // add
  @R0
  D=M
  @R2
  M=D+M

  // inc i
  @i
  M=M+1
(END)
  @END
  0;JMP

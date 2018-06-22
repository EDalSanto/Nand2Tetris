@SP    // load top of stack
AM=M-1 // set address and address register to 1 less
D=M    // load y

@SP
AM=M-1 // get to x
D=M-D  // y - x -> diff result stored in D

// jump to 0
@NOT_EQUAL
D;JNE

// Equal
@SP
A=M
M=-1   // set to -1

// jump out of comparison
@OUT_COMP
0;JMP

// Not Equal
(NOT_EQUAL)
@SP
A=M
M=0

(OUT_COMP)
// increment stack pointer
@SP
M=M+1

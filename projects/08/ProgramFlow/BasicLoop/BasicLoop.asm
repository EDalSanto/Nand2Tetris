@0
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@R5
M=D
@1
D=M
@0
D=D+A
@R6
M=D
@R5
D=M
@R6
A=M
M=D
(LOOP_START)
@2
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
AM=M-1
M=M+D
@SP
M=M+1
@SP
AM=M-1
D=M
@R5
M=D
@1
D=M
@0
D=D+A
@R6
M=D
@R5
D=M
@R6
A=M
M=D
@2
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@SP
AM=M-1
M=M-D
@SP
M=M+1
@SP
AM=M-1
D=M
@R5
M=D
@2
D=M
@0
D=D+A
@R6
M=D
@R5
D=M
@R6
A=M
M=D
@2
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
AM=M-1
D=M
@LOOP_START
D;JNE
@1
D=M
@0
D=D+A
A=D
D=M
@SP
A=M
M=D
@SP
M=M+1

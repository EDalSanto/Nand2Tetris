@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@17
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
D=M-D
@NOT_eq.1
D;JNE
@SP
A=M
M=-1
@INC_STACK_POINTER_eq.1
0;JMP
(NOT_eq.1)
@SP
A=M
M=0
(INC_STACK_POINTER_eq.1)
@SP
M=M+1
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
@16
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
D=M-D
@NOT_eq.2
D;JNE
@SP
A=M
M=-1
@INC_STACK_POINTER_eq.2
0;JMP
(NOT_eq.2)
@SP
A=M
M=0
(INC_STACK_POINTER_eq.2)
@SP
M=M+1
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
@17
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
D=M-D
@NOT_eq.3
D;JNE
@SP
A=M
M=-1
@INC_STACK_POINTER_eq.3
0;JMP
(NOT_eq.3)
@SP
A=M
M=0
(INC_STACK_POINTER_eq.3)
@SP
M=M+1
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
@891
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
D=M-D
@NOT_lt.1
D;JGE
@SP
A=M
M=-1
@INC_STACK_POINTER_lt.1
0;JMP
(NOT_lt.1)
@SP
A=M
M=0
(INC_STACK_POINTER_lt.1)
@SP
M=M+1
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@892
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
D=M-D
@NOT_lt.2
D;JGE
@SP
A=M
M=-1
@INC_STACK_POINTER_lt.2
0;JMP
(NOT_lt.2)
@SP
A=M
M=0
(INC_STACK_POINTER_lt.2)
@SP
M=M+1
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
@891
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
D=M-D
@NOT_lt.3
D;JGE
@SP
A=M
M=-1
@INC_STACK_POINTER_lt.3
0;JMP
(NOT_lt.3)
@SP
A=M
M=0
(INC_STACK_POINTER_lt.3)
@SP
M=M+1
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
@32766
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
D=M-D
@NOT_gt.1
D;JLE
@SP
A=M
M=-1
@INC_STACK_POINTER_gt.1
0;JMP
(NOT_gt.1)
@SP
A=M
M=0
(INC_STACK_POINTER_gt.1)
@SP
M=M+1
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@32767
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
D=M-D
@NOT_gt.2
D;JLE
@SP
A=M
M=-1
@INC_STACK_POINTER_gt.2
0;JMP
(NOT_gt.2)
@SP
A=M
M=0
(INC_STACK_POINTER_gt.2)
@SP
M=M+1
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
@32766
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
D=M-D
@NOT_gt.3
D;JLE
@SP
A=M
M=-1
@INC_STACK_POINTER_gt.3
0;JMP
(NOT_gt.3)
@SP
A=M
M=0
(INC_STACK_POINTER_gt.3)
@SP
M=M+1
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
@53
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
M=M+D
@SP
M=M+1
@112
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
A=M-1
M=-M
@SP
AM=M-1
D=M
@SP
AM=M-1
M=M&D
@SP
M=M+1
@82
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
M=M|D
@SP
M=M+1
@SP
AM=M-1
D=M
M=!M
@SP
M=M+1

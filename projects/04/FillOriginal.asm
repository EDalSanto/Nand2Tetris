// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// Loop with no end..
// at each iteration, read from keyboard
  // if no key pressed (0?) darken screen by setting all screen bits to 0
  // else set all screen bits to 1


(LOOP)

@SCREEN // loads 16... into A
D=A     // D register holds it
@i      // load register i
M=D     // set register i to screen value

@KBD    // load keyboard input register into memory
D=M     // read value

// conditionally set screen to black or white loops
@WHITE
D;JEQ   // if keyboard input is 0, go to white
@BLACK
0;JMP   // else go to black

// set all bits to 1
(BLACK)
// set current address to value
@i
A=M
M=-1

// increment i by 1
@i
M=M+1
@i
// check where we are
D=M  // load current iteration value
@KBD // load screen value
D=A-D // once we reach address of kbd terminate this inner loop
@LOOP
D;JEQ    // Infinite Loop back to top
@BLACK   // else go back to black
0;JMP

// set all bits to 0
(WHITE)
// set current address to value
@i
A=M
M=0

// increment i by 1
@i
M=M+1
@i

// check where we are
D=M  // load current iteration value
@KBD // load screen value
D=A-D // once we reach address of kbd terminate this inner loop
@LOOP
D;JEQ    // Infinite Loop back to top
@WHITE   // else go back to black
0;JMP

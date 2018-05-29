/* Input1: text file named SomeProgram.asm containing Hack assembly program
 * Input2: name of output file of SomeProgram.asm containing Hack assembly program
 * Output: text file name SomeProgram.hack containing translated Hack Machine Code
 * */

/*** Assembler Without Symbols ***/
// main
  // for each line in input file
    // pass instruction to Parser
      /* Parse Module -> tokenize instruction components */
        // note: ignore whitespaces and comments
        // define helper functions which diagnose instruction
        /* main function logic */
        // initialize binary string that will be written to output file
        // if A command
          // add starting 0 for A command
          // set binary output string to decimal convert to binary
        // else C command
          /* Code Module */
            // define structs
              // dest
              // comp
                // note: multiple keys with same value
              // jump
          // add starting 1 for C command
          // pass comp token to a-bit / comp-bits translator; add to binary output
          // pass dest-bits to translator; add to binary output
          // pass jump-bits to translator; add to binary output
        // write binary string to output file

#include <stdio.h>
#include <string.h>

char *parse_line(char *line);

int main(void) {
  FILE *input_file_pointer;
  FILE *output_file_pointer;
  char *line = NULL;
  char *binary_string = NULL;
  size_t len = 0;
  ssize_t read;

  input_file_pointer = fopen("./add/Add.asm", "r");
  output_file_pointer = fopen("./add/Add.hack", "w");

  while ((read = getline(&line, &len, input_file_pointer)) != -1) {
    binary_string = parse_line(line);
    // write to file
    fputs(binary_string, output_file_pointer);

    printf("%s", line);
  }
  fclose(input_file_pointer);
  free(line);

  return 0;
}

char *parse_line(char *line) {
  char *res;
  // ignore whitespaces and comments
  if (line[0] == '/' || strlen(line) == 2) {
    printf("not to process");
  }
  res = "foobar";
  return res;

  /* main function logic */
  // initialize binary string that will be written to output file
  // if A command
    // add starting 0 for A command
    // set binary output string to decimal convert to binary
  // else C command
    /* Code Module */
      // define structs
        // dest
        // comp
          // note: multiple keys with same value
        // jump
    // add starting 1 for C command
    // pass comp token to a-bit / comp-bits translator; add to binary output
    // pass dest-bits to translator; add to binary output
    // pass jump-bits to translator; add to binary output
  // write binary string to output file
}

/*** Assembler With Symbols ***/

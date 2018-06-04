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
#include <stdlib.h>

char *parse_line(char *line);

int main(void) {
  FILE *input_file_pointer;
  FILE *output_file_pointer;
  char *line = NULL;
  char *binary_string = NULL;
  size_t len = 0;
  ssize_t read = 0;
  ssize_t next_read = 0;

  input_file_pointer = fopen("./add/Add.asm", "r");
  output_file_pointer = fopen("./add/Add.hack", "w");

  getline(&line, &len, input_file_pointer);
  while (next_read != -1) {
    binary_string = parse_line(line);
    next_read = getline(&line, &len, input_file_pointer);

    if (strlen(binary_string) == 0) { continue; }

    if (next_read != -1) { strcat(binary_string, "\n"); }

    fputs(binary_string, output_file_pointer);
  }
  fclose(input_file_pointer);
  free(line);
  free(binary_string);

  return 0;
}

/* Function to reverse string from start to end*/
void reverse_string(char *string, int start, int end)
{
  while (start < end)
  {
      char temp = string[start];
      string[start] = string[end];
      string[end] = temp;
      start++;
      end--;
  }
}

// function to convert decimal to binary
char *dec_to_binary(int n)
{
  // array to store binary number
  char *binary_str;
  binary_str = (char*)malloc(17);
  memset(binary_str, '\0', 17);

  // counter for binary array
  int i = 0;
  while (n > 0) {

      // storing remainder in binary array
      binary_str[i] = (n % 2) + 48;
      n = n / 2;
      i++;
  }

  binary_str[i] = '\0';

  /* pad with zeros */
  char *z = "0";
  while (strlen(binary_str) < 15) {
    strcat(binary_str, z);
  }

  reverse_string(binary_str, 0, 14);

  return binary_str;
}

char *parse_line(char *line) {
  /* each output is no more than 16 bits */
  char *res = (char*)malloc(18);
  memset(res, '\0', 18);

  char *binary;

  // ignore whitespaces and comments
  if (line[0] == '/' || strlen(line) == 2) {
    //printf("not to process\n");
  }

  // if A command
  if (line[0] == '@') {
    binary = dec_to_binary(atoi(line + 1));
    strcpy(res, binary);
    free(binary);
  }
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
  return res;
}

/*** Assembler With Symbols ***/

# Boolean Arithmetic and ALU

##### Roadmap
* build family of adders -> chips designed to add numbers
* build Arithmetic Logic Unit -> **Computer's calculating brain**, designed to perform a whole set of arithmetic and logical operations
  * ALU will be centerpiece for chip for computer's Central Processing Unit

* [Why computers use Binary?](https://www.youtube.com/watch?v=1sWCBgGALXE)
  * problem of sending signals between locations..
  * headphones send sound waves converted to volts
    * high variability causes air to vibrate more quickly which causes louder volume
    * known as analog symbol
  * with computers, we need a way to consistently add numbers
    * we could use analog volts again but large numbers would fry circuitry, as well be subject to imprecision (which is incredibly important for computers)
    * if we represent digits by sending in volts in a range, we can avoid the above problems
      * volts get sent in range which represents digit
      * using binary gives us largest range while maintaining ability to represent different values
        * **binary gives us most room for error in chaotic real world**
      * **downside** -> we need to use **more digits** with binary (3.332 times decimal)
    * seperateness, choice, begins at 2

##### Binary Numbers
* convert binary to decimal -> sum up 2^k for each kth digit from the right
* convert decimal to binary -> list out powers of 2 less than number, pick all numbers needed to sum up to number, pick 1 where number user, else 0

##### Binary Addition
* similar to decimal addition
* Overflow -> left-most bits carry over outside of word size
  * modern computers ignore this so sum of calculation will not add up properly in this case

##### Negative Numbers
* use 2's complement to represent negative number
  * when applied to n-bit numbers, x + (-x) always sums up to 2^n (i.e., 1 followed by n 0's)
  * properties
    * can code a total of 2^n signed numbers, with maximal and minimal respectively 2^(n-1) and -2^(n - 1) respectively
    * codes of all positive numbers begin with a 0
    * codes of all negative numbers begin with a 1
  * computing -x
    * idea: 2^n - x = ((2^n - 1) - x) + 1
    * hardware: flip all the bits of x and add 1 to result
  * can add signed numbers with simple bitwise addition and result will be represented correctly
    * thus, subtraction can be easily handled by converting x - y to x + (-y)
* add 1 to number -> flip bits from right to left until flipped 0 to 1

##### Arithmetic Logic Unit
* ALU -> executes all the arithmetic and logical operations performed by the computer
* Which operations should the ALU perform? -> hardware / software tradeoff; can add some functionality at either layer
* Hack ALU
  * 2 16-bit inputs, series of 6 control input bits, 2 control output bits, 1 16-bit output
  * 6 control bits enable in theory 2^6 number of functions that could be done

##### Perspective
* all of the chips are pretty standard but ALU is pretty simplified
* Why not include multiplication and division in ALU?
  * when building computer system, functionality is divided between hardward and operating system that runs on top of it
  * designer's freedom to decide
  * hardware will be faster but cost more -> matter of tradeoffs
* Carry look ahead -> more optimized adder then chaining carry to next fulladder
  * [vid](https://www.youtube.com/watch?v=6Z1WikEWxH0) -> able to dervie formula so that once solved first carry can compute subsequent ones
* [How does electricity become computer logic](https://www.quora.com/How-do-computers-work-the-way-they-do-When-does-electricity-become-executable-logic-and-how)

# Boolean Arithmetic and ALU

##### Roadmap
* build family of adders -> chips designed to add numbers
* build Arithmetic Logic Unit -> Computer's calculating brain, designed to perform a whole set of arithmetic and logical operations
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

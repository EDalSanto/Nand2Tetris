# Memory

##### Roadmap
* turn to computer's main memory unit -> Random Access Memory
* done gradually, bottom-up, from elementary flip-flop gates to one-bit registers to n-bit registers to a family of RAM chips
* unlike **computer's processing chips**, which are based on **combinational logic**, computer's memory logic requires clock-based sequential logic

##### Sequential Logic
* in most computers, passage of time represented by a master clock that delivers a continous train of alternating signals
  * exact hardware implementation usually based on oscillator that alternates continuously between two phases, i.e., 0 / 1
* time broken up into **discrete time units in computer**

##### Flip Flops
* need to be able remember 1 piece of information to pass from time t-1 to time t
* not just dependent on current input but internal to chip
* Data Flip Flop -> interface consists of single-bit data input and single-bit data output
  * includes clock input that continuously changes according to the master clock's signal
  * **outputs the input value from previous time unit**
    * at every time point, having previous signal fed to input shifted 1 time unit to the right
    * whereas **previous chips** all **only** depended on **current input**, this chip depends on past input / state
      * logical dependency on time
  * will build all sequential logic gates on DFF
* 1-Bit Register
  * takes input bit and load bit and outputs bit
  * load bit tells the register to "load the input bit" at time t-1 to be output at time t
  * makes use of mux and dff

##### Memory Units
* Von Neuman Architecture
  * Memory -> can mean many different things
    * Main Memory -> RAM, ...
      * actually **hardwired into computer motherboard**
    * Secondary Memory -> hard disks, memory sticks, ...
    * Volatile / non-Volatile
      * **Volatile** -> like RAM, which is **lost immediately** when turn **computer off**
      * **Non-Volatile** -> like flask disk, which **persists** even when computer shut off
  * Perspective
    * Physical -> implementation of how we build memory
    * Logical
      * always focus more on logical in this course
  * **Register** -> **most basic memory element**
    * with 1-bit register, can put many together to make n-bit register
    * width (w) -> 16-bit, 32-bit, or 64-bit
    * **state** -> the **value** which is **currently stored**
    * read operation -> prob out, which emits the Register's state
    * write operation -> set in to V, set load to 1
      * register's state will become V
      * from the next cycle onward will emit V
    * **takes complete cycle for register to stabilize and emit new state**
  * **RAM abstraction** -> holds data and instructions on which our programs operate
    * a **sequence** of **n addressable registers** with addresses from 0 to n-1
    * at any given point in time, only 1 register in RAM is selected
    * read Register i -> set address of RAM to i and out emits the state of Register i
      * potentially millions of registers in RAM device
    * write Register i -> set address again and do same work as done with individual register
    * **Why called "Random Access Memory"?** -> irrespective of the RAM size, **every register can be accessed and operated on at the same time instantaneously**
      * enter address -> **constant lookup like with array**

##### Counters
* counter -> sequential chip whose state is an integer number that **increments every time unit**
  * out(t) = out(t - 1) + c (where c is usually 1)
  * like register with control bits
  * typical CPU includes a **program counter** whose **output** is interpreted as the **address of the instruction that should be executed next in the current program**
  * probably needs to be able to reset to beginining (count to zero), load a new counting base (GOTO)

##### Time Matters
* **sequential chips** always consist of a layer of **DFFs sandwiched between optional combinational logic layers**
  * outputs change only at the point of transition from one clock cycle to the next, and not within the clock cycle itself
    * this "discretization" of the sequential chips' outputs has side effect of enabling the synchronization of the overall computer architecture
      * i.e., one of ALU inputs may take more time to arrive but doesn't matter since output always fed into sequential chip
      * just have to be sure that the length of clock cycle will be slightly longer than the time for a bit to travel the longest distance from one chip in the architecture to another

##### Perspective
* **flip-flops** can be created from **NAND gates in a loop**
* ROM -> Read-Only, non-volatile memory used when computer boots
  * boot -> loads from disk instructions for OS
* flash memory -> good things of both RAM and ROM
* tradeoffs in building computer
  * have very large, inexpensive memory with data that is only rarely used
  * have small, expensive memoery with data that is often used by processor -> caches like discussed in LL with ruby hashes
    * as caches get smaller, they get closer to the processor and more expensive

##### Clocks deeper dive
* [Clocks for Software Engineers](http://zipcpu.com/blog/2017/09/18/clocks-for-sw-engineers.html)
  * Lesson #1: **Hardware Design is Parallel Design**
    * things don't take place serially, one instruction after another, like normally in software
    * good example is thinking about **loop in software vs hardware**
      * [software loop](http://zipcpu.com/img/sw-loop.svg)
      * [hardware loop](http://zipcpu.com/img/hw-loop.svg)
        * every **iteration runs in parallel** -> loop iterations can't necessarily depend upon the output of prior loop iterations like in software
  * Why the clock is important?
    * everything takes time in hardware even for simple operations like reordering wires or moving the logic from one chip to another
    * clock speed is limited by amount of time to accomplish whatever logic you place between clocks
    * speed of the fastest operation limited by the clock speed required to accomplish slowest operation

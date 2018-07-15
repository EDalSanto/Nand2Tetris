# High-Level Language

### Overview
* getting high-level overview of Jack in this module to later write compiler and OS in Jack
* Jack Program collection of one more classes, one of which must be called Main
  * must have at least one function named main
  * Main.main => program's entry point

### Object-Based Programming
![ObjectProgrammingRecap](./images/ObjectProgrammingRecap.png)
* constructor => method designed to create new objects
  * must return the base address of the new object
    * Java does this implicitly must be explicit in Jack
* Object Representation
  * compiled constructor's code includes OS calls that store the new memory object
  ![ObjectRepresentation](./images/ObjectRepresentation.png)

### List Processing
* ![List](./images/ListProcessing.png)
  * the atom null, or
  * an atom followed by a list
* this => special variable that points to current object
![ListRepresentation](./images/ListRepresentation.png)

### Jack Language Specification
* arrays and objects can be easily converted back and forth between one another because under the hood they are treated very similiarly
* ![JackDataTypes](./images/JackDataTypes.png)
* ![JackClasses](./images/JackClasses.png)
  * ![JacksStandardClassOS](./images/JacksStandardClassOS.png)
* ![SubRoutines](./images/SubRoutines.png)
  * functions -> don't understand what objects are and just perform some computational services
* ![JackPecularities](./images/JackPecularities.png)

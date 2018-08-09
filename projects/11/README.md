# Compiler 2: Code Generation

### Overview
![CompilerDevelopmentRoadMap](./images/CompilerDevelopmentRoadMap.png)
* in Jack, like in Java and C#, **classes are standalone compilation units**

### Handling Variables
![VarSymbolTable](./images/VarSymbolTables.png)
* use symbol tables at subroutine and class levels to keep track of variables
  * can reset for each class and subroutine
![VarSymbolTablesUsage](./images/VarSymbolTablesUsage)
* **methods** of a class, in any language, **always pass current object / instance as first argument when invoked**
![HandlingNestedScope](./images/HandlingNestedScope.png)
* current scope hides all the other scopes behind it
  * in Jack, we only have two scope levels: class and subroutine

### Handling Expressions
![ParseTree](./images/ParseTree.png)
* all source languages use infix notation whereas vm code is postfix -> compile needs to make this translation
  ![DFSCodeGeneration](./images/DFSCodeGeneration.png)
  * depth-first tree traversal can be used to make translation
  * will use recursive one-stage approach
  ![RecursiveCodeGeneration](./images/RecursiveCodeGeneration.png)
![XMLtoVMCode](./images/XMLtoVMCode.png)
![OperatorPriority](./images/OperatorPriority.png)

### Handling Flow of Control
* make use of if-goto and labels in vm code
![CompileIf](./images/CompilingIf.png)
![CompileWhile](./images/CompilingWhile.png)

### Handling Objects: Low-Level Aspects
* Challenge of translating from high-level language to VM to Machine Code
* Memory Segments Refresher
  * need to write compiler that writes VM code
  * always use push / pop and the segment you want
  * VM code deals with host RAM
    * first 5 positions are pointers to designated segments in RAM
    * currently executing VM function has own stack frame with
    * Global Stack -> maintains currently executing function and its stacks as well other functions as they wait for the currently executing one to terminate
  ![LocalArgumentVariables](./images/LocalArgumentVariables.png)
  ![ObjectArrayData](./images/ObjectArrayData.png)
  ![AccessingRamData](./images/AccessingRamData.png)


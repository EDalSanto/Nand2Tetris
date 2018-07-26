# Compiler 1: Syntax Analysis

### Overview
![CompilerDevelopmentRoadMap](./images/CompilerDevelopmentRoadMap.png)
* process of translation from high-level to low-level consists two independent stages: syntax analysis and code generation
  * syntax analysis sub-stages
    * lexical analysis, or *tokenizing*
    * parsing
* Jack Analyzer -> program that unveils the syntax of the Jack program without generating executable code
  * result of syntax analysis

### Syntax Analysis
![Tokenizing](./images/Tokenizing.png)
![JackTokenizer](./images/JackTokenizer.png)

### Grammar
* program must abide by established grammar of compiler
![JackGrammar](./images/JackGrammar.png)

### Parse Tree
![ParseTreeJack](./images/ParseTreeJack.png)
* parse tree -> recursive data type, where values may contain other values of the same type
![ParseTreeJackExpression](./images/ParseTreeJackExpression.png)

### Parser Logic
![ParsingLogic](./images/ParsingLogic.png)
* non-terminals -> higher-level syntactic structure composed of terminals, or words, i.e., while, {}, etc.
![LLGrammar](./images/LLGrammar.png)
* programming languages much easier to parse than natural languages because only need to look ahead 1 token to understand current token, whereas in a language like English it may be 5-7 tokens

### The Jack Grammar
![LexicalElements](./images/LexicalElements.png)
![ProgramStructure](./images/ProgramStructure.png)
![ParsingExpressions](./images/ParsingExpressions.png)

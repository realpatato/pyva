#############
# CONSTANTS #
#############

DIGITS = "0123456789"

##########
# ERRORS #
##########

class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f"{self.error_name}: {self.details} "
        result += f"File {self.pos_start.file_name}, line {self.pos_start.ln + 1}"
        return result
    
class IllegalCharError(Error):
    def __init__(self,  pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Illegal Character Error", details)

############
# POSITION #
############

class Position:
    def __init__(self, index, ln, col, file_name, file_text):
        self.index = index
        self.ln = ln
        self.col = col
        self.file_name = file_name
        self.file_text = file_text
    
    def advance(self, current_char):
        self.index += 1
        self.col += 1

        if current_char == "\n":
            self.ln += 1
            self.col = 0
        
        return self
    
    def copy(self):
        return Position(self.index, self.ln, self.col, self.file_name, self.file_text)

##########
# TOKENS #
##########

TT_INT    = "INT"
TT_FLOAT  = "FLOAT"
TT_PLUS   = "PLUS"
TT_MINUS  = "MINUS"
TT_MUL    = "MUL"
TT_DIV    = "DIV"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"

class Token:
    def __init__(self, type_, value = None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value:
            return f"{self.type}:{self.value}"
        return f'{self.type}'
    
#########
# LEXER #
#########

class Lexer:
    def __init__(self, file_name, text):
        self.file_name = file_name
        self.text = text
        self.pos = Position(-1, 0, -1, file_name, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        if self.pos.index < len(self.text):
            self.current_char = self.text[self.pos.index]
        else:
            self.current_char = None

    def make_tokens(self):
        tokens = []
        while self.current_char != None:
            if self.current_char in " \t":
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(Token(self.make_number()))
            elif self.current_char == "+":
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == "-":
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == "*":
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == "/":
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == "(":
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Token(TT_RPAREN))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, f"\"{char}\"")
        return tokens, None
    
    def make_number(self):
        num_str = ""
        dot_count = 0

        while (self.current_char != None) and (self.current_char in (DIGITS + ".")):
            if self.current_char == ".":
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += "."
            else: 
                num_str += self.current_char
            self.advance()
        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        else:
            return Token(TT_FLOAT, float(num_str))
        
#########
# NODES #
#########

class NumberNode:
    def __init__(self, token):
        self.token = token
    
    def __repr__(self):
        return f"{self.token}"

class BinaryOperationNode:
    def __init__(self, left_node, operator_token, right_node):
        self.left_node = left_node
        self.operator_token = operator_token
        self.right_node = right_node
    
    def __repr__(self):
        return f"({self.left_node}, {self.operator_token}, {self.right_node})"

##########
# PARSER #
##########

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = 1
        self.advance()
    
    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token

    def factor(self):
        token = self.current_token()
        if token.type in (TT_INT, TT_FLOAT):
            self.advance()
            return NumberNode(token)

    def term(self):
        pass

    def expression(self):
        pass

####### 
# RUN #
#######

def run(file_name, text):
    lexer = Lexer(file_name, text)
    tokens, error = lexer.make_tokens()

    return tokens, error
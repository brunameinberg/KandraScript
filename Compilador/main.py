import sys
from string import *
from math import *
from re import *
from abc import ABC, abstractmethod
from typing import List

class PrePro:
    @staticmethod
    def filter(file_name: str) -> str:
        with open(file_name, 'r', encoding='utf-8') as file:
            source = file.read()

        # Remove comentários do tipo /* comentário */
        source_sem_comentarios = PrePro.remover_comentarios(source)

        return source_sem_comentarios
    
    @staticmethod
    def remover_comentarios(source: str) -> str:
        result = []
        comentario = False
        achei_fim = False
        tem_comentario = False
        i = 0

        while i < len(source):
            if not comentario:
                if source[i:i+2] == '/*':
                    tem_comentario = True
                    comentario = True
                    i += 2
                else:
                    result.append(source[i])
                    i += 1
            else:
                if source[i:i+2] == '*/':
                    comentario = False
                    i += 2
                    achei_fim = True
                else:
                    i += 1
        
        if tem_comentario and not(achei_fim):
            raise ValueError("Comentário aberto")

        return ''.join(result)

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def get(self, name: str):
        if name in self.symbols:
            return self.symbols[name]
        else:
            raise KeyError(f"Variável '{name}' não encontrada")
    
    def assign (self, name, value, var_type):
        if self.symbols[name][1] != var_type:
            raise Exception(f"O tipo da variável declarado {self.symbols[name][1]} não é o mesmo tipo do valor a ser atribuido {var_type}")
        self.symbols[name][0] = value

    def set(self, name, value, type):
        self.symbols[name] = [value, type]


class FuncTable:
    table = {}

    def get(name: str):
        if name in FuncTable.table:
            return FuncTable.table[name]
        else:
            raise KeyError(f"Variável '{name}' não encontrada")
    
    def assign (self, name, value, var_type):
        if FuncTable.table[name][1] != var_type:
            raise Exception(f"O tipo da variável declarado {FuncTable.table[name][1]} não é o mesmo tipo do valor a ser atribuido {var_type}")
        FuncTable.table[name][0] = value

    def set(name: str, value: int, type: str):
        if name not in FuncTable.table:
            FuncTable.table[name] = [value, type]
        else:
            raise Exception(f"Uma função com o nome {name} foi declarada anteriormente.")


class Token:
    def __init__(self, type: str, value: any):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.next = None
        self.selectNext()
    
    def selectNext(self):
        while self.position < len(self.source) and self.source[self.position].isspace():
            self.position += 1

        if self.position >= len(self.source):
            self.next = Token('EOF', None)
            return

        if self.source[self.position].isdigit():
            comeco = self.position
            while self.position < len(self.source) and self.source[self.position].isdigit():
                self.position += 1
            valor = int(self.source[comeco:self.position])
            self.next = Token('INT', valor)

        # Strings
        elif self.source[self.position] == '"':
            self.position += 1  # Avança para o próximo caractere depois da aspas
            comeco = self.position
            while self.position < len(self.source) and self.source[self.position] != '"':
                self.position += 1
            if self.position >= len(self.source):
                raise Exception("String não terminada")
            valor = self.source[comeco:self.position]
            self.position += 1  # Avança para o próximo caractere após a segunda aspas
            self.next = Token('STRING', valor)
        
        #palavras reservadas
        elif self.source[self.position:self.position + 6] == "printf":
            self.next = Token('PRINTF', None)
            self.position += 6

        elif self.source[self.position:self.position + 2] == "if":
            self.next = Token('IF', None)
            self.position += 2

        elif self.source[self.position:self.position + 4] == "else":
            self.next = Token('ELSE', None)
            self.position += 4

        elif self.source[self.position:self.position + 5] == "while":
            self.next = Token('WHILE', None)
            self.position += 5

        elif self.source[self.position:self.position + 5] == "scanf":
            self.next = Token('SCANF', None)
            self.position += 5

        elif self.source[self.position:self.position + 3] == "int":
            self.next = Token('INTEIRO', None)
            self.position += 3
        
        elif self.source[self.position:self.position + 3] == "str":
            self.next = Token('STR', None)
            self.position += 3

        elif self.source[self.position:self.position + 6] == "return":
            self.next = Token('RETURN', None)
            self.position += 6
        
        elif self.source[self.position:self.position + 4] == "void":
            self.next = Token('VOID', None)
            self.position += 4

        elif self.source[self.position:self.position + 9] == "character":
            self.next = Token('PERSONAGEM', None)
            self.position += 9
        
        elif self.source[self.position:self.position + 10] == "attributes":
            self.next = Token('ATRIBUTOS', None)
            self.position += 10

        elif self.source[self.position:self.position + 8] == "strength":
            self.next = Token('FORÇA', None)
            self.position += 8

        elif self.source[self.position:self.position + 5] == "magic":
            self.next = Token('MAGIA', None)
            self.position += 5

        elif self.source[self.position:self.position + 4] == "mana":
            self.next = Token('MANA', None)
            self.position += 4

        elif self.source[self.position:self.position + 9] == "inventory":
            self.next = Token('INVENTARIO', None)
            self.position += 9      

        elif self.source[self.position:self.position + 5] == "spell":
            self.next = Token('FEITICO', None)
            self.position += 5

        elif self.source[self.position:self.position + 5] == "power":
            self.next = Token('PODER', None)
            self.position += 5

        elif self.source[self.position:self.position + 9] == "mana_cost":
            self.next = Token('CUSTO_MANA', None)
            self.position += 9

        elif self.source[self.position:self.position + 6] == "effect":
            self.next = Token('EFEITO', None)
            self.position += 6

        elif self.source[self.position:self.position + 7] == "mission":
            self.next = Token('MISSAO', None)
            self.position += 7

        elif self.source[self.position:self.position + 9] == "objective":
            self.next = Token('OBJETIVO', None)
            self.position += 9

        elif self.source[self.position:self.position + 12] == "participants":
            self.next = Token('PARTICIPANTES', None)
            self.position += 12

        elif self.source[self.position:self.position + 6] == "reward":
            self.next = Token('RECOMPENSA', None)
            self.position += 6

        elif self.source[self.position:self.position + 8] == "location":
            self.next = Token('LOCALIZACAO', None)
            self.position += 8

        elif self.source[self.position:self.position + 6] == "CREATE":
            self.next = Token('CREATE', None)
            self.position += 6

        elif self.source[self.position:self.position + 4] == "CAST":
            self.next = Token('CAST', None)
            self.position += 4

        elif self.source[self.position:self.position + 13] == "ENCHANTED_IF":
            self.next = Token('ENCHANTED_IF', None)
            self.position += 13

        elif self.source[self.position:self.position + 19] == "WHILE_THE_MOON_SHINES":
            self.next = Token('WHILE_THE_MOON_SHINES', None)
            self.position += 19

        elif self.source[self.position:self.position + 22] == "UNTIL_THE_FINAL_BATTLE":
            self.next = Token('UNTIL_THE_FINAL_BATTLE', None)
            self.position += 22
            
        #operadores lógicos
        elif self.source[self.position:self.position + 2] == '&&':
                    self.next = Token('AND', None)
                    self.position += 2

        elif self.source[self.position:self.position + 2] == '||':
                    self.next = Token('OR', None)
                    self.position += 2

        elif self.source[self.position:self.position + 2] == '==':
                    self.next = Token('EQUALS', None)
                    self.position += 2

        elif self.source[self.position] == ">":
            self.next = Token('GREATER', None)
            self.position += 1

        elif self.source[self.position] == "<":
            self.next = Token('MINOR', None)
            self.position += 1
        
        #resto
        elif self.source[self.position] == "+":
            self.next = Token('PLUS', None)
            self.position += 1
        
        elif self.source[self.position] == "-":
            self.next = Token('MINUS',None)
            self.position += 1

        elif self.source[self.position] == "*":
            self.next = Token('MULT',None)
            self.position += 1

        elif self.source[self.position] == "/":
            self.next = Token('DIV',None)
            self.position += 1
        
        elif self.source[self.position] == "=":
            self.next = Token('EQUAL', None)
            self.position += 1

        elif self.source[self.position] == "!":
            self.next = Token('NOT', None)
            self.position += 1
        
        elif self.source[self.position] == ";":
            # Ignora múltiplos pontos e vírgulas seguidos
            while self.position < len(self.source) and self.source[self.position] == ";":
                self.position += 1
            self.next = Token('SEMICOLON', None)
        
        elif self.source[self.position] == "(":
            self.next = Token('OPPAR',None)
            self.position += 1

        elif self.source[self.position] == ")":
            self.next = Token('CLPAR',None)
            self.position += 1

        elif self.source[self.position] == "{":
            self.next = Token('OPBRACE', None)
            self.position += 1

        elif self.source[self.position] == "}":
            self.next = Token('CLBRACE', None)
            self.position += 1

        elif self.source[self.position] == ",":
            self.next = Token('COMMA', None)
            self.position += 1

        elif self.source[self.position].isalpha() or self.source[self.position] == "_":
            comeco = self.position
            while (self.position < len(self.source) and 
                   (self.source[self.position].isalnum() or self.source[self.position] == "_")):
                self.position += 1
            valor = self.source[comeco:self.position]
            self.next = Token('IDENT', valor)
        
        else:
            raise Exception(f"Caracter inválido: {self.source[self.position]}")

class Node(ABC):
    def __init__(self, value: any):
        self.value = value
        self.children: List[Node] = []

    @abstractmethod
    def Evaluate(self, symbol_table: SymbolTable) -> any:
        pass


class IntVal(Node):
    def __init__(self, value: any):
        super().__init__(value)
    
    def Evaluate(self, symbol_table: SymbolTable) -> int:
        return (int(self.value), "int")
    
class StringVal(Node):
    def __init__(self, value):
        super().__init__(value)
    
    def Evaluate(self, symbol_table: SymbolTable) -> str:
        return (str(self.value), "str")
    
class NoOp(Node):
    def __init__(self):
        super().__init__(None)

    def Evaluate(self, symbol_table: SymbolTable) -> None:
        return None, None


class If(Node):
    def __init__(self, cond: Node, if_block:Node, else_block: Node = None):
        super().__init__('if')
        self.children.extend([cond, if_block])
        if else_block:
            self.children.append(else_block)

    def Evaluate(self, symbol_table: SymbolTable):
        cond_value, cond_type = self.children[0].Evaluate(symbol_table)
        if cond_value:
            return self.children[1].Evaluate(symbol_table)
        elif len(self.children) == 3:
            return self.children[2].Evaluate(symbol_table)
        return None, None

class While(Node):
    def __init__(self, cond: Node, block:Node):
        super().__init__('while')
        self.children.extend([cond, block])

    def Evaluate(self, symbol_table: SymbolTable):

        cond_value, cond_type = self.children[0].Evaluate(symbol_table)

        while cond_value:
            self.children[1].Evaluate(symbol_table)
            cond_value, cond_type = self.children[0].Evaluate(symbol_table)
        return None, None
    
class Scanf(Node):
    def __init__(self):
        super().__init__('scanf')

    def Evaluate(self, symbol_table: SymbolTable):
        valor = int(input())
        return (valor, "int")
    
class RelationOp(Node):
    def __init__(self, value: str, esq: Node, dir: Node):
        super().__init__(value)
        self.children.extend([esq, dir])

    def Evaluate(self, symbol_table: SymbolTable) -> any:
        valor_esquerdo, tipo_esquerdo = self.children[0].Evaluate(symbol_table)
        valor_direito, tipo_direito = self.children[1].Evaluate(symbol_table)

        if tipo_esquerdo != tipo_direito:
            raise Exception("Para operações relacionais os tipos devem ser iguais!")

        if self.value == '<':
            return int(valor_esquerdo < valor_direito), "int"
        elif self.value == '>':
            return int(valor_esquerdo > valor_direito), "int"
        elif self.value == '==':
            return int(valor_esquerdo == valor_direito), "int"
        else:
            raise Exception("Operador relacional não reconhecido")
    
class UnOp(Node):
    def __init__(self, value: str, child: Node):
        super().__init__(value)
        self.children.append(child)

    def Evaluate(self, symbol_table: SymbolTable) -> any:
        valor_filho, tipo_filho = self.children[0].Evaluate(symbol_table)

        if tipo_filho != "int":
            raise Exception(f"Tipo não suportado para a operação {self.value}.")

        if self.value == '-':
            return (-int(valor_filho), "int")
        
        elif self.value == '+':
            return (int(valor_filho), "int")
        
        elif self.value == '!':
            return (int(not(valor_filho)), "int")
        
        else:
            raise ValueError("Operação unária não suportada!")

class BinOp(Node):
    def __init__(self, value: str, esq: Node, dir: Node):
        super().__init__(value)
        self.children.extend([esq, dir]) 
    
    def Evaluate(self, symbol_table: SymbolTable) -> any:
        valor_esq, tipo_esq = self.children[0].Evaluate(symbol_table)
        valor_dir, tipo_dir = self.children[1].Evaluate(symbol_table)

        if ((tipo_dir == "str") or (tipo_esq == "str")):
            if self.value == '+':
                return (str(str(valor_esq) + str(valor_dir)), "str")
            else:
                raise ValueError(f"O tipo string não é suportado para o tipo de operação {self.value}")

        if self.value == '+':
            return (int(valor_esq + valor_dir), "int")
        elif self.value == '-':
            return (int(valor_esq - valor_dir), "int")
        elif self.value == '*':
            return (int(valor_esq * valor_dir), "int")
        elif self.value == '/':
            if valor_dir == 0:
                raise ZeroDivisionError("Divisão por zero")
            return (int(valor_esq / valor_dir), "int")
        elif self.value == '&&':
            return (int(valor_esq and valor_dir), "int")
        elif self.value == '||':
            return (int(valor_esq or valor_dir), "int")
        else:
            raise ValueError("Operação não suportada!")

class Assignment(Node):
    def __init__(self, var_name: str, expr: Node):
        super().__init__('=')
        self.var_name = var_name  # O nome da variável não é um nó, é apenas o nome
        self.children.append(expr)  # A expressão é um nó

    def Evaluate(self, symbol_table: SymbolTable):    
        value, var_type = self.children[0].Evaluate(symbol_table)
        if self.var_name not in list(symbol_table.symbols.keys()):
            raise NameError(f"Variável '{self.var_name}' não declarada.")
        symbol_table.assign(self.var_name, value, var_type)  # Armazenar o valor na tabela de símbolos
        return (value, var_type)
    
class VarDec(Node):
    def __init__(self, var_type: str, variaveis: List[str], atribuicoes: List[Node] = []):
        super().__init__('VarDec')
        self.var_type = var_type
        self.variaveis = variaveis
        self.atribuicoes = atribuicoes

    def Evaluate(self, symbol_table: SymbolTable):
        # Primeiramente, declara todas as variáveis com o tipo fornecido
        for var_name in self.variaveis:
            if var_name in symbol_table.symbols:
                raise ValueError(f"A variável '{var_name}' já foi declarada.")
            # Inicializa com None por padrão
            symbol_table.set(var_name, None, self.var_type)

        # Agora, faz as atribuições quando disponíveis
        for i, var_name in enumerate(self.variaveis):
            if i < len(self.atribuicoes):  # Verifica se existe uma atribuição correspondente
                value, assigned_type = self.atribuicoes[i].Evaluate(symbol_table)
                if assigned_type != self.var_type:
                    raise TypeError(f"Tipo incompatível para '{var_name}'. Esperado: {self.var_type}.")
                # Atualiza o valor na tabela de símbolos
                #symbol_table.set(var_name, value, self.var_type)
        return None, None

class Identifier(Node):
    def __init__(self, value: str):
        super().__init__(value)

    def Evaluate(self, symbol_table: SymbolTable) -> int:
        value, var_type = symbol_table.get(self.value)
        return (value, var_type)

class Block(Node):
    def __init__(self):
        super().__init__('block')

    def Evaluate(self, symbol_table: SymbolTable) -> None:
        for child in self.children:
            result = child.Evaluate(symbol_table)
            if isinstance(child, Return):
                return result

class Printf(Node):
    def __init__(self, child: Node):
        super().__init__('printf')
        self.children.append(child)

    def Evaluate(self, symbol_table: SymbolTable):
        value, var_type = self.children[0].Evaluate(symbol_table)
        print(value)
        return None, None
    
class FuncDec(Node):
    def __init__(self, func_name: str, func_type: str, lista_var_dec_arg: List[Node], block: Node):
        super().__init__(func_name)  # Chama o construtor da classe base para inicializar a lista `children`
        self.func_name = func_name
        self.func_type = func_type
        # Adiciona os nós-filhos corretamente
        if lista_var_dec_arg == []:
            self.children.append([])
        else:
            self.children.append(lista_var_dec_arg)
        self.children.append(block)

    def Evaluate(self, symbol_table: SymbolTable):
        # Define a função na tabela de símbolos com o tipo FUNCTION
        symbol_table.set(self.func_name, self, 'FUNCTION')
        FuncTable.set(self.func_name, self, 'FUNCTION')
        return None


class FuncCall(Node):
    def __init__(self, func_name: str, argumentos: List[Node]):
        super().__init__(func_name)  # Chama o construtor da classe base para inicializar `children`
        self.func_name = func_name
        self.children.extend(argumentos)  # Adiciona cada argumento individualmente

    def Evaluate(self, symbol_table: SymbolTable):
        # Recupera o nó da função a partir da tabela de símbolos
        node_func = FuncTable.get(self.func_name)

        # Cria uma tabela de símbolos local para a execução da função
        local_symbol_table = SymbolTable()
        lista_var_dec_args, block = node_func[0].children

        # Verifica se o número de argumentos da chamada coincide com o número de parâmetros]

        if len(lista_var_dec_args) != len(self.children):
            raise Exception(f"Erro de sintaxe: número de argumentos diferente do número de parâmetros da função {self.func_name}!")

        # Associa os argumentos passados aos parâmetros da função
        for var_dec, arg_call in zip(lista_var_dec_args, self.children):
            var_dec.Evaluate(local_symbol_table)  # Avalia a declaração do parâmetro
            local_symbol_table.assign(var_dec.variaveis[0], arg_call.Evaluate(symbol_table)[0],var_dec.var_type)

        result = block.Evaluate(local_symbol_table)
        return result

class Return(Node):
    def __init__(self, value):
        super().__init__("Return")
        self.children.append(value)
    def Evaluate(self, symbol_table):
        return self.children[0].Evaluate(symbol_table)
    
class Program(Node):
    def __init__(self, functions):
        super().__init__('program')
        self.children = functions
    
    def Evaluate(self, symbol_table):
        main = False
        for func in self.children:
            if func.func_name == 'main':
                main = True
            func.Evaluate(symbol_table)
        if main:
            no_main = FuncCall('main', [])
            return no_main.Evaluate(symbol_table)
        else:
            raise Exception ("é necessário uma função main")
        
class CharacterNode(Node):
    def __init__(self, name: str, attributes: dict):
        super().__init__('CHARACTER')
        self.name = name
        self.attributes = attributes

    def Evaluate(self, symbol_table: SymbolTable):
        # Armazena o personagem na tabela de símbolos
        symbol_table.set(self.name, self.attributes, 'CHARACTER')

class SpellNode(Node):
    def __init__(self, name: str, power: int, mana_cost: int, effect: str):
        super().__init__('SPELL')
        self.name = name
        self.power = power
        self.mana_cost = mana_cost
        self.effect = effect

    def Evaluate(self, symbol_table: SymbolTable):
        symbol_table.set(self.name, {
            'power': self.power,
            'mana_cost': self.mana_cost,
            'effect': self.effect
        }, 'SPELL')

class MissionNode(Node):
    def __init__(self, name: str, objective: str, participants: list, reward: list, location: str):
        super().__init__('MISSION')
        self.name = name
        self.objective = objective
        self.participants = participants
        self.reward = reward
        self.location = location

    def Evaluate(self, symbol_table: SymbolTable):
        symbol_table.set(self.name, {
            'objective': self.objective,
            'participants': self.participants,
            'reward': self.reward,
            'location': self.location
        }, 'MISSION')


class Parser:
    @staticmethod
    def parseFactor(tokenizer: Tokenizer):
        if tokenizer.next.type == 'OPPAR':
            tokenizer.selectNext()
            result = Parser.parseRelationalExpression(tokenizer)
            if tokenizer.next.type == 'CLPAR':
                tokenizer.selectNext()
                return result
            else:
                raise Exception("Esperado fechar parênteses")

        elif tokenizer.next.type == 'INT':
            result = IntVal(tokenizer.next.value)
            tokenizer.selectNext()
            return result
        
        elif tokenizer.next.type == 'STRING':
            result = StringVal(tokenizer.next.value)
            tokenizer.selectNext()
            return result

        elif tokenizer.next.type == 'IDENT':
            id_name = tokenizer.next.value
            identifier = Identifier(id_name)
            tokenizer.selectNext()
            if tokenizer.next.type == "OPPAR":
                tokenizer.selectNext()
                arguments = []
                while tokenizer.next.type != 'CLPAR':
                    arguments.append(Parser.parseRelationalExpression(tokenizer))
                    if tokenizer.next.type == 'COMMA':
                        tokenizer.selectNext()
                if tokenizer.next.type != 'CLPAR':
                    raise Exception("Esperado ')' ao final da chamada de função")
                tokenizer.selectNext()
                return FuncCall(id_name, arguments)
            return identifier

        elif tokenizer.next.type == 'PLUS':
            tokenizer.selectNext()
            return UnOp('+', Parser.parseFactor(tokenizer))
        
        elif tokenizer.next.type == 'MINUS':
            tokenizer.selectNext()
            return UnOp('-', Parser.parseFactor(tokenizer))
        
        elif tokenizer.next.type == 'NOT':
            tokenizer.selectNext()
            return UnOp('!', Parser.parseFactor(tokenizer))
        
        elif tokenizer.next.type == 'SCANF':
            tokenizer.selectNext()
            if tokenizer.next.type == 'OPPAR':
                tokenizer.selectNext()
                if tokenizer.next.type == 'CLPAR':
                    tokenizer.selectNext()
                    return Scanf()
                else:
                    raise Exception("Esperado ')' após o nome da variável em scanf")
            else:
                raise Exception("Esperado um '(' após 'scanf'")

    @staticmethod
    def parseTerm(tokenizer: Tokenizer):
        result = Parser.parseFactor(tokenizer)

        while tokenizer.next.type in ['MULT', 'DIV', 'AND']:
            if tokenizer.next.type == 'MULT':
                tokenizer.selectNext()
                result = BinOp('*', result, Parser.parseFactor(tokenizer))
            elif tokenizer.next.type == 'DIV':
                tokenizer.selectNext()
                result = BinOp('/', result, Parser.parseFactor(tokenizer))
            elif tokenizer.next.type == 'AND':
                tokenizer.selectNext()
                result = BinOp('&&', result, Parser.parseFactor(tokenizer))
        return result

    @staticmethod
    def parseExpression(tokenizer: Tokenizer):
        result = Parser.parseTerm(tokenizer)

        while tokenizer.next.type in ['PLUS', 'MINUS', 'OR']:
            if tokenizer.next.type == 'PLUS':
                tokenizer.selectNext()
                result = BinOp('+', result, Parser.parseTerm(tokenizer))
            elif tokenizer.next.type == 'MINUS':
                tokenizer.selectNext()
                result = BinOp('-', result, Parser.parseTerm(tokenizer))
            elif tokenizer.next.type == 'OR':
                tokenizer.selectNext()
                result = BinOp('||', result, Parser.parseTerm(tokenizer))

        return result
    
    @staticmethod
    def parseRelationalExpression(tokenizer: Tokenizer):
        result = Parser.parseExpression(tokenizer)

        while tokenizer.next.type in ['EQUALS', 'MINOR', 'GREATER']:
            if tokenizer.next.type == 'EQUALS':
                tokenizer.selectNext()
                result = RelationOp('==', result, Parser.parseExpression(tokenizer))
            elif tokenizer.next.type == 'MINOR':
                tokenizer.selectNext()
                result = RelationOp('<', result, Parser.parseExpression(tokenizer))
            elif tokenizer.next.type == "GREATER":
                tokenizer.selectNext()
                result = RelationOp('>', result, Parser.parseExpression(tokenizer))

        return result

    @staticmethod
    def parseStatement(tokenizer: Tokenizer):
        if tokenizer.next.type in ['INTEIRO', 'STR']:
            if tokenizer.next.type == 'INTEIRO':
                tipo = "int"
            else:
                tipo = "str"
            tokenizer.selectNext()
            variaveis = []
            atribuicoes = []
            
            while tokenizer.next.type == 'IDENT':
                var_name = tokenizer.next.value
                variaveis.append(var_name)
                tokenizer.selectNext()

                if tokenizer.next.type == 'EQUAL':
                    tokenizer.selectNext()
                    atribuicoes.append(Assignment(var_name, Parser.parseRelationalExpression(tokenizer)))

                if tokenizer.next.type == 'COMMA':
                    tokenizer.selectNext()
                elif tokenizer.next.type == 'SEMICOLON':
                    break
                else:
                    raise Exception("Erro de sintaxe: esperado ',' ou ';' após a variável.")
                
            if tokenizer.next.type != 'SEMICOLON':
                raise Exception("Erro de sintaxe: esperado ';' após a declaração.")
            tokenizer.selectNext()

            return VarDec(tipo, variaveis, atribuicoes)
        
        elif tokenizer.next.type == 'IDENT':
            var_name = tokenizer.next.value
            tokenizer.selectNext()
            if tokenizer.next.type == 'EQUAL':
                tokenizer.selectNext()
                expr = Parser.parseRelationalExpression(tokenizer)
                if tokenizer.next.type == 'SEMICOLON':
                    tokenizer.selectNext()
                    return Assignment(var_name, expr)
            elif tokenizer.next.type == 'OPPAR':
                args = []
                tokenizer.selectNext()
                while tokenizer.next.type != 'CLPAR':
                    args.append(Parser.parseRelationalExpression(tokenizer))
                    if tokenizer.next.type == 'COMMA':
                        tokenizer.selectNext()
                
                if tokenizer.next.type != 'CLPAR':
                    raise Exception("Esperado ')' ao final da chamada de função!")
                tokenizer.selectNext()
                if tokenizer.next.type == 'SEMICOLON':
                    tokenizer.selectNext()
                    return FuncCall(var_name, args)

        elif tokenizer.next.type == 'PRINTF':
            tokenizer.selectNext()

            if tokenizer.next.type == 'OPPAR':
                tokenizer.selectNext()
                expr = Parser.parseRelationalExpression(tokenizer)

                if tokenizer.next.type == 'CLPAR':
                    tokenizer.selectNext()

                    if tokenizer.next.type == 'SEMICOLON':
                        tokenizer.selectNext()
                        return Printf(expr)
                    else:
                        raise Exception("Esperado ';' após a chamada de printf")
                else:
                    raise Exception("Esperado ')' após a expressão no printf")
            else:
                raise Exception("Esperado '(' após 'printf'")
            
        elif tokenizer.next.type == 'IF':
            tokenizer.selectNext()
            if tokenizer.next.type == 'OPPAR':
                tokenizer.selectNext()
                cond = Parser.parseRelationalExpression(tokenizer)
                if tokenizer.next.type == 'CLPAR':
                    tokenizer.selectNext()
                    if tokenizer.next.type == 'OPBRACE':
                        if_block = Parser.parseBlock(tokenizer)
                    else:
                        if_block = Parser.parseStatement(tokenizer)

                    else_block = None
                    if tokenizer.next.type == 'ELSE':
                        tokenizer.selectNext()
                        if tokenizer.next.type == 'OPBRACE':
                            else_block = Parser.parseBlock(tokenizer)
                        else:
                            else_block = Parser.parseStatement(tokenizer)
                    return If(cond, if_block, else_block)
                else:
                    raise Exception("Esperado um ')' após a expressão condicional")  
            else:
                raise Exception("Esperado um '(' após 'if'")    
            
        elif tokenizer.next.type == 'WHILE':
            tokenizer.selectNext()
            if tokenizer.next.type == 'OPPAR':
                tokenizer.selectNext()
                cond = Parser.parseRelationalExpression(tokenizer)
                if tokenizer.next.type == 'CLPAR':
                    tokenizer.selectNext()
                    if tokenizer.next.type == 'OPBRACE':
                        block = Parser.parseBlock(tokenizer)
                    else:
                        block = Parser.parseStatement(tokenizer)
                    return While(cond, block)
                else:
                    raise Exception("Esperado um ')' após a expressão do while")
            else:
                raise Exception("Esperado um '(' após while")
        
        elif tokenizer.next.type == 'RETURN':
            tokenizer.selectNext()
            expr = None
            if tokenizer.next.type == 'OPPAR':
                tokenizer.selectNext()
                expr = Parser.parseRelationalExpression(tokenizer)
                if tokenizer.next.type == 'CLPAR':
                    tokenizer.selectNext()
                    return Return(expr)
                else: 
                    raise Exception("Esperado um ')' após a expressão do return")
            else:
                raise Exception("Esperado um '(' após return")
            
        elif tokenizer.next.type == 'CREATE':
            tokenizer.selectNext()
            if tokenizer.next.type == 'CHARACTER':
                tokenizer.selectNext()
                if tokenizer.next.type == 'STRING':
                    name = tokenizer.next.value
                    tokenizer.selectNext()
                    if tokenizer.next.type == 'OPBRACE':
                        tokenizer.selectNext()
                        if tokenizer.next.type == 'ATRIBUTOS':
                            tokenizer.selectNext()
                            if tokenizer.next.type == 'EQUAL':
                                tokenizer.selectNext()
                                attributes = {}
                                if tokenizer.next.type == 'OPBRACE':
                                    tokenizer.selectNext()
                                    while tokenizer.next.type != 'CLBRACE':
                                        attr_name = tokenizer.next.type
                                        tokenizer.selectNext()
                                        if tokenizer.next.type == 'EQUAL':
                                            tokenizer.selectNext()
                                            if tokenizer.next.type == 'INT':
                                                attributes[attr_name] = tokenizer.next.value
                                                tokenizer.selectNext()
                                            if tokenizer.next.type == 'SEMICOLON':
                                                tokenizer.selectNext()

                                        else:
                                            raise Exception("Esperado '=' nos atributos")
                                    tokenizer.selectNext()
                                    return CharacterNode(name, attributes)
                                else:
                                    raise Exception("Esperado '{' no bloco de atributos")
                        else:
                            raise Exception("Esperado 'attributes'")
                else:
                    raise Exception("Esperado nome do personagem")
            

        elif tokenizer.next.type == 'SEMICOLON':
            # Ignora múltiplos pontos e vírgulas seguidos
            tokenizer.selectNext()
            return NoOp()

        elif tokenizer.next.type == 'EOF':
            return NoOp()
        
        elif tokenizer.next.type == 'OPBRACE':  # Início de um bloco aninhado
            return Parser.parseBlock(tokenizer)  # Chama parseBlock diretamente

        else:
            raise Exception("Instrução inválida")


    @staticmethod
    def parseBlock(tokenizer: Tokenizer):
        block = Block()  # Cria um novo nó de bloco para armazenar as instruções

        if tokenizer.next.type == 'OPBRACE':  # Verifica se há uma abertura de bloco '{'
            tokenizer.selectNext()
            while tokenizer.next.type != 'CLBRACE':  # Enquanto não encontrar o fechamento '}'
                block.children.append(Parser.parseStatement(tokenizer))  # Adiciona instruções ao bloco
                
                # Se atingir EOF sem encontrar o '}', lança uma exceção
                if tokenizer.next.type == 'EOF':
                    raise Exception("Erro de sintaxe: Esperado '}' para fechar o bloco")

            tokenizer.selectNext()  # Consome o token de fechamento '}'
        else:
            raise Exception("Erro de sintaxe: Esperado '{' no início do bloco")

        return block
    
    @staticmethod
    def parseFunction(tokenizer: Tokenizer):
        # Suporte para declarar funções do tipo 'int' ou 'void'
        if tokenizer.next.type not in ['INTEIRO', 'VOID']:
            raise Exception("Esperado 'int' ou 'void' para declaração de função")
        
        if tokenizer.next.type == 'INTEIRO':
            func_type = "int"
        else:
            func_type = "void"
        
        tokenizer.selectNext()

        if tokenizer.next.type != 'IDENT':
            raise Exception("Esperado o nome da função")
        
        func_name = tokenizer.next.value
        tokenizer.selectNext()

        if tokenizer.next.type != 'OPPAR':
            raise Exception("Esperado '(' após o nome da função")
        
        tokenizer.selectNext()
        params = []
        if tokenizer.next.type != 'CLPAR':
            # Parse de parâmetros de função
            while True:
                if tokenizer.next.type == 'INTEIRO':
                    param_type = 'int'
                elif tokenizer.next.type == 'STR':
                    param_type = 'str'
                else:
                    raise Exception("Tipo de parâmetro inválido")

                tokenizer.selectNext()

                if tokenizer.next.type != 'IDENT':
                    raise Exception("Esperado nome do parâmetro")
                
                param_name = tokenizer.next.value
                node_param = VarDec(param_type, [param_name])
                params.append(node_param)
                tokenizer.selectNext()

                if tokenizer.next.type == 'COMMA':
                    tokenizer.selectNext()
                else:
                    break
        
        if tokenizer.next.type != 'CLPAR':
            raise Exception("Esperado ')' após a lista de parâmetros")
        
        tokenizer.selectNext()

        if tokenizer.next.type != 'OPBRACE':
            raise Exception("Esperado '{' para início do corpo da função")
        
        func_body = Parser.parseBlock(tokenizer)
        return FuncDec(func_name, func_type, params, func_body)
    
    @staticmethod
    def parseProgram(tokenizer: Tokenizer):
        program = []
        while tokenizer.next.type != 'EOF':
            program.append(Parser.parseFunction(tokenizer))
        return Program(program)
    
    @staticmethod
    def parseCharacter(tokenizer: Tokenizer):
        if tokenizer.next.type == 'CREATE':
            tokenizer.selectNext()
            if tokenizer.next.type == 'CHARACTER':
                tokenizer.selectNext()
                if tokenizer.next.type == 'STRING':
                    name = tokenizer.next.value
                    tokenizer.selectNext()
                    if tokenizer.next.type == 'OPBRACE':
                        tokenizer.selectNext()
                        if tokenizer.next.type == 'ATRIBUTOS':
                            tokenizer.selectNext()
                            if tokenizer.next.type == 'EQUAL':
                                tokenizer.selectNext()
                                attributes = {}
                                if tokenizer.next.type == 'OPBRACE':
                                    tokenizer.selectNext()
                                    while tokenizer.next.type != 'CLBRACE':
                                        attr_name = tokenizer.next.type
                                        tokenizer.selectNext()
                                        if tokenizer.next.type == 'EQUAL':
                                            tokenizer.selectNext()
                                            if tokenizer.next.type == 'INT':
                                                attributes[attr_name] = tokenizer.next.value
                                                tokenizer.selectNext()
                                            if tokenizer.next.type == 'SEMICOLON':
                                                tokenizer.selectNext()
                                        else:
                                            raise Exception("Expected '=' in attributes")
                                    tokenizer.selectNext()
                                else:
                                    raise Exception("Expected '{' in attributes block")
                        else:
                            raise Exception("Expected 'attributes'")
                else:
                    raise Exception("Expected character name")
        else:
            raise Exception("Expected 'CREATE'")
        return CharacterNode(name, attributes)


    @staticmethod
    def run(code: str):
        tokenizer = Tokenizer(code)
        program = Parser.parseProgram(tokenizer)  # Executa o bloco principal
        if tokenizer.next.type != 'EOF':
            raise Exception("Caractere inesperado no final do código")
        
        return program


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python <nome_programa> <nome_arquivo>")
        sys.exit(1)

    caminho_arquivo = sys.argv[1]

    try:
        codigo_limpo = PrePro.filter(caminho_arquivo)
        arvore = Parser.run(codigo_limpo)
        symbol_table = SymbolTable()
        arvore.Evaluate(symbol_table)

    except FileNotFoundError:
        print("Arquivo não encontrado")
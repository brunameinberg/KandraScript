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
        if '.' in name:  # Identificador composto, como Hero.strength
            parts = name.split('.')
            current = self.symbols.get(parts[0])
            if current is None:
                raise KeyError(f"Identificador '{parts[0]}' não encontrado.")
            value, value_type = current
            if not isinstance(value, dict):
                raise KeyError(f"Identificador '{parts[0]}' não contém atributos.")
            
            for part in parts[1:]:
                if part in value:
                    value = value[part]
                else:
                    raise KeyError(f"Atributo '{part}' não encontrado em '{parts[0]}'.")
            
            return value, type(value).__name__.lower()
        else:  # Identificador simples
            if name in self.symbols:
                return self.symbols[name][0], self.symbols[name][1]
            else:
                raise KeyError(f"Identificador '{name}' não encontrado.")

    def assign(self, name, value, var_type):
        if '.' in name:
            parts = name.split('.')
            current = self.symbols.get(parts[0])
            if current is None:
                raise KeyError(f"Identificador '{parts[0]}' não encontrado.")

            obj, obj_type = current
            if not isinstance(obj, dict):
                raise KeyError(f"'{parts[0]}' não é um objeto válido para atribuição.")

            # Navegar até o atributo final
            for part in parts[1:-1]:
                if part not in obj:
                    raise KeyError(f"Atributo '{part}' não encontrado.")
                obj = obj[part]

            final_attr = parts[-1]
            if final_attr not in obj:
                raise KeyError(f"Atributo '{final_attr}' não encontrado.")
            
            # Verificar o tipo e atualizar o valor
            if isinstance(obj[final_attr], int) and var_type != "int":
                raise TypeError(f"Tipo incompatível para '{final_attr}'. Esperado 'int'.")
            print(f"DEBUG assign: Atualizando '{name}' para {value} (tipo: {var_type})")
            obj[final_attr] = value

        else:
            # Identificadores simples
            if name not in self.symbols:
                raise KeyError(f"Variável '{name}' não declarada.")
            if self.symbols[name][1] != var_type:
                raise TypeError(f"Tipo incompatível para variável '{name}'.")
            print(f"DEBUG assign: Atualizando '{name}' para {value} (tipo: {var_type})")
            self.symbols[name][0] = value




    def set(self, name, value, value_type):
        self.symbols[name] = [value, value_type]



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
        

        elif self.source[self.position:self.position + 9] == "character":
            self.next = Token('CHARACTER', None)
            self.position += 9
        
        elif self.source[self.position:self.position + 10] == "attributes":
            self.next = Token('ATTRIBUTES', None)
            self.position += 10

        elif self.source[self.position:self.position + 8] == "strength":
            self.next = Token('IDENT', "strength")
            self.position += 8

        elif self.source[self.position:self.position + 5] == "magic":
            self.next = Token('IDENT', "magic")
            self.position += 5

        elif self.source[self.position:self.position + 9] == "mana_cost":
            self.next = Token('IDENT', "mana_cost")
            self.position += 9

        elif self.source[self.position:self.position + 4] == "mana":
            self.next = Token('IDENT', "mana")
            self.position += 4

        elif self.source[self.position:self.position + 9] == "inventory":
            self.next = Token('IDENT', "inventory")
            self.position += 9      

        elif self.source[self.position:self.position + 5] == "spell":
            self.next = Token('SPELL', None)
            self.position += 5

        elif self.source[self.position:self.position + 5] == "power":
            self.next = Token('IDENT', "power")
            self.position += 5

        elif self.source[self.position:self.position + 6] == "effect":
            self.next = Token('IDENT', "effect")
            self.position += 6

        elif self.source[self.position:self.position + 7] == "mission":
            self.next = Token('MISSION', None)
            self.position += 7

        elif self.source[self.position:self.position + 9] == "objective":
            self.next = Token('OBJECTIVE', None)
            self.position += 9

        elif self.source[self.position:self.position + 12] == "participants":
            self.next = Token('PARTICIPANTS', None)
            self.position += 12

        elif self.source[self.position:self.position + 6] == "reward":
            self.next = Token('REWARD', None)
            self.position += 6

        elif self.source[self.position:self.position + 8] == "location":
            self.next = Token('LOCATION', None)
            self.position += 8

        elif self.source[self.position:self.position + 6] == "CREATE":
            self.next = Token('CREATE', None)
            self.position += 6

        elif self.source[self.position:self.position + 4] == "CAST":
            self.next = Token('CAST', None)
            self.position += 4

        elif self.source[self.position:self.position + 12] == "ENCHANTED_IF":
            self.next = Token('ENCHANTED_IF', None)
            self.position += 12

        elif self.source[self.position:self.position + 21] == "WHILE_THE_MOON_SHINES":
            self.next = Token('WHILE_THE_MOON_SHINES', None)
            self.position += 21

        elif self.source[self.position:self.position + 22] == "UNTIL_THE_FINAL_BATTLE":
            self.next = Token('UNTIL_THE_FINAL_BATTLE', None)
            self.position += 22
        
        elif self.source[self.position:self.position + 10] == "OTHER_PATH":
            self.next = Token('OTHER_PATH', None)
            self.position += 10
        
        elif self.source[self.position:self.position + 14] == "CREATE_DYNAMIC":
            self.next = Token('CREATE_DYNAMIC', None)
            self.position += 14

        elif self.source[self.position:self.position + 10] == "ITERATE_LIST":
            self.next = Token('ITERATE_LIST', None)
            self.position += 10

        elif self.source[self.position:self.position + 13] == "ADVANCE_MISSION":
            self.next = Token('ADVANCE_MISSION', None)
            self.position += 13

        elif self.source[self.position:self.position + 12] == "MISSION_STEP":
            self.next = Token('MISSION_STEP', None)
            self.position += 12
        
        elif self.source[self.position:self.position + 2] == "IN":
            self.next = Token('IN', None)
            self.position += 2
        
        elif self.source[self.position] == ".":
            self.next = Token('DOT', None)
            self.position += 1

        elif self.source[self.position:self.position + 2] == "BY":
            self.next = Token('BY', None)
            self.position += 2
        
        elif self.source[self.position:self.position + 2] == "ON":
            self.next = Token('ON', None)
            self.position += 2

        elif self.source[self.position:self.position + 3] == "LOG":
            self.next = Token('LOG', None)
            self.position += 3

            print(f"Tokenizer: token identificado -> {self.next.type}, valor -> {self.next.value}")

        #tratando lista
        elif self.source[self.position] == "[":
            self.next = Token('OPEN_BRACKET', None)
            self.position += 1

        elif self.source[self.position] == "]":
            self.next = Token('CLOSE_BRACKET', None)
            self.position += 1
            
        #operadores lógicos

        elif self.source[self.position:self.position + 2] == '!=':
            self.next = Token('NOT_EQUALS', None)
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
    
        #print(f"DEBUG Tokenizer: Próximo token -> {self.next.type}, Valor -> {self.next.value}, Posição -> {self.position}")



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
    def __init__(self, cond: Node, block: Node):
        super().__init__('while')
        self.children.extend([cond, block])

    def Evaluate(self, symbol_table: SymbolTable):
        print("DEBUG While: Iniciando avaliação do loop")

        cond_value, cond_type = self.children[0].Evaluate(symbol_table)

        while cond_value:
            self.children[1].Evaluate(symbol_table)
            cond_value, cond_type = self.children[0].Evaluate(symbol_table)

        return None, None

    
    
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
        print(f"DEBUG Assignment: Atribuindo {value} (tipo: {var_type}) para {self.var_name}")
        symbol_table.assign(self.var_name, value, var_type)
        # Confirmar a atualização
        novo_valor, _ = symbol_table.get(self.var_name)
        print(f"DEBUG Assignment: Novo valor de {self.var_name} é {novo_valor}")
        return (value, var_type)
    

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
            child.Evaluate(symbol_table)


class Printf(Node):
    def __init__(self, child: Node):
        super().__init__('printf')
        self.children.append(child)

    def Evaluate(self, symbol_table: SymbolTable):
        value, var_type = self.children[0].Evaluate(symbol_table)
        print(value)
        return None, None
    

        
class CharacterNode(Node):
    def __init__(self, name: str, attributes: dict):
        super().__init__('CHARACTER')
        self.name = name
        self.attributes = {k.lower(): v for k, v in attributes.items()}

    def Evaluate(self, symbol_table: SymbolTable):
        # Armazena o personagem na tabela de símbolos
        symbol_table.set(self.name, self.attributes, 'CHARACTER')
        print(f"Personagem criado: {self.name}")
        print(f"Atributos de {self.name}: {self.attributes}")

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

        print(f"Feitiço criado: {self.name}")
        caracteristicas = f"Power: {self.power}, Mana Cost: {self.mana_cost}, Effect: {self.effect}"
        print(f"Características de {self.name}: {caracteristicas}")


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

        print(f"Missão criada: {self.name}")
        caracteristicas = f"Objective: {self.objective}, Participants: {self.participants}, Reward: {self.reward}, Location: {self.location}"
        print(f"Características de {self.name}: {caracteristicas}")

class ListNode(Node):
    def __init__(self, elements):
        super().__init__('LIST')
        self.children.extend(elements)

    def Evaluate(self, symbol_table: SymbolTable):
        return [child.Evaluate(symbol_table)[0] for child in self.children], "list"

class IterateList(Node):
    def __init__(self, iterator, iterable, block):
        super().__init__('ITERATE_LIST')
        self.iterator = iterator
        self.iterable = iterable
        self.children.append(block)

    def Evaluate(self, symbol_table: SymbolTable):
        iterable, _ = symbol_table.get(self.iterable)
        for item in iterable:
            symbol_table.set(self.iterator, item, "VALUE")
            self.children[0].Evaluate(symbol_table)

class AdvanceMission(Node):
    def __init__(self, mission_name, next_step):
        super().__init__('ADVANCE_MISSION')
        self.mission_name = mission_name
        self.next_step = next_step

    def Evaluate(self, symbol_table: SymbolTable):
        mission, _ = symbol_table.get(self.mission_name)
        mission['objective'] = self.next_step
        symbol_table.set(self.mission_name, mission, "MISSION")

class CreateDynamic(Node):
    def __init__(self, obj_type, name, block):
        super().__init__('CREATE_DYNAMIC')
        self.obj_type = obj_type
        self.name = name
        self.children.append(block)

    def Evaluate(self, symbol_table: SymbolTable):
        block_result = self.children[0].Evaluate(symbol_table)
        symbol_table.set(self.name, block_result, self.obj_type)

class CastSpellNode(Node):
    def __init__(self, spell_name: str, caster: str, target: str):
        super().__init__('CAST')
        self.spell_name = spell_name
        self.caster = caster
        self.target = target

    def Evaluate(self, symbol_table: SymbolTable):
        # Recupera o feitiço da tabela de símbolos
        spell, spell_type = symbol_table.get(self.spell_name)
        if spell_type != 'SPELL':
            raise Exception(f"'{self.spell_name}' não é um feitiço válido.")

        # Recupera o lançador e o alvo da tabela de símbolos
        caster, caster_type = symbol_table.get(self.caster)
        target, target_type = symbol_table.get(self.target)

        if caster_type != 'CHARACTER':
            raise Exception(f"'{self.caster}' não é um personagem válido.")
        if target_type != 'CHARACTER':
            raise Exception(f"'{self.target}' não é um personagem válido.")

        # Verifica se o lançador tem mana suficiente
        if caster.get('mana', 0) < spell['mana_cost']:
            raise Exception(f"'{self.caster}' não tem mana suficiente para lançar '{self.spell_name}'.")

        # Consome a mana do lançador
        caster['mana'] -= spell['mana_cost']

        # Aplica o efeito no alvo (apenas exibe uma mensagem por enquanto)
        print(f"{self.caster} lançou '{self.spell_name}' em {self.target}!")
        print(f"Efeito: {spell['effect']}")
        print(f"{self.target} sofreu {spell['power']} de dano!")
        
        # Atualiza a tabela de símbolos
        symbol_table.set(self.caster, caster, 'CHARACTER')
        symbol_table.set(self.target, target, 'CHARACTER')

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
            # Inicia um identificador simples
            var_name = tokenizer.next.value
            tokenizer.selectNext()

            # Permite composição de identificadores (IDENT.DOT.IDENT)
            while tokenizer.next.type == 'DOT':
                tokenizer.selectNext()
                if tokenizer.next.type == 'IDENT':
                    prop_name = tokenizer.next.value
                    var_name = f"{var_name}.{prop_name}"  # Concatena como identificador composto
                    tokenizer.selectNext()
                else:
                    raise Exception("Esperado identificador após '.'")

            return Identifier(var_name)  # Retorna o identificador completo

        elif tokenizer.next.type == 'PLUS':
            tokenizer.selectNext()
            return UnOp('+', Parser.parseFactor(tokenizer))
        
        elif tokenizer.next.type == 'MINUS':
            tokenizer.selectNext()
            return UnOp('-', Parser.parseFactor(tokenizer))
        
        elif tokenizer.next.type == 'NOT':
            tokenizer.selectNext()
            return UnOp('!', Parser.parseFactor(tokenizer))
        
        #lista
        #lista
        elif tokenizer.next.type == 'OPEN_BRACKET':
            tokenizer.selectNext()
            elements = []
            while tokenizer.next.type != 'CLOSE_BRACKET':
                elements.append(Parser.parseRelationalExpression(tokenizer))
                if tokenizer.next.type == 'COMMA':
                    tokenizer.selectNext()
            if tokenizer.next.type != 'CLOSE_BRACKET':
                raise Exception("Esperado ']' para fechar a lista.")
            tokenizer.selectNext()
            return ListNode(elements)



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
        print(f"parseStatement: token atual -> {tokenizer.next.type}, valor -> {tokenizer.next.value}")
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
            var_name = tokenizer.next.value  # Obtém o identificador inicial
            tokenizer.selectNext()

            # Verifica identificadores compostos (com DOT)
            while tokenizer.next.type == 'DOT':
                tokenizer.selectNext()
                if tokenizer.next.type == 'IDENT':
                    var_name += f".{tokenizer.next.value}"  # Concatena o nome completo
                    tokenizer.selectNext()
                else:
                    raise Exception("Esperado identificador após '.'")

            # Verifica se é uma atribuição
            if tokenizer.next.type == 'EQUAL':
                print(f"DEBUG parseStatement: Criando nó Assignment para {var_name}")
                tokenizer.selectNext()  # Consome '='
                expr = Parser.parseRelationalExpression(tokenizer)  # Processa o lado direito
                if tokenizer.next.type == 'SEMICOLON':
                    tokenizer.selectNext()  # Consome ';'
                    return Assignment(var_name, expr)  # Retorna nó de atribuição
                else:
                    raise Exception("Esperado ';' após atribuição.")
            else:
                raise Exception(f"Instrução inválida no token: {tokenizer.next.type}, valor: {tokenizer.next.value}")

                    

        elif tokenizer.next.type == 'ENCHANTED_IF':
            tokenizer.selectNext()
            condition = Parser.parseRelationalExpression(tokenizer)  # Avaliação da condição lógica
            
            if tokenizer.next.type == 'OPBRACE':  # Espera abertura do bloco "{"
                tokenizer.selectNext()
                if_block = Parser.parseBlock(tokenizer)  # Processa o bloco associado ao "if"
                print(f"DEBUG ENCHANTED_IF: Bloco IF contém {len(if_block.children)} instruções")
            else:
                raise Exception("Esperado '{' após 'ENCHANTED_IF' para abrir o bloco.")

            else_block = None  # Bloco "else" é opcional
            tokenizer.selectNext()
            
            if tokenizer.next.type == 'OTHER_PATH':  # Verifica se há um bloco "else"
                print("DEBUG: Encontrado OTHER_PATH")
                tokenizer.selectNext()
                print("DEBUG: Encontrado OTHER_PATH")
                if tokenizer.next.type == 'OPBRACE':  # Espera abertura do bloco "{"
                    
                    tokenizer.selectNext()
                    else_block = Parser.parseBlock(tokenizer)  # Processa o bloco associado ao "else"
                    print(f"DEBUG OTHER_PATH: Bloco ELSE contém {len(else_block.children)} instruções")
                else:
                    raise Exception("Esperado '{' após 'OTHER_PATH' para abrir o bloco.")

            return If(condition, if_block, else_block)

        elif tokenizer.next.type == "LOG":
            tokenizer.selectNext()
            if tokenizer.next.type == 'OPPAR':
                tokenizer.selectNext()
                message = Parser.parseRelationalExpression(tokenizer)
                if tokenizer.next.type == 'CLPAR':
                    tokenizer.selectNext()
                    if tokenizer.next.type == 'SEMICOLON':
                        tokenizer.selectNext()
                        return Printf(message)
                    else:
                        raise Exception("Esperado ';' após LOG.")
                else:
                    raise Exception("Esperado ')' após argumento de LOG.")
            else:
                raise Exception("Esperado '(' após LOG.")
    
            
        elif tokenizer.next.type == 'WHILE_THE_MOON_SHINES':
            tokenizer.selectNext()  # Consome o token 'WHILE_THE_MOON_SHINES'
            if tokenizer.next.type == 'OPPAR':  # Verifica '('
                tokenizer.selectNext()  # Consome '('
                condition = Parser.parseRelationalExpression(tokenizer)  # Processa a condição
                if tokenizer.next.type == 'CLPAR':  # Verifica ')'
                    tokenizer.selectNext()  # Consome ')'
                    if tokenizer.next.type == 'OPBRACE':  # Verifica '{'
                        block = Parser.parseBlock(tokenizer)  # Processa o bloco do loop
                    else:
                        block = Parser.parseStatement(tokenizer)
                    return While(condition, block)
                else:
                    raise Exception("Esperado ')' após a condição em WHILE_THE_MOON_SHINES")
            else:
                raise Exception("Esperado '(' após WHILE_THE_MOON_SHINES")

            
        
            
        elif tokenizer.next.type == 'CREATE':
            tokenizer.selectNext()
            if tokenizer.next.type == 'CHARACTER':  # Verifica se é a palavra 'character'
                return Parser.parseCharacter(tokenizer)
            elif tokenizer.next.type == 'SPELL':
                return Parser.parseSpell(tokenizer)
            elif tokenizer.next.type == 'MISSION':
                return Parser.parseMission(tokenizer)
            else:
                raise Exception("Esperado 'character' ou spell após 'CREATE'")

            

        elif tokenizer.next.type == 'SEMICOLON':
            # Ignora múltiplos pontos e vírgulas seguidos
            tokenizer.selectNext()
            return NoOp()

        elif tokenizer.next.type == 'EOF':
            return NoOp()
        
        elif tokenizer.next.type == 'OPBRACE':  # Início de um bloco aninhado
            return Parser.parseBlock(tokenizer)  # Chama parseBlock diretamente

        elif tokenizer.next.type == 'CREATE_DYNAMIC':
            tokenizer.selectNext()
            if tokenizer.next.type in ['CHARACTER', 'SPELL']:
                obj_type = tokenizer.next.type.lower()
                tokenizer.selectNext()
                if tokenizer.next.type == 'STRING':
                    name = tokenizer.next.value
                    tokenizer.selectNext()
                    block = Parser.parseBlock(tokenizer)
                    return CreateDynamic(obj_type, name, block)

        elif tokenizer.next.type == 'MISSION_STEP':
            tokenizer.selectNext()
            mission_name = tokenizer.next.value
            tokenizer.selectNext()
            if tokenizer.next.type == 'TO':
                tokenizer.selectNext()
                next_step = tokenizer.next.value
                tokenizer.selectNext()
                if tokenizer.next.type == 'SEMICOLON':
                    tokenizer.selectNext()
                    return AdvanceMission(mission_name, next_step)
                else:
                    raise Exception("Esperado ';' após 'TO'")
                
        elif tokenizer.next.type == 'CAST':
            tokenizer.selectNext()  # Consome "CAST"
            if tokenizer.next.type != 'SPELL':
                raise Exception("Esperado 'SPELL' após 'CAST'.")
            tokenizer.selectNext()  # Consome "SPELL"

            if tokenizer.next.type != 'STRING':
                raise Exception("Esperado o nome do feitiço.")
            spell_name = tokenizer.next.value
            tokenizer.selectNext()  # Consome o nome do feitiço

            if tokenizer.next.type != 'BY':
                raise Exception("Esperado 'BY' após o nome do feitiço.")
            tokenizer.selectNext()  # Consome "BY"

            if tokenizer.next.type != 'STRING':
                raise Exception("Esperado o nome do lançador.")
            caster = tokenizer.next.value
            tokenizer.selectNext()  # Consome o nome do lançador

            if tokenizer.next.type != 'ON':
                raise Exception("Esperado 'ON' após o lançador.")
            tokenizer.selectNext()  # Consome "ON"

            if tokenizer.next.type != 'STRING':
                raise Exception("Esperado o nome do alvo.")
            target = tokenizer.next.value
            tokenizer.selectNext()  # Consome o nome do alvo

            if tokenizer.next.type != 'SEMICOLON':
                raise Exception("Esperado ';' após o comando 'CAST'.")
            tokenizer.selectNext()  # Consome ";"

       
            return CastSpellNode(spell_name, caster, target)
        
        if tokenizer.next.type == 'CLBRACE':
            print("DEBUG: Encontrado CLBRACE. Finalizando bloco.")
            tokenizer.selectNext() 
            return NoOp()
        
        else:
            raise Exception(f"Instrução inválida no token: {tokenizer.next.type}, valor: {tokenizer.next.value}")


    @staticmethod
    def parseCharacter(tokenizer: Tokenizer):
        tokenizer.selectNext()  # Já sabemos que é 'PERSONAGEM'
        if tokenizer.next.type == 'STRING':  # Nome do personagem
            name = tokenizer.next.value
            tokenizer.selectNext()
            if tokenizer.next.type == 'OPBRACE':  # Abre o bloco '{'
                tokenizer.selectNext()
                if tokenizer.next.type == 'ATTRIBUTES':  # Verifica se é 'attributes'
                    tokenizer.selectNext()
                    if tokenizer.next.type == 'EQUAL':
                        tokenizer.selectNext()
                        attributes = {}
                        if tokenizer.next.type == 'OPBRACE':  # Abre os atributos '{'
                            tokenizer.selectNext()
                            while tokenizer.next.type != 'CLBRACE':  # Até fechar '}'
                                if tokenizer.next.type == 'IDENT':  # Nome do atributo
                                    attr_name = tokenizer.next.value  # Corrige aqui para usar o valor
                                    tokenizer.selectNext()
                                if tokenizer.next.type == 'EQUAL':
                                    tokenizer.selectNext()
                                    if tokenizer.next.type == 'INT':  # Valor do atributo
                                        attributes[attr_name] = tokenizer.next.value
                                        tokenizer.selectNext()
                                    elif tokenizer.next.type == 'OPEN_BRACKET':  # Lista
                                        attributes[attr_name] = Parser.parseFactor(tokenizer).Evaluate(SymbolTable())[0]

                                    else:
                                        raise Exception("Esperado um valor inteiro ou lista para o atributo")
                                    if tokenizer.next.type == 'SEMICOLON':  # Finaliza o atributo
                                        tokenizer.selectNext()
                                    else:
                                        raise Exception("Esperado ';' após o valor do atributo")
                                else:
                                    raise Exception("Esperado '=' após o nome do atributo")
                            tokenizer.selectNext()  # Fecha os atributos '}'
                            if tokenizer.next.type == 'CLBRACE':  # Fecha o bloco 'character'
                                tokenizer.selectNext()
                                return CharacterNode(name, attributes)
                            else:
                                raise Exception("Esperado '}' para fechar o bloco do personagem")
                        else:
                            raise Exception("Esperado '{' para abrir os atributos")
                    else:
                        raise Exception("Esperado '=' após 'attributes'")
                else:
                    raise Exception("Esperado 'attributes' após '{'")
            else:
                raise Exception("Esperado '{' após o nome do personagem")
        else:
            raise Exception("Esperado um nome para o personagem")

    @staticmethod
    def parseSpell(tokenizer: Tokenizer):
        
        if tokenizer.next.type != 'SPELL':
            raise Exception("Esperado 'spell' após 'CREATE'")
        
        tokenizer.selectNext()  # Consome "spell"
        if tokenizer.next.type != 'STRING':
            raise Exception("Esperado um nome para o feitiço")
        
        name = tokenizer.next.value
        tokenizer.selectNext()  # Consome o nome
        
        if tokenizer.next.type != 'OPBRACE':
            raise Exception("Esperado '{' após o nome do feitiço")
        tokenizer.selectNext()  # Consome '{'

        attributes = {}
        for attr in ['power', 'mana_cost', 'effect']:
            if tokenizer.next.type != 'IDENT' or tokenizer.next.value != attr:
                raise Exception(f"Esperado '{attr}' no feitiço")
            tokenizer.selectNext()  # Consome a chave

            if tokenizer.next.type != 'EQUAL':
                raise Exception(f"Esperado '=' após '{attr}'")
            tokenizer.selectNext()  # Consome '='

            if attr in ['power', 'mana_cost'] and tokenizer.next.type == 'INT':
                attributes[attr] = tokenizer.next.value
            elif attr == 'effect' and tokenizer.next.type == 'STRING':
                attributes[attr] = tokenizer.next.value
            else:
                raise Exception(f"Valor inválido para '{attr}'")
            
            tokenizer.selectNext()  # Consome o valor

            if tokenizer.next.type != 'SEMICOLON':
                raise Exception(f"Esperado ';' após '{attr}'")
            tokenizer.selectNext()  # Consome ';'

        if tokenizer.next.type != 'CLBRACE':
            raise Exception("Esperado '}' para fechar o bloco do feitiço")
        tokenizer.selectNext()  # Consome '}'

        print(f"Feitiço criado: {name}, atributos: {attributes}")

        return SpellNode(name, attributes['power'], attributes['mana_cost'], attributes['effect'])


    @staticmethod
    def parseMission(tokenizer: Tokenizer):
       
        if tokenizer.next.type != 'MISSION':
            raise Exception("Esperado 'mission' após 'CREATE'")
        
        tokenizer.selectNext()  # Consome "mission"
        if tokenizer.next.type != 'STRING':
            raise Exception("Esperado um nome para a missão")
        
        name = tokenizer.next.value
        tokenizer.selectNext()  # Consome o nome da missão
        
        if tokenizer.next.type != 'OPBRACE':
            raise Exception("Esperado '{' após o nome da missão")
        tokenizer.selectNext()  # Consome '{'

        # Inicializando os atributos da missão
        attributes = {}

        # Objetivo
        if tokenizer.next.type != 'OBJECTIVE':
            raise Exception("Esperado 'objective' na missão")
        tokenizer.selectNext()  # Consome "objective"

        if tokenizer.next.type != 'EQUAL':
            raise Exception("Esperado '=' após 'objective'")
        tokenizer.selectNext()  # Consome "="

        if tokenizer.next.type != 'STRING':
            raise Exception("Esperado uma string para 'objective'")
        attributes['objective'] = tokenizer.next.value
        tokenizer.selectNext()  # Consome o valor de 'objective'

        if tokenizer.next.type != 'SEMICOLON':
            raise Exception("Esperado ';' após 'objective'")
        tokenizer.selectNext()  # Consome ";"

        # Participantes
        if tokenizer.next.type != 'PARTICIPANTS':
            raise Exception("Esperado 'participants' na missão")
        tokenizer.selectNext()  # Consome "participants"

        if tokenizer.next.type != 'EQUAL':
            raise Exception("Esperado '=' após 'participants'")
        tokenizer.selectNext()  # Consome "="

        participants = Parser.parseFactor(tokenizer)  # Participantes são uma lista
        attributes['participants'], _ = participants.Evaluate(SymbolTable())

        if tokenizer.next.type != 'SEMICOLON':
            raise Exception("Esperado ';' após 'participants'")
        tokenizer.selectNext()  # Consome ";"

        # Recompensa
        if tokenizer.next.type != 'REWARD':
            raise Exception("Esperado 'reward' na missão")
        tokenizer.selectNext()  # Consome "reward"

        if tokenizer.next.type != 'EQUAL':
            raise Exception("Esperado '=' após 'reward'")
        tokenizer.selectNext()  # Consome "="

        reward = Parser.parseFactor(tokenizer)  # Recompensa é uma lista
        attributes['reward'], _ = reward.Evaluate(SymbolTable())

        if tokenizer.next.type != 'SEMICOLON':
            raise Exception("Esperado ';' após 'reward'")
        tokenizer.selectNext()  # Consome ";"

        # Localização
        if tokenizer.next.type != 'LOCATION':
            raise Exception("Esperado 'location' na missão")
        tokenizer.selectNext()  # Consome "location"

        if tokenizer.next.type != 'EQUAL':
            raise Exception("Esperado '=' após 'location'")
        tokenizer.selectNext()  # Consome "="

        if tokenizer.next.type != 'STRING':
            raise Exception("Esperado uma string para 'location'")
        attributes['location'] = tokenizer.next.value
        tokenizer.selectNext()  # Consome o valor de 'location'

        if tokenizer.next.type != 'SEMICOLON':
            raise Exception("Esperado ';' após 'location'")
        tokenizer.selectNext()  # Consome ";"

        if tokenizer.next.type != 'CLBRACE':
            raise Exception("Esperado '}' ao final da missão")
        tokenizer.selectNext()  # Consome '}'

        return MissionNode(name, attributes['objective'], attributes['participants'], attributes['reward'], attributes['location'])


    @staticmethod
    def parseBlock(tokenizer: Tokenizer):
        block = Block()  # Cria um novo bloco
        
        if tokenizer.next.type == 'OPBRACE':  # Verifica abertura de bloco
            tokenizer.selectNext()  # Consome '{'
            while tokenizer.next.type != 'CLBRACE':  # Enquanto não encontrar '}'
                if tokenizer.next.type == 'EOF':
                    raise Exception("Erro de sintaxe: Esperado '}' para fechar o bloco, mas EOF encontrado")
                block.children.append(Parser.parseStatement(tokenizer))  # Adiciona instruções
            tokenizer.selectNext()  # Consome '}'
        else:
            # Permite um único comando sem bloco
            block.children.append(Parser.parseStatement(tokenizer))

        print(f"DEBUG parseBlock: Bloco contém {len(block.children)} instruções")
        return block

    
    @staticmethod
    def parseProgram(tokenizer: Tokenizer):
        block = Block()  # Bloco principal do programa
        while tokenizer.next.type != 'EOF':
            block.children.append(Parser.parseStatement(tokenizer))
        return block

    
    
    class CreateDynamic(Node):
        def __init__(self, obj_type: str, name: str, block: Node):
            super().__init__('CREATE_DYNAMIC')
            self.obj_type = obj_type
            self.name = name
            self.children.append(block)

        def Evaluate(self, symbol_table: SymbolTable):
            block_result = self.children[0].Evaluate(symbol_table)
            symbol_table.set(self.name, block_result, self.obj_type)

    class IterateList(Node):
        def __init__(self, iterator: str, iterable: str, block: Node):
            super().__init__('ITERATE_LIST')
            self.iterator = iterator
            self.iterable = iterable
            self.children.append(block)

        def Evaluate(self, symbol_table: SymbolTable):
            iterable, _ = symbol_table.get(self.iterable)
            for item in iterable:
                symbol_table.set(self.iterator, item, "VALUE")
                self.children[0].Evaluate(symbol_table)

    class AdvanceMission(Node):
        def __init__(self, mission_name: str, next_step: str):
            super().__init__('ADVANCE_MISSION')
            self.mission_name = mission_name
            self.next_step = next_step

        def Evaluate(self, symbol_table: SymbolTable):
            mission, _ = symbol_table.get(self.mission_name)
            mission['objective'] = self.next_step
            symbol_table.set(self.mission_name, mission, "MISSION")



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


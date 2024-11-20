# KandraScript
Repositório criado para a realização da APS de Lógica Computacional

## Sobre o Projeto

### Tarefas:
1. Estruturar a linguagem segundo o padrão EBNF.
2. Utilizar as ferramentas Flex e Bison para realizar as etapas de Análise Léxica e Sintática. A saída
deve ser um arquivo C ou CPP compilado pelo Flex/Bison.
3. Utilizar alguma VM (LLVM, JVM, .net, etc) para interpretar um programa da sua linguagem.
4. Criar um conjunto de testes que demonstre as características da sua Linguagem.
5. Criar um vídeo de dois a cinco minutos apresentando sua linguagem (Motivação, Características,
Curiosidades e Execução de exemplos). Colocar link no README. Na apresentação, deixar claro
quais foram as modificações necessárias no compilador para adpatar adaptar a sua linguagem e novas
características adicionadas

## O KandraScript

A inspiração da criação dessa linguagem é baseada em livros de fantasia. A ideia do KandraScript é possibilitar a criação de ambientes, personagens, feitiços e até missões com um SQL/C inspired. Nosso nome é baseado em uma espécie de "ser" da séria MistBorn do Brandon Sanderson, os Kandras. Kandras são seres que conseguem remodelar seu corpo para parecer qualquer pessoa ou animal, por isso são ótimos espiões. 

## Gramática EBNF

LETTER = (A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z)

NUMBER = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

STRING = '"', {LETTER | " "}, '"'

IDENTIFIER = LETTER, {LETTER | NUMBER | "_"}

VALUE = STRING | NUMBER | LIST | SPELL | CHARACTER

LIST = "[", VALUE, {",", VALUE}, "]"

COMMENT = "//", {LETTER | NUMBER | " "}, "\n"

CHARACTER = "CREATE", "character", STRING, "{",
                "attributes", "=", "{",
                    "strength", "=", NUMBER, ";",
                    "magic", "=", NUMBER, ";",
                    "mana", "=", NUMBER, ";",
                    "inventory", "=", LIST, ";",
                "}", 
            "}"

SPELL = "CREATE" "spell", STRING, "{",
            "power", "=", NUMBER, ";",
            "mana_cost", "=", NUMBER, ";",
            "effect", "=", STRING, ";",
        "}"

MISSION = "CREATE" "mission", STRING, "{",
               "objective", "=", STRING, ";",
               "participants", "=", LIST, ";",
               "reward", "=", LIST, ";",
               "location", "=", STRING, ";",
           "}"

CAST = "CAST", "SPELL", STRING, "BY", STRING, "ON", STRING, "{",
           "ENCHANTED_IF", IDENTIFIER, ".", IDENTIFIER, ("<" | ">" | "="), NUMBER, "{",
                IDENTIFIER, ".", IDENTIFIER, ("+=" | "-="), IDENTIFIER, ".", IDENTIFIER, ";",
           "}",
           "OTHER_PATH", "{",
                "RESULT", "=", STRING, ";",
           "}",
       "}"

CONDITIONAL = "ENCHANTED_IF", CONDITION_BLOCK, "OTHER_PATH", BLOCK

CONDITION_BLOCK = IDENTIFIER, ".", IDENTIFIER, ("<" | ">" | "="), VALUE, "{", BLOCK, "}"

LOOP = "WHILE_THE_MOON_SHINES", CONDITION_BLOCK, BLOCK |
       "UNTIL_THE_FINAL_BATTLE", IDENTIFIER, "from", NUMBER, "to", NUMBER, BLOCK

BLOCK = "{", {STATEMENT}, "}"

STATEMENT = CHARACTER | SPELL | MISSION | CAST | CONDITIONAL | LOOP | ASSIGNMENT

ASSIGNMENT = IDENTIFIER, ".", IDENTIFIER, "=", VALUE, ";"

%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void yyerror(const char *s);
int yylex();
%}

%union {
    int num;
    char* str;
}

%token <str> IDENTIFIER
%token <num> NUMBER
%token CREATE CHARACTER ATTRIBUTES SPELL STRENGTH MAGIC MANA INVENTORY POWER MANA_COST EFFECT

%%

program:
    program_element program  
    |
;

program_element:
    character_def { printf("Personagem criado com sucesso!\n"); }
    | spell_def { printf("Feitiço criado com sucesso!\n"); }
;

character_def:
    CREATE CHARACTER IDENTIFIER '{' attributes '}' 
    {
        printf("Personagem: %s\n", $3);
    }
;

attributes:
    ATTRIBUTES '=' '{' STRENGTH '=' NUMBER ';'
    MAGIC '=' NUMBER ';'
    MANA '=' NUMBER ';'
    INVENTORY '=' list ';' '}' 
    {
        printf("Atributos do personagem:\n");
        printf("  Força: %d\n", $6);
        printf("  Magia: %d\n", $10);
        printf("  Mana: %d\n", $14);
        printf("  Inventário: Lista definida.\n");
    }
;

spell_def:
    CREATE SPELL IDENTIFIER '{' spell_attributes '}' 
    {
        printf("Feitiço: %s\n", $3);
    }
;

spell_attributes:
    POWER '=' NUMBER ';'
    MANA_COST '=' NUMBER ';'
    EFFECT '=' IDENTIFIER ';' 
    {
        printf("Atributos do feitiço:\n");
        printf("  Poder: %d\n", $3);
        printf("  Custo de Mana: %d\n", $7);
        printf("  Efeito: %s\n", $11);
    }
;

list:
    '[' items ']' 
    {
        printf("Lista de itens criada.\n");
    }
;

items:
    IDENTIFIER
    | IDENTIFIER ',' items
;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Erro: %s\n", s);
}

int main() {
    if (yyparse() == 0) {
        printf("Análise sintática concluída com sucesso.\n");
    } else {
        printf("Erro na análise sintática.\n");
    }
    return 0;
}

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
%token CREATE CHARACTER ATTRIBUTES STRENGTH MAGIC MANA INVENTORY

%%

program:
    character_def { printf("Personagem criado com sucesso!\n"); }
;

character_def:
    CREATE CHARACTER '"' IDENTIFIER '"' '{' attributes '}' 
    {
        printf("Personagem: %s\n", $4);
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

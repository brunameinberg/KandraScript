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
%token CREATE CHARACTER ATTRIBUTES MANA

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
    ATTRIBUTES '=' '{' MANA '=' NUMBER ';' '}' 
    {
        printf("Atributos: Mana = %d\n", $6);
        printf("Atributos processados com sucesso.\n");
    }
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

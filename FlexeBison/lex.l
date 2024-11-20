%{
#include "parser.tab.h" // Inclui os tokens gerados pelo Bison
#define YYSTYPE_IS_DECLARED 1
%}

%%

"CREATE"          { printf("Token: CREATE\n"); return CREATE; }
"character"       { printf("Token: CHARACTER\n"); return CHARACTER; }
"attributes"      { printf("Token: ATTRIBUTES\n"); return ATTRIBUTES; }
"strength"        { printf("Token: STRENGTH\n"); return STRENGTH; }
"magic"           { printf("Token: MAGIC\n"); return MAGIC; }
"mana"            { printf("Token: MANA\n"); return MANA; }
"inventory"       { printf("Token: INVENTORY\n"); return INVENTORY; }
"\""              { printf("Token: \"\n"); return '"'; }
"{"               { printf("Token: {\n"); return '{'; }
"}"               { printf("Token: }\n"); return '}'; }
"="               { printf("Token: =\n"); return '='; }
";"               { printf("Token: ;\n"); return ';'; }
"["               { printf("Token: [\n"); return '['; }
"]"               { printf("Token: ]\n"); return ']'; }
","               { printf("Token: ,\n"); return ','; }
[0-9]+            { printf("Token: NUMBER (%s)\n", yytext); yylval.num = atoi(yytext); return NUMBER; }
[a-zA-Z_][a-zA-Z0-9_]* { printf("Token: IDENTIFIER (%s)\n", yytext); yylval.str = strdup(yytext); return IDENTIFIER; }
[ \t]+            { /* Ignora espaços e tabulações */ }
[\n\r]+           { /* Ignora quebras de linha */ }
.                 { printf("Token não reconhecido: %s\n", yytext); }

%%

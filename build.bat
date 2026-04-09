@echo off

echo [1/2] Renderizando Quarto...
quarto render

echo [2/2] Compilando LaTeX y moviendo PDFs...
for /d %%T in (tp*) do (
    if exist %%T\%%T_enunciado.tex (
        echo --- %%T ---
        cd %%T
        lualatex -output-directory=..\build %%T_enunciado.tex
        cd ..
        if not exist docs\%%T mkdir docs\%%T
        copy build\%%T_enunciado.pdf docs\%%T\%%T_enunciado.pdf
    )
)

echo Limpiando temporales...
del /q build\*.aux build\*.log build\*.out build\*.toc build\*.synctex.gz

echo Listo.
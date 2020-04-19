@pdflatex -synctex=1 -interaction=nonstopmode -shell-escape "%1.tex" && pythontex "%1.dvi" && pdflatex -synctex=1 -interaction=nonstopmode -shell-escape "%1.tex"

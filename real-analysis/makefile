# Tools
LATEXMK = latexmk
RM = rm -f

# Targets
all: ra.dvi

# Rules
%.dvi: *.tex
	$(LATEXMK) -dvi -M -MP -MF $*.d $*

mostlyclean:
	$(LATEXMK) -silent -c
	$(RM) *.bbl

clean: mostlyclean
	$(LATEXMK) -silent -C
	$(RM) *.run.xml *.synctex.gz
	$(RM) *.d

.PHONY: all clean doc mostlyclean dvi


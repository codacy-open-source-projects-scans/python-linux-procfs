CTAGS_EXTRA := $(shell ctags --version 2>&1 | grep -iq universal && echo extras || echo extra)
.PHONY: tags
tags:
	ctags -R --$(CTAGS_EXTRA)=+fq --python-kinds=+cfmvi

.PHONY: cleantags
cleantags:
	rm -f tags

.PHONY: pyclean
pyclean:
	@find . -type f \( -name \*~ -o -name \*.pyc \) -delete

clean: pyclean cleantags

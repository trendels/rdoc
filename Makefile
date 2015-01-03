python_modules :=	\
	rhino					\
	rhino.mapper	 		\
	rhino.resource 			\
	rhino.static 			\
	rhino.request 			\
	rhino.response 			\
	rhino.util 				\
	rhino.test				\
	rhino.errors			\
	rhino.ext.jinja2		\
	rhino.ext.session		\
	rhino.ext.sqlalchemy	\

pandoc_bin := pandoc
pandoc_opts := --smart --indented-code-classes=python --standalone \
	--section-divs --css=../style.css --filter=filters/highlight_builtins.py
pandoc_from := markdown+compact_definition_lists
pandoc_to := html5

mkd_files  := $(python_modules:%=build/%.mkd)
html_files := $(python_modules:%=build/%.html)

all: rules $(html_files)

rules:
	python make_rules.py $(python_modules) > $@

-include rules

%.html: %.mkd
	$(pandoc_bin) $(pandoc_opts) --from=$(pandoc_from) --to=$(pandoc_to) $< > $@

clean:
	rm -rf rules build/

.PHONY: all clean

.PRECIOUS: %.mkd

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
	--section-divs --css=../style.css \
	--filter=filters/highlight_builtins.py \
	--filter=filters/autolink.py
pandoc_from := markdown+compact_definition_lists
pandoc_to := html5

link_files := $(python_modules:%=build/%.links)
html_files := $(python_modules:%=build/%.html)

all: links $(html_files)

rules:
	python make_rules.py $(python_modules) > $@

links: $(link_files)
	cat build/*.links | sort > links

-include rules

%.html: %.mkd
	LINKS=links $(pandoc_bin) $(pandoc_opts) --from=$(pandoc_from) --to=$(pandoc_to) $< > $@

clean:
	rm -rf rules links build/

.PHONY: all clean

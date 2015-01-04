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
	--section-divs \
	--filter=filters/highlight_builtins.py \
	--filter=filters/autolink.py
pandoc_from := markdown+compact_definition_lists
pandoc_to := html5

api_links := $(python_modules:%=build/api/%.links)
api_html := $(python_modules:%=build/api/%.html)
api_html += build/api/index.html

src_files := $(shell find src/ -name '*.mkd')
doc_html := $(src_files:src/%.mkd=build/%.html)

all: links build/style.css $(api_html) $(doc_html)

rules:
	python make_rules.py $(python_modules) > $@

links: $(api_links)
	cat build/api/*.links | sort > links

build/api/index.mkd:
	python make_index.py $(python_modules) > $@

build/style.css: style.css
	mkdir -p build
	cp style.css build/

-include rules

build/%.html: src/%.mkd
	@mkdir -p $(dir $@)
	$(pandoc_bin) $(pandoc_opts) --metadata=links:./links --metadata=filename:$@ --css=$(shell python relpath.py build/style.css $@) --from=$(pandoc_from) --to=$(pandoc_to) $< > $@

%.html: %.mkd
	$(pandoc_bin) $(pandoc_opts) --metadata=links:./links --metadata=filename:$@ --css=$(shell python relpath.py build/style.css $@) --from=$(pandoc_from) --to=$(pandoc_to) $< > $@

clean:
	rm -rf rules links build/

.PHONY: all clean

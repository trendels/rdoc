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
api_html := $(python_modules:%=build/html/api/%.html)
api_html += build/html/api/index.html

src_files := $(shell find src/ -name '*.mkd')
doc_html := $(src_files:src/%.mkd=build/html/%.html)

static_src := $(shell find static/ -type f)
static_files := $(static_src:static/%=build/html/static/%)

all: build/links $(static_files) $(api_html) $(doc_html)

build/rules:
	@mkdir -p $(dir $@)
	python make_rules.py $(python_modules) > $@

build/links: $(api_links)
	@mkdir -p $(dir $@)
	cat build/api/*.links | sort > build/links

build/api/index.mkd:
	@mkdir -p $(dir $@)
	python make_index.py $(python_modules) > $@

build/html/static/%: static/%
	@mkdir -p $(dir $@)
	cp $< $@

-include build/rules

build/html/%.html: src/%.mkd
	@mkdir -p $(dir $@)
	$(pandoc_bin) $(pandoc_opts) --metadata=link_prefix:$(shell python relpath.py build/html $@)/ --metadata=links:./build/links --css=static/style.css --from=$(pandoc_from) --to=$(pandoc_to) --template=pandoc.html5 $< meta.yml > $@

build/html/api/%.html: build/api/%.mkd
	@mkdir -p $(dir $@)
	$(pandoc_bin) $(pandoc_opts) --metadata=link_prefix:$(shell python relpath.py build/html $@)/ --metadata=links:./build/links --css=static/style.css --from=$(pandoc_from) --to=$(pandoc_to) --template=pandoc.html5 $< meta.yml > $@

clean:
	rm -rf build/

.PHONY: all clean

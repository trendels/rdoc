python_modules := $(shell egrep -v '^\#' modules)

pandoc_bin := pandoc
pandoc_opts := --standalone \
	--section-divs --toc \
	--filter=filters/highlight_builtins.py \
	--filter=filters/autolink.py
pandoc_from := markdown+compact_definition_lists
pandoc_to := html5
pandoc_template := ./templates/rdoc

# Additional pandoc options when building module documentation
pandoc_module_opts := --indented-code-classes=python

# Additional pandoc options when building other documentation
pandoc_doc_opts :=

module_links := $(python_modules:%=build/modules/%.links)
module_html := $(python_modules:%=build/html/modules/%.html)
module_html += build/html/modules/index.html

src_files := $(shell find src/ -name '*.mkd')
doc_html := $(src_files:src/%.mkd=build/html/%.html)

static_src := $(shell find static/ -type f)
static_files := $(static_src:static/%=build/html/static/%)

all: build/links.yml $(static_files) $(module_html) $(doc_html)

build/rules: modules
	@mkdir -p $(dir $@)
	python bin/make_rules.py $(python_modules) > $@

build/links.yml: $(module_links)
	@mkdir -p $(dir $@)
	python bin/make_links.py build/modules/*.links > $@

build/modules/index.mkd: modules
	@mkdir -p $(dir $@)
	python bin/make_index.py $(python_modules) > $@

build/html/static/%: static/%
	@mkdir -p $(dir $@)
	cp $< $@

-include build/rules

build/html/%.html: src/%.mkd meta.yml modules
	@mkdir -p $(dir $@)
	$(pandoc_bin) $(pandoc_opts) $(pandoc_doc_opts) --metadata=link_prefix:$(shell python bin/relpath.py build/html $@)/ --css=static/style.css --from=$(pandoc_from) --to=$(pandoc_to) --template=$(pandoc_template) $< meta.yml build/links.yml > $@

build/html/modules/%.html: build/modules/%.mkd meta.yml modules
	@mkdir -p $(dir $@)
	$(pandoc_bin) $(pandoc_opts) $(pandoc_module_opts) --metadata=link_prefix:$(shell python bin/relpath.py build/html $@)/ --css=static/style.css --from=$(pandoc_from) --to=$(pandoc_to) --template=$(pandoc_template) $< meta.yml build/links.yml > $@

clean:
	rm -rf build/

.PHONY: all clean

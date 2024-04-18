CWD = $(shell pwd)

PROJECTS = vsg-models/vsg-themes vsg-models/vsg-clips vsg-models/vsg-gen vsg-utils
DOC_PROJECTS = docs
BIN_PROJECTS = $(PROJECTS)

documentation:
	for project in $(DOC_PROJECTS); do \
		cd $$project && $(MAKE) documentation && cd $(CWD) ; \
	done

clean_documentation:
	cd $(DOC_PROJECTS) && $(MAKE) clean && cd $(CWD)

clean: clean_documentation
	for project in $(BIN_PROJECTS); do \
		cd $$project && $(MAKE) clean && cd $(CWD) ; \
	done

install: install-project-components
	@echo "Downloading required files... "
	dvc pull

install-project-components:
	for project in $(PROJECTS); do \
		cd $$project && $(MAKE) install && cd $(CWD) ; \
	done

run-experiment-standalone: install
	@echo "######################### Generating themes"
	python vsg-models/vsg-themes/vsg_themes/theme_extractor.py
	@echo "######################### Generating clips"
	python vsg-models/vsg-clips/vsg_clips/clips_generator.py
	@echo "######################### Generating blog"
	python vsg-models/vsg-gen/vsg_gen/blog.py

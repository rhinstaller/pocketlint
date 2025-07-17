PKGNAME=pocketlint
VERSION=$(shell awk '/Version:/ { print $$2 }' python-$(PKGNAME).spec)

PREFIX=/usr

PYTHON?=python3

build:
	$(PYTHON) setup.py build

check:
	@echo "*** Running pylint to verify source ***"
	PYTHONPATH=./build/lib $(PYTHON) tests/pylint/runpylint.py

clean:
	-rm pylint-log
	$(PYTHON) setup.py -q clean --all

install:
	$(PYTHON) -m pip install . --root=$(DESTDIR) --no-deps --no-build-isolation

tag:
	git tag -a -m "Tag as $(VERSION)" -f $(VERSION)
	@echo "Tagged as $(VERSION)"

archive: check tag
	git archive --format=tar --prefix=$(PKGNAME)-$(VERSION)/ $(VERSION) > $(PKGNAME)-$(VERSION).tar
	gzip -9 $(PKGNAME)-$(VERSION).tar
	@echo "The archive is in $(PKGNAME)-$(VERSION).tar.gz"

release-pypi:
	if ! $(PYTHON) -m build --sdist --wheel; then \
		echo ""; \
		echo Distribution package build failed! Please verify that you have \'python3-build\' and \'python3-setuptools\' installed. >&2; \
		exit 1; \
	fi
	if ! $(PYTHON) -m twine upload dist/*; then \
		echo ""; \
		echo Package upload failed! Make sure the \'twine tool\' is installed and you are registered >&2; \
		exit 1; \
	fi

local:
	@rm -rf $(PKGNAME)-$(VERSION).tar.gz
	@rm -rf /tmp/$(PKGNAME)-$(VERSION) /tmp/$(PKGNAME)
	@dir=$$PWD; cp -a $$dir /tmp/$(PKGNAME)-$(VERSION)
	@cd /tmp/$(PKGNAME)-$(VERSION) ; $(PYTHON) -m build --sdist --outdir .
	@cp /tmp/$(PKGNAME)-$(VERSION)/$(PKGNAME)-$(VERSION).tar.gz .
	@rm -rf /tmp/$(PKGNAME)-$(VERSION)
	@echo "The archive is in $(PKGNAME)-$(VERSION).tar.gz"

rpmlog:
	@git log --pretty="format:- %s (%ae)" $(VERSION).. |sed -e 's/@.*)/)/' | grep -v "Merge pull request"

bumpver:
	@NEWSUBVER=$$((`echo $(VERSION) |cut -d . -f 2` + 1)) ; \
	NEWVERSION=`echo $(VERSION).$$NEWSUBVER |cut -d . -f 1,3` ; \
	DATELINE="* `LC_ALL=C.UTF-8 date "+%a %b %d %Y"` `git config user.name` <`git config user.email`> - $$NEWVERSION-1"  ; \
	cl=`grep -n %changelog python-${PKGNAME}.spec |cut -d : -f 1` ; \
	tail --lines=+$$(($$cl + 1)) python-${PKGNAME}.spec > speclog ; \
	(head -n $$cl python-${PKGNAME}.spec ; echo "$$DATELINE" ; make --quiet rpmlog 2>/dev/null ; echo ""; cat speclog) > python-${PKGNAME}.spec.new ; \
	mv python-${PKGNAME}.spec.new python-${PKGNAME}.spec ; rm -f speclog ; \
	sed -i "s/Version:   $(VERSION)/Version:   $$NEWVERSION/" python-${PKGNAME}.spec ; \
	sed -i "s/version='$(VERSION)'/version='$$NEWVERSION'/" setup.py

ci:
	PYTHONPATH=. tests/pylint/runpylint.py

.PHONY: check clean install tag archive local

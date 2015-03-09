PKGNAME=pocketlint
VERSION=$(shell awk '/Version:/ { print $$2 }' python3-$(PKGNAME).spec)

PREFIX=/usr

PYTHON?=python3

build:
	$(PYTHON) setup.py build

check:
	@echo "*** Running pylint to verify source ***"
	PYTHONPATH=./build/lib tests/pylint/runpylint.py

clean:
	-rm pylint-log
	$(PYTHON) setup.py -q clean --all

install:
	$(PYTHON) setup.py install --root=$(DESTDIR) --skip-build

tag:
	git tag -a -m "Tag as $(VERSION)" -f $(VERSION)
	@echo "Tagged as $(VERSION)"

archive: check tag
	git archive --format=tar --prefix=$(PKGNAME)-$(VERSION)/ $(VERSION) > $(PKGNAME)-$(VERSION).tar
	gzip -9 $(PKGNAME)-$(VERSION).tar
	@echo "The archive is in $(PKGNAME)-$(VERSION).tar.gz"

local:
	@rm -rf $(PKGNAME)-$(VERSION).tar.gz
	@rm -rf /tmp/$(PKGNAME)-$(VERSION) /tmp/$(PKGNAME)
	@dir=$$PWD; cp -a $$dir /tmp/$(PKGNAME)-$(VERSION)
	@cd /tmp/$(PKGNAME)-$(VERSION) ; $(PYTHON) setup.py -q sdist
	@cp /tmp/$(PKGNAME)-$(VERSION)/dist/$(PKGNAME)-$(VERSION).tar.gz .
	@rm -rf /tmp/$(PKGNAME)-$(VERSION)
	@echo "The archive is in $(PKGNAME)-$(VERSION).tar.gz"

rpmlog:
	@git log --pretty="format:- %s (%ae)" $(VERSION).. |sed -e 's/@.*)/)/'
	@echo

bumpver:
	@NEWSUBVER=$$((`echo $(VERSION) |cut -d . -f 2` + 1)) ; \
	NEWVERSION=`echo $(VERSION).$$NEWSUBVER |cut -d . -f 1,3` ; \
	DATELINE="* `date "+%a %b %d %Y"` `git config user.name` <`git config user.email`> - $$NEWVERSION-1"  ; \
	cl=`grep -n %changelog python3-${PKGNAME}.spec |cut -d : -f 1` ; \
	tail --lines=+$$(($$cl + 1)) python3-${PKGNAME}.spec > speclog ; \
	(head -n $$cl python3-${PKGNAME}.spec ; echo "$$DATELINE" ; make --quiet rpmlog 2>/dev/null ; echo ""; cat speclog) > python3-${PKGNAME}.spec.new ; \
	mv python3-${PKGNAME}.spec.new python3-${PKGNAME}.spec ; rm -f speclog ; \
	sed -i "s/Version:   $(VERSION)/Version:   $$NEWVERSION/" python3-${PKGNAME}.spec ; \
	sed -i "s/version='$(VERSION)'/version='$$NEWVERSION'/" setup.py

.PHONY: check clean install tag archive local

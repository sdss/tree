# !usr/bin/env python
# -*- coding: utf-8 -*-
#

from sphinx.testing.path import path
import pytest


@pytest.fixture(scope="session")
def rootdir():
    return path(__file__).parent.abspath() / "roots"


@pytest.mark.sphinx(testroot="docutree")
def test_docutree(app, status, warning):
    app.builder.build_all()

    dmdoc = app.srcdir / "_build/html/contents.html"
    assert dmdoc.exists()

    tt = dmdoc.read_text()

    # check for datamodel directive stuff
    assert '<section id="datamodel">' in tt
    assert '<h2>SDSS<a class="headerlink" href="#sdss" title="Link to this heading">¶</a></h2>' in tt
    assert "<td><p>MANGA_SPECTRO_REDUX</p></td>\n<td><p>/dr17/manga/spectro/redux</p></td>" in tt

    # check for changelog directive stuff
    assert '<section id="changelog">' in tt
    assert 'Changes: DR17 from DR16' in tt
    assert '<p>New <span class="maroon">MANGA_AGN</span>: /dr17/manga/agn</p></li>\n<li><p>' in tt
    assert "<dt><strong>New Paths:</strong></dt><dd><ul>" in tt
    assert '<li><p><span class="maroon">apogee_astronn</span>:  $APOGEE_ASTRONN/apogee_astroNN-{release}.fits</p></li>' in tt

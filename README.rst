| |workflow_pytests| |workflow_checks| |coveralls| |docs| |packaging|
| |lgt_general| |lgt_alerts| |codacy| |requires|

\


| |version| |wheel| |supported-versions| |supported-implementations|
| |commits-since| |licence| |code_Style| |zenodo|


------------------------------------------------

\

.. image:: https://raw.githubusercontent.com/reegis/deflex/master/docs/images/logo_deflex_big.svg
    :target: https://github.com/reegis/deflex
    :width: 600pt

deflex - flexible multi-regional energy system model for heat, power and mobility
=================================================================================

* Multi sectoral energy system of Germany/Europe
* Dispatch optimisation
* Start with basic scenarios
* Highly configurable and adaptable


.. |docs| image:: https://readthedocs.org/projects/deflex/badge/?style=flat
    :target: https://readthedocs.org/projects/deflex
    :alt: Documentation Status

.. |workflow_pytests| image:: https://github.com/reegis/deflex/workflows/tox%20pytests/badge.svg?branch=master
    :target: https://github.com/reegis/deflex/actions?query=workflow%3A%22tox+pytests%22

.. |workflow_checks| image:: https://github.com/reegis/deflex/workflows/tox%20checks/badge.svg?branch=master
    :target: https://github.com/reegis/deflex/actions?query=workflow%3A%22tox+checks%22

.. |packaging| image:: https://github.com/reegis/deflex/workflows/packaging/badge.svg?branch=master
    :target: https://github.com/reegis/deflex/actions?query=workflow%3Apackaging

.. |requires| image:: https://requires.io/github/reegis/deflex/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/reegis/deflex/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/github/reegis/deflex/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://coveralls.io/github/reegis/deflex?branch=master

.. |version| image:: https://img.shields.io/pypi/v/deflex.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/deflex

.. |wheel| image:: https://img.shields.io/pypi/wheel/deflex.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/deflex

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/deflex.svg
    :alt: Supported versions
    :target: https://pypi.org/project/deflex

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/deflex.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/deflex

.. |commits-since| image:: https://img.shields.io/github/commits-since/reegis/deflex/v0.2.0.svg
    :alt: Commits since latest release
    :target: https://github.com/reegis/deflex/compare/v0.2.0...master

.. |lgt_general| image:: https://img.shields.io/lgtm/grade/python/g/reegis/deflex.svg?logo=lgtm&logoWidth=18
    :target: https://lgtm.com/projects/g/reegis/deflex/context:python

.. |lgt_alerts| image:: https://img.shields.io/lgtm/alerts/g/reegis/deflex.svg?logo=lgtm&logoWidth=18
    :target: https://lgtm.com/projects/g/reegis/deflex/alerts/

.. |code_style| image:: https://img.shields.io/badge/automatic%20code%20style-black-blueviolet
    :target: https://black.readthedocs.io/en/stable/

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/b91ed03ffa8e407ab3e69a10c5115efa
   :target: https://app.codacy.com/gh/reegis/deflex?utm_source=github.com&utm_medium=referral&utm_content=reegis/deflex&utm_campaign=Badge_Grade

.. |licence| image:: https://img.shields.io/badge/licence-MIT-blue
    :target: https://spdx.org/licenses/MIT.html

.. |zenodo| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3572594.svg
   :target: https://doi.org/10.5281/zenodo.3572594


Installation
============

The following line will install the basic version. Some functions depend on further packages, see below to install additional requirements::

    pip install deflex

To run older scenarios you can install the old stable phd version::

    pip install https://github.com/reegis/deflex/archive/phd.zip


Installation of a solver (mandatory)
------------------------------------

To solve an energy system a linear solver has to be installed. For the
communication with the solver `Pyomo` is used. Have a look at the `Pyomo docs <https://pyomo.readthedocs.io/en/stable/solving_pyomo_models.html#supported-solvers>`_ to learn about which solvers are supported.

The default solver is the CBC solver. Go to the `oemof.solph documentation
<https://oemof-solph.readthedocs.io/en/latest/readme.html#installing-a-solver>`_
to get help for the solver installation.


Additional requirements (optional)
----------------------------------

The basic installation can be used to compute scenarios (csv, xls, xlsx). For
some functions additional packages are needed.

1. To run the example with all plots you need the following packages:
    * pygeos (spatial operations)
    * geopandas (maps)
    * descartes (plot maps with matplotlib)
    * lmfit (linear fit)
    * matplotlib (plotting)
    * requests (download example files)

    ``pip install deflex[example]``

2. To use the maps of the polygons, transmission lines etc.:
    * pygeos (spatial operations)
    * geopandas (maps)

    ``pip install deflex[map]``

3. To develop deflex:
    * pytest
    * sphinx
    * sphinx_rtd_theme
    * pygeos
    * geopandas
    * requests

    ``pip install deflex[dev]``


Basic usage
===========

.. code-block:: python

    scenario = "/path/to/my/scenario.xls"
    main.model_scenario(scenario)


Use example
===========

1. Run ``pip install deflex[example]``
2. Create a local directory (e.g. /home/user/deflex_examples).
3. Download the
   `example <https://raw.githubusercontent.com/reegis/deflex/master/examples/examples.py>`_
   to this new directory.
4. Now execute the example file. The script will download some example
   scenarios with results and show some exemplary plots.
5. A directory "deflex_examples" will be created in you home directory. Use
   ``print(os.path.expanduser("~"))`` to find out where your home directory is
   located. If you want to change it replace the base path in the example:

.. code-block:: diff

    - BASEPATH = os.path.join(os.path.expanduser("~"), "deflex_examples")
    + BASEPATH = "/your/favoured/path/"

Documentation
=============


https://deflex.readthedocs.io/

The `documentation of deflex <https://deflex.readthedocs.io/en/latest/>`_ is powered by readthedocs.

Go to the `download page <http://readthedocs.org/projects/deflex/downloads/>`_ to download different versions and formats (pdf, html, epub) of the documentation.



Contributing
==============

We are warmly welcoming all who want to contribute to the deflex library.


Citing deflex
========================

Go to the `Zenodo page of deflex <https://doi.org/10.5281/zenodo.3572594>`_ to find the DOI of your version. To cite all deflex versions use:

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3572594.svg
   :target: https://doi.org/10.5281/zenodo.3572594

Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox

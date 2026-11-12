#
# Conditional build:
%bcond_without	doc	# mdBook documentation
%bcond_without	tests	# unit tests

Summary:	A repository of test results
Summary(pl.UTF-8):	Repozytorium wyników testów
Name:		python3-testrepository
Version:	0.0.22
Release:	1
License:	Apache v2.0 or BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/testrepository/
Source0:	https://pypi.org/packages/source/t/testrepository/testrepository-%{version}.tar.gz
# Source0-md5:	02b83bc2426b5a124c12e93065c8a92d
URL:		https://launchpad.net/testrepository
BuildRequires:	python3-build
BuildRequires:	python3-hatch-vcs
BuildRequires:	python3-hatchling
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools >= 1:61
%if %{with tests}
BuildRequires:	python3-fixtures
BuildRequires:	python3-iso8601
BuildRequires:	python3-subunit >= 0.0.18
BuildRequires:	python3-testresources
BuildRequires:	python3-testscenarios
BuildRequires:	python3-testtools >= 0.9.30
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	mdbook
%endif
Requires:	python3-modules >= 1:3.2
Conflicts:	python-testrepository < 0.0.20-12
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This project provides a database of test results which can be used as
part of developer workflow to ensure/check things like:
- No commits without having had a test failure, test fixed cycle.
- No commits without new tests being added.
- What tests have failed since the last commit (to run just a subset).
- What tests are currently failing and need work.

Test results are inserted using subunit (and thus anything that can
output subunit or be converted into a subunit stream can be accepted).

%description -l pl.UTF-8
Ten projekt zapewnia bazę danych wyników testów, które można używać
jako część ciągu pracy programistów, mającą na celu
zapewnienie/sprawdzenie, że:
- nie wejdą zmiany bez naprawienia nieprzechodzących testów
- nie wejdą zmiany bez dodania nowych testów
- które testy nie powiodły się od ostatnich zmian (aby uruchomić
  podzbiór)
- które testy obecnie nie przechodzą i wymagają pracy

Wyniki testów są wprowadzane przy użyciu modułu subunit (więc może być
przyjęte wszystko, co na wyjściu ma format subunit albo może być
przekonwertowane do takiego strumienia).

%package apidocs
Summary:	API documentation for Python testrepository module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona testrepository
Group:		Documentation

%description apidocs
API documentation for Python testrepository module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona testrepository.

%prep
%setup -q -n testrepository-%{version}

%build
%py3_build_pyproject

%if %{with tests}
# tests create temporary repositories in $HOME
install -d test-home
HOME=$(pwd)/test-home \
PYTHONPATH=$(pwd) \
%{__python3} -m testtools.run testrepository.tests.test_suite
%endif

%if %{with doc}
mdbook build doc
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%{__mv} $RPM_BUILD_ROOT%{_bindir}/testr{,-3}
ln -sf testr-3 $RPM_BUILD_ROOT%{_bindir}/testr

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/testrepository/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Apache-2.0 BSD COPYING NEWS README.md
%attr(755,root,root) %{_bindir}/testr
%attr(755,root,root) %{_bindir}/testr-3
%{py3_sitescriptdir}/testrepository
%{py3_sitescriptdir}/testrepository-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/book/*
%endif

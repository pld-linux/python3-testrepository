#
# Conditional build:
%bcond_with	tests	# testr (python 2 only because of bzr dependency, broken as of 0.0.20)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	A repository of test results
Summary(pl.UTF-8):	Repozytorium wyników testów
Name:		python-testrepository
Version:	0.0.20
Release:	9
License:	Apache v2.0 or BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/testrepository/
Source0:	https://pypi.python.org/packages/source/t/testrepository/testrepository-%{version}.tar.gz
# Source0-md5:	f648b0aceeca4fcd5f8a62eeedea289b
URL:		https://launchpad.net/testrepository
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-bzr
BuildRequires:	python-fixtures
BuildRequires:	python-pytz
BuildRequires:	python-subunit >= 0.0.18
BuildRequires:	python-testresources
BuildRequires:	python-testscenarios
BuildRequires:	python-testtools >= 0.9.30
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
# no bzr for python3, so no tests
%if %{with python3_tests}
BuildRequires:	python3-bzr
BuildRequires:	python3-fixtures
BuildRequires:	python3-pytz
BuildRequires:	python3-subunit >= 0.0.18
BuildRequires:	python3-testresources
BuildRequires:	python3-testscenarios
BuildRequires:	python3-testtools >= 0.9.30
%endif
%endif
Requires:	python-modules >= 1:2.6
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

%package -n python3-testrepository
Summary:	A repository of test results
Summary(pl.UTF-8):	Repozytorium wyników testów
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2

%description -n python3-testrepository
This project provides a database of test results which can be used as
part of developer workflow to ensure/check things like:
- No commits without having had a test failure, test fixed cycle.
- No commits without new tests being added.
- What tests have failed since the last commit (to run just a subset).
- What tests are currently failing and need work.

Test results are inserted using subunit (and thus anything that can
output subunit or be converted into a subunit stream can be accepted).

%description -n python3-testrepository -l pl.UTF-8
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

%prep
%setup -q -n testrepository-%{version}

%build
%if %{with python2}
%py_build
%{?with_tests:%{__python} testr init && %{__python} testr run}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%{?with_python3_tests:%{__python3} testr init && %{__python3} testr run}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install
%{__mv} $RPM_BUILD_ROOT%{_bindir}/testr{,-2}

%py_postclean
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/testrepository/tests
%endif

%if %{with python3}
%py3_install
%{__mv} $RPM_BUILD_ROOT%{_bindir}/testr{,-3}

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/testrepository/tests
%endif

%if %{with python2}
ln -sf testr-2 $RPM_BUILD_ROOT%{_bindir}/testr
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc BSD COPYING NEWS README.txt doc
%attr(755,root,root) %{_bindir}/testr
%attr(755,root,root) %{_bindir}/testr-2
%{py_sitescriptdir}/testrepository
%{py_sitescriptdir}/testrepository-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-testrepository
%defattr(644,root,root,755)
%doc BSD COPYING NEWS README.txt doc
%attr(755,root,root) %{_bindir}/testr-3
%{py3_sitescriptdir}/testrepository
%{py3_sitescriptdir}/testrepository-%{version}-py*.egg-info
%endif

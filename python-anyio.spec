%define module anyio
# disabled tests for python upgrade
%bcond tests 0

Summary:	High level compatibility layer for multiple asynchronous event loop implementations
Name:		python-anyio
Version:	4.12.0
Release:	1
License:	MIT
Group:		Development/Python
Url:		https://github.com/agronholm/anyio
Source:		https://files.pythonhosted.org/packages/source/a/%{module}/%{module}-%{version}.tar.gz
# to fix tests
#Patch0:		anyio-3.7.1-fix-test-symlink.patch

BuildRequires:	pkgconfig(python3)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(psutil)
BuildRequires:	python%{pyver}dist(idna)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(setuptools-scm)
BuildRequires:	python%{pyver}dist(toml)
BuildRequires:	python%{pyver}dist(wheel)
BuildRequires:	python%{pyver}dist(trio)

# for tests
%if %{with tests}
BuildRequires:	python%{pyver}dist(pytest)
BuildRequires:	python%{pyver}dist(coverage)
BuildRequires:	python%{pyver}dist(cython)
BuildRequires:	python%{pyver}dist(hypothesis)
BuildRequires:	python%{pyver}dist(pluggy)
BuildRequires:	python%{pyver}dist(pytest-mock)
BuildRequires:	python%{pyver}dist(sniffio)
BuildRequires:	python%{pyver}dist(trustme)
BuildRequires:	python%{pyver}dist(uvloop)
%endif

BuildArch:	noarch
Provides:	python%{pyver}dist(%{module}) = %{version}-%{release}

%description
AnyIO is an asynchronous networking and concurrency library that works on top
of either asyncio or trio. It implements trio-like structured concurrency (SC)
on top of asyncio, and works in harmony with the native SC of trio itself.

Applications and libraries written against AnyIO's API will run unmodified on
either asyncio or trio. AnyIO can also be adopted into a library or application
incrementally – bit by bit, no full refactoring necessary. It will blend in with
native libraries of your chosen backend.

%prep
%autosetup -n %{module}-%{version} -p1
# Remove upstream's egg-info
rm -vrf src/%{module}.egg-info
# disable coverage test requirement
sed -e '/"coverage/d' -i pyproject.toml

%build
%py_build

%install
%py_install

%if %{with tests}
%check
# we dont have network access to run these tests
ignore="${ignore-} --ignore=tests/test_sockets.py --ignore=tests/streams/test_tls.py"

%{__python} -m pytest -v -Wdefault -m "not network" ${ignore-} -k "not ((trio and exception_group) or test_properties) and not test_autouse_async_fixture and not test_cancel_scope_in_asyncgen_fixture and not test_module_scoped_task_group_fixture"
%endif

%files
%license LICENSE
%doc README.rst
%{python_sitelib}/%{module}-%{version}.dist-info
%{python_sitelib}/%{module}/*.py
%{python_sitelib}/%{module}/*.typed
%{python_sitelib}/%{module}/__pycache__/*.cpython-3*.pyc
%{python_sitelib}/%{module}/*/*.py
%{python_sitelib}/%{module}/*/__pycache__/*.cpython-3*.pyc

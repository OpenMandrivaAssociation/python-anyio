%define module anyio

Summary:	High level compatibility layer for multiple asynchronous event loop implementations
Name:		python-%{module}
Version:	3.7.1
Release:	1
License:	MIT
Group:		Development/Python
Url:		https://github.com/agronholm/%{module}
Source:		https://files.pythonhosted.org/packages/source/a/%{module}/%{module}-%{version}.tar.gz

BuildRequires:	pkgconfig(python3)
BuildRequires:	python-pip
BuildRequires:	python-pytest
BuildRequires:	python-setuptools
BuildRequires:	python-setuptools_scm
BuildRequires:	python-tomli
BuildRequires:	python-wheel

BuildArch:	noarch

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

%build
%py_build

%install
%py_install


%files
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{module}-%{version}.dist-info
%{python3_sitelib}/%{module}/*.py
%{python3_sitelib}/%{module}/*.typed
%{python3_sitelib}/%{module}/__pycache__/*.cpython-3*.pyc
%{python3_sitelib}/%{module}/*/*.py
%{python3_sitelib}/%{module}/*/__pycache__/*.cpython-3*.pyc

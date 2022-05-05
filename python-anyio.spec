%define module anyio

Summary:	Asynchronous concurrency and networking framework working on top of either trio or asyncio in python
Name:		python-%{module}
Version:	3.5.0
Release:	1
License:	MIT
Group:		Development/Python
Url:		https://github.com/agronholm/%{module}
Source:		https://files.pythonhosted.org/packages/source/a/%{module}/%{module}-%{version}.tar.gz

BuildRequires:	pkgconfig(python3)
BuildRequires:	python3dist(pip)
BuildRequires:	python3dist(setuptools)
BuildRequires:	python3dist(setuptools-scm)
BuildRequires:	python3dist(wheel)

BuildArch:	noarch

%description
AnyIO is an asynchronous networking and concurrency library that works on top
of either asyncio or trio. It implements trio-like structured concurrency (SC)
on top of asyncio, and works in harmony with the native SC of trio itself.

Applications and libraries written against AnyIO's API will run unmodified on
either asyncio or trio. AnyIO can also be adopted into a library or application
incrementally – bit by bit, no full refactoring necessary. It will blend in with
native libraries of your chosen backend.

%files
%license LICENSE
%doc README.rst
%{python_sitelib}/%{module}/
%{python_sitelib}/%{module}-%{version}-py%{pyver}.egg-info/

#----------------------------------------------------------------------------

%prep
%autosetup -n %{module}-%{version}

%build
%py_build

%install
%py_install


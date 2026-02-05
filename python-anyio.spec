%define module anyio
# enable tests
%bcond tests 1

Name:		python-anyio
Version:	4.12.1
Release:	1
Summary:	Asynchronous concurrency & networking framework
License:	MIT
Group:		Development/Python
URL:		https://github.com/agronholm/anyio
Source:		https://github.com/agronholm/anyio/archive/%{version}/%{name}-%{version}.tar.gz
BuildSystem:	python
BuildArch:	noarch
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
BuildRequires:	python%{pyver}dist(cython)
BuildRequires:	python%{pyver}dist(exceptiongroup)
BuildRequires:	python%{pyver}dist(hypothesis)
BuildRequires:	python%{pyver}dist(pluggy)
BuildRequires:	python%{pyver}dist(psutil)
BuildRequires:	python%{pyver}dist(pytest)
BuildRequires:	python%{pyver}dist(pytest-mock)
BuildRequires:	python%{pyver}dist(sniffio)
BuildRequires:	python%{pyver}dist(trustme)
BuildRequires:	python%{pyver}dist(uvloop)
%endif

Provides:	python%{pyver}dist(%{module}) = %{version}-%{release}

%description
AnyIO is an asynchronous networking and concurrency library that works on top
of either asyncio or trio. It implements trio-like structured concurrency (SC)
on top of asyncio, and works in harmony with the native SC of trio itself.

Applications and libraries written against AnyIO's API will run unmodified on
either asyncio or trio. AnyIO can also be adopted into a library or application
incrementally – bit by bit, no full refactoring necessary. It will blend in with
native libraries of your chosen backend.

%prep -a
# Remove upstream's egg-info
rm -vrf src/%{module}.egg-info
# disable coverage test requirement
sed -i '/"blockbuster/d' pyproject.toml
sed -i '/"coverage/d' pyproject.toml
sed -i '/"truststore/d' pyproject.toml
sed -i '/"uvloop/d' pyproject.toml

%build -p
# package cannot figure out its own version, use scm override to provide it
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}

%if %{with tests}
%check
export CI=true
export PYTHONPATH="%{buildroot}%{python_sitelib}:${PWD}"
# we dont have network access to run these tests
# some of these are also flaky
skiptest+="(TestTCPStream and test_happy_eyeballs)"
skiptest+=" or (TestTCPStream and test_connection_refused)"
skiptest+=" or test_bind_link_local"
skiptest+=" or (TestTCPStream and (ipv4 or ipv6))"
skiptest+=" or (TestTCPListener and (ipv4 or ipv6))"
skiptest+=" or (TestConnectedUDPSocket and (ipv4 or ipv6))"
skiptest+=" or (TestUDPSocket and (ipv4 or ipv6))"
skiptest+=" or (TestTLSStream and test_ragged_eofs)"
skiptest+=" or (test_send_eof_not_implemented)"
skiptest+=" or (test_exception_group and trio)"
skiptest+=" or (test_properties and trio)"
skiptest+=" or (test_properties and asyncio)"
skiptest+=" or test_keyboardinterrupt_during_test"
skiptest+=" or test_anyio_fixture_adoption_does_not_persist"

pytest -Wdefault -m "not network" -k "not (${skiptest})" -ra
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

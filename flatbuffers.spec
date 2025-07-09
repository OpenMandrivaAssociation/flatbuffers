%define major %(echo %{version}|cut -d. -f1)
%define libname %mklibname flatbuffers
%define devname %mklibname flatbuffers -d
%define staticname %mklibname flatbuffers -d -s

Name:		flatbuffers
Version:	25.2.10
Release:	2
Source0:	https://github.com/google/flatbuffers/archive/v%{version}.tar.gz
Summary:	Memory efficient serialization library
URL: 		https://flatbuffers.dev/
License:	Apache 2.0
Group:		System/Libraries
BuildRequires:	cmake ninja

%description
Memory efficient serialization library

%package -n %{libname}
Summary: Memory efficient serialization library
Group: System/Libraries
Requires: %{name} = %{EVRD}

%description -n %{libname}
Memory efficient serialization library

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}
Requires: %{name} = %{EVRD}
Provides: %{name}-devel = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

%package -n %{staticname}
Summary: Static library files for %{name}
Group: Development/C
Requires: %{devname} = %{EVRD}

%description -n %{staticname}
Static library files (Headers etc.) for %{name}.

%prep
%autosetup -p1

# https://github.com/google/flatbuffers/issues/5769
# Fixup CMake/FlatbuffersConfigVersion.cmake.in - Upstream releases tarballs
# that make no sense. They exect git describe to find correct information about
# the version in use - and replace that into the cmake file in the end. Obviously
# the tarball has no .git directory and thus does not carry that inormation
# We just inject %%version there. Easiest fix.
#sed -i 's/@VERSION_MAJOR@.@VERSION_MINOR@.@VERSION_PATCH@/%{version}/' CMake/FlatbuffersConfigVersion.cmake.in

%cmake -G Ninja \
	-DFLATBUFFERS_BUILD_SHAREDLIB:BOOL=ON \
	-DFLATBUFFERS_BUILD_TESTS=OFF

%build
%ninja_build -C build

%install
%ninja_install -C build

%files
%{_bindir}/flatc

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/cmake/*
%{_libdir}/pkgconfig/*.pc

%files -n %{staticname}
%{_libdir}/*.a

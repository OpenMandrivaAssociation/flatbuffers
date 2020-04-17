%define major 1
%define libname %mklibname flatbuffers %{major}
%define devname %mklibname flatbuffers -d

Name:		flatbuffers
Version:	1.12.0
Release:	1
Source0:	https://github.com/google/flatbuffers/archive/v%{version}.tar.gz
Summary:	Memory efficient serialization library
URL: 		http://google.github.io/flatbuffers/
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

%prep
%setup -q
%autopatch -p1


# https://github.com/google/flatbuffers/issues/5769
# Fixup CMake/FlatbuffersConfigVersion.cmake.in - Upstream releases tarballs
# that make no sense. They exect git describe to find correct information about
# the version in use - and replace that into the cmake file in the end. Obviously
# the tarball has no .git directory and thus does not carry that inormation
# We just inject %%version there. Easiest fix.
sed -i 's/@VERSION_MAJOR@.@VERSION_MINOR@.@VERSION_PATCH@/%{version}/' CMake/FlatbuffersConfigVersion.cmake.in

%build
%cmake -G Ninja \
	-DFLATBUFFERS_BUILD_SHAREDLIB:BOOL=ON \
	-DFLATBUFFERS_BUILD_TESTS=OFF \
	-DFLATBUFFERS_BUILD_STATICLIB:BOOL=OFF

%ninja -C build

%install
%ninja_install -C build
# cmake flags for disabling static libs isn't respected
rm -f %{buildroot}%{_libdir}/libflatbuffers.a

%files
%{_bindir}/flatc

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/cmake/*

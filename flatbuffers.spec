%define major 1
%define libname %mklibname flatbuffers %{major}
%define devname %mklibname flatbuffers -d

Name:		flatbuffers
Version:	1.10.0
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

%description -n %{devname}
Development files (Headers etc.) for %{name}.

%prep
%setup -q
%apply_patches
%cmake -G Ninja \
	-DFLATBUFFERS_BUILD_SHAREDLIB:BOOL=ON \
	-DFLATBUFFERS_BUILD_STATICLIB:BOOL=OFF

%build
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

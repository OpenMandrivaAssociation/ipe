%define _disable_ld_as_needed 1

Name:		ipe
Version:	7.1.1
Release:	%mkrel 1
Summary:	Drawing editor for creating figures in PDF or PostScript formats
Group:		Publishing
License:	GPLv2+
URL:		http://ipe7.sourceforge.net/
Source0:	http://sourceforge.net/projects/ipe7/files/%{name}/%{name}-%{version}-src.tar.gz
BuildRequires:	qt4-devel
BuildRequires:	desktop-file-utils
BuildRequires:	pkgconfig
BuildRequires:	lua-devel
Requires:	tetex-latex
Requires:	urw-fonts
Requires:	xdg-utils

%description
Ipe is a drawing editor for creating figures in PDF or (encapsulated)
Postscript format. It supports making small figures for inclusion into
LaTeX-documents as well as making multi-page PDF presentations that
can be shown on-line with a PDF viewer


%package	devel
Summary:	Development files and documentation for designing Ipelets
Group:		System/Libraries 
Requires:	%{name} = %{version}-%{release}
Requires:	qt4-devel
%description devel 
This packages contains the files necessary to develop Ipelets, which are
plugins for the Ipe editor.


%prep
%setup -n %{name}-%{version} -q

%build
#fix pkgconfig call for lua includes searching for versioned .pc file
sed -i  's|lua5.1|lua|g' src/config.mak

pushd src
#use moc instead of the default moc-qt4
#correctly set IPELIBDIR for x86_64 build
make IPEPREFIX=%_prefix IPE_USE_ICONV=-DIPE_USE_ICONV MOC=moc IPELIBDIR=%{_libdir}
popd 

# Create desktop file
cat > %{name}.desktop <<EOF
[Desktop Entry]
Type=Application
Encoding=UTF-8
Name=Ipe
Comment=The Ipe extensible drawing editor
Exec=ipe
Categories=Qt;Application;Graphics;
EOF

%install
rm -rf $RPM_BUILD_ROOT

pushd src
#correctly set IPELIBDIR for x86_64 build
%make IPEPREFIX=$RPM_BUILD_ROOT/%_prefix IPELIBDIR=$RPM_BUILD_ROOT/%{_libdir} install

#fix ipelets installation to /usr/lib instead of %{_libdir}
#
##DOES NOT WORK, ipe does not find ipelets thereafter
#
#mkdir -p $RPM_BUILD_ROOT/%{_libdir}/ipe/%{version}/
#mv $RPM_BUILD_ROOT/usr/lib/ipe/%{version}/ipelets $RPM_BUILD_ROOT/%{_libdir}/ipe/%{version}/

#install fontmap as describe in install.txt
mkdir -p $RPM_BUILD_ROOT/usr/share/%{name}/%{version}
cp -f ../fontmaps/gsfonts-fontmap.xml $RPM_BUILD_ROOT/usr/share/%{name}/%{version}/fontmap.xml
popd

#install altered desktop file
desktop-file-install --vendor mandriva                          \
        --dir ${RPM_BUILD_ROOT}%{_datadir}/applications         \
        --add-category X-MandrivaLinux                          \
        %{name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc readme.txt gpl.txt news.txt
%{_bindir}/ipe
%{_bindir}/ipe6upgrade
%{_bindir}/ipeextract
%{_bindir}/ipescript
%{_bindir}/iperender
%{_bindir}/ipetoipe
%{_bindir}/ipeview
/usr/lib/ipe/%{version}/ipelets/*.lua
/usr/lib/ipe/%{version}/ipelets/*.so
%{_libdir}/libipe.so.%{version}
%{_libdir}/libipecairo.so.%{version}
%{_libdir}/libipecanvas.so
%{_libdir}/libipecairo.so
%{_libdir}/libipe.so
%{_libdir}/libipelua.so
%{_libdir}/libipeui.so
#libipecanvas.so.7.1.1
%{_libdir}/libipecanvas.so.%{version}
%{_libdir}/libipelua.so.%{version}
%{_libdir}/libipeui.so.%{version}
%{_mandir}/man1/ipe*.xz
%{_datadir}/ipe/%{version}/styles
%{_datadir}/ipe/%{version}/scripts/
%{_datadir}/ipe/%{version}/lua
%{_datadir}/ipe/%{version}/icons
%{_datadir}/ipe/%{version}/doc
%{_datadir}/ipe/%{version}/fontmap.xml
%{_datadir}/applications/mandriva-%{name}.desktop


%files devel
%defattr(-,root,root,-)
%doc readme.txt gpl.txt news.txt
%{_includedir}/*.h

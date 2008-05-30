Name:		fvwm
Version:	1.24r
Summary:	An X Window System based window manager
Release:	%mkrel 28
Epoch:		1
License:	GPL
Group:		Graphical desktop/FVWM based
BuildRequires:	X11-devel xpm-devel imake x11-data-bitmaps
Requires:	x11-data-bitmaps fvwm2-icons xterm xsetroot
URL:		http://www.fvwm.org/
Source0:	sunsite.unc.edu:/pub/Linux/X11/window-managers/%{name}-%{version}.tar.bz2
Source1:	%{name}-%{version}-system-menu.fvwmrc
Source2:	fvwm1.menu-method
Source3:	%{name}.icon-48.png
Source4:	%{name}.icon-32.png
Source5:	%{name}.icon-16.png
Patch0:		%{name}-%{version}-fsstnd.patch
Patch1:		%{name}-%{version}-imake.patch.bz2
Patch2:		%{name}-%{version}-security.patch.bz2
Patch3:		%{name}-%{version}-fvwmman.patch.bz2
Patch4:		%{name}-%{version}-menu-100.patch.bz2
Patch5:		%{name}-%{version}-config.patch
Buildroot:	%{_tmppath}/%{name}-%{version}-root

%description
FVWM (the F stands for whatever you want, but the VWM stands for Virtual Window
Manager) is a window manager for the X Window System. FVWM was derived from the
twm window manager. FVWM is designed to minimize memory consumption, to provide
window frames with a 3D look, and to provide a simple virtual desktop. FVWM can
be configured to look like Motif.

Install the fvwm package if you'd like to use the FVWM window manager. If you
install fvwm, you'll also need to install fvwm2-icons.

%prep

%setup -q
%patch0 -p1 -b .fsstnd
%patch1 -p1 -b .imake
%patch2 -p1 -b .security
%patch3 -p1 -b .fvwmman
%patch4 -p1
%patch5 -p1
install -m644 %{SOURCE3} %{name}-48.png
install -m644 %{SOURCE4} %{name}-32.png
install -m644 %{SOURCE5} %{name}-16.png
# fix strange perms
chmod 644 sample.fvwmrc/*

%build
xmkmf
perl -p -i -e "s|CXXDEBUGFLAGS = .*|CXXDEBUGFLAGS = $RPM_OPT_FLAGS|" Makefile
perl -p -i -e "s|CDEBUGFLAGS = .*|CDEBUGFLAGS = $RPM_OPT_FLAGS|" Makefile
make Makefiles
perl -p -i -e "s|CXXDEBUGFLAGS = .*|CXXDEBUGFLAGS = $RPM_OPT_FLAGS|" */Makefile
perl -p -i -e "s|CDEBUGFLAGS = .*|CDEBUGFLAGS = $RPM_OPT_FLAGS|" */Makefile
perl -p -i -e "s|CXXDEBUGFLAGS = .*|CXXDEBUGFLAGS = $RPM_OPT_FLAGS|" */*/Makefile
perl -p -i -e "s|CDEBUGFLAGS = .*|CDEBUGFLAGS = $RPM_OPT_FLAGS|" */*/Makefile

%make

%install
rm -rf %{buildroot}
make install install.man DESTDIR=%{buildroot}
mkdir -p %{buildroot}/%{_datadir}/X11/fvwm/
rm -f %{buildroot}/%{_sysconfdir}/X11/fvwm/system.fvwmrc

mkdir -p %{buildroot}%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Categories=X-MandrivaLinux-System-Session-Windowmanagers;
Name=Fvwm
Comment=FVWM Windows manager
Icon=fvwm
Exec=startfvwm
EOF

install -D -m 644 %{SOURCE1} %{buildroot}/%{_datadir}/X11/fvwm/system.fvwmrc
install -D -m 644 %{SOURCE2} %{buildroot}/%{_menudir}/%{name}

# icons
install -D -m 644 %{name}-16.png %{buildroot}%{_miconsdir}/%{name}.png
install -D -m 644 %{name}-32.png %{buildroot}%{_iconsdir}/%{name}.png 
install -D -m 644 %{name}-48.png %{buildroot}%{_liconsdir}/%{name}.png

mkdir -p %{buildroot}/%{_datadir}/X11/wmsession.d/
cat << EOF > %{buildroot}/%{_datadir}/X11/wmsession.d/10Fvwm1
NAME=Fvwm1
EXEC=%{_bindir}/startfvwm
DESC=A very stable and light window manager
SCRIPT:
exec %{_bindir}/startfvwm
EOF

# 1.24r-24mdk: add startfvwm script to set cursor (defaults to wait)
# is this the right way to set the cursor?
cat > %{buildroot}%{_bindir}/startfvwm << EOF
%{_bindir}/xsetroot -cursor_name left_ptr
exec %{_bindir}/fvwm
EOF
chmod 755 %{buildroot}%{_bindir}/startfvwm

%post
%update_menus
%make_session

%postun
%clean_menus
%make_session

%clean
rm -fr %{buildroot}

%files
%defattr(-,root,root)
%config(noreplace) %{_menudir}/%{name}
%config(noreplace) %{_datadir}/X11/wmsession.d/10Fvwm1
%doc sample.fvwmrc/*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/X11/fvwm
%{_bindir}/fvwm
%{_bindir}/startfvwm
%{_mandir}/man*/*

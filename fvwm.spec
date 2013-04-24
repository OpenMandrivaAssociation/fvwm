Name:		fvwm
Version:	1.24r
Summary:	An X Window System based window manager
Release:	35
Epoch:		1
License:	GPLv2+
Group:		Graphical desktop/FVWM based
BuildRequires:	libx11-devel
BuildRequires:	libxext-devel
BuildRequires:	libxpm-devel
BuildRequires:	libxt-devel
BuildRequires:	x11-data-bitmaps
BuildRequires:	libxmu-devel
BuildRequires:	imake
Requires:	x11-data-bitmaps fvwm2-icons xterm xsetroot
URL:		http://www.fvwm.org/
Source0:	sunsite.unc.edu:/pub/Linux/X11/window-managers/%{name}-%{version}.tar.bz2
Source1:	%{name}-%{version}-system-menu.fvwmrc
Source2:	fvwm1.menu-method
Source3:	%{name}.icon-48.png
Source4:	%{name}.icon-32.png
Source5:	%{name}.icon-16.png
# patch to add FHS compliance
Patch0:		%{name}-%{version}-fsstnd.patch
# add Alpha support on linux for the makefile
Patch1:		%{name}-%{version}-imake.patch
# ??? try to open a file in exclusive mode 
Patch2:		%{name}-%{version}-security.patch
# add a suffix to manpage 
Patch3:		%{name}-%{version}-fvwmman.patch
# increase the number of popup from 50 to 100
Patch4:		%{name}-%{version}-menu-100.patch
# remove /usr/lib/X11 from linker search path 
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
make Makefiles
%make CDEBUGFLAGS="%optflags" EXTRA_LDOPTIONS="%ldflags"

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

mkdir -p %{buildroot}/%{_sysconfdir}/X11/wmsession.d/
cat << EOF > %{buildroot}/%{_sysconfdir}/X11/wmsession.d/10Fvwm1
NAME=Fvwm1
EXEC=%{_bindir}/startfvwm
DESC=A very stable and light window manager
SCRIPT:
exec %{_bindir}/startfvwm
EOF

# 1.24r-24mdk: add startfvwm script to set cursor (defaults to wait)
# is this the right way to set the cursor?
cat > %{buildroot}%{_bindir}/startfvwm << EOF
#!/bin/sh
%{_bindir}/xsetroot -cursor_name left_ptr
exec %{_bindir}/fvwm
EOF
chmod 755 %{buildroot}%{_bindir}/startfvwm



%clean
rm -fr %{buildroot}

%files
%defattr(-,root,root)
%config(noreplace) %{_menudir}/%{name}
%config(noreplace) %{_sysconfdir}/X11/wmsession.d/10Fvwm1
%doc sample.fvwmrc/*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/X11/fvwm
%{_bindir}/fvwm
%{_bindir}/startfvwm
%{_mandir}/man*/*


%changelog
* Thu Feb 03 2011 Funda Wang <fwang@mandriva.org> 1:1.24r-33mdv2011.0
+ Revision: 635470
- tighten BR

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.24r-32mdv2011.0
+ Revision: 610781
- rebuild

* Tue Mar 02 2010 Michael Scherer <misc@mandriva.org> 1:1.24r-31mdv2010.1
+ Revision: 513429
- fix rpmlint warning on startfvwm
- fix License
- move fwvm session file to the proper directory ( fix #57945 )

* Thu Sep 03 2009 Thierry Vignaud <tv@mandriva.org> 1:1.24r-31mdv2010.0
+ Revision: 428977
- rebuild

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 1:1.24r-30mdv2009.0
+ Revision: 266825
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Fri May 30 2008 Paulo Andrade <pcpa@mandriva.com.br> 1:1.24r-29mdv2009.0
+ Revision: 213535
- Uncompress some of the patches to make it easier to change them, and
  also to allow viewing the diffs in the commit mail logs.
  Add extra minimal Requires.
  Patch fvwm-1.24r-config.patch was actually undoing
  fvwm-1.24r-fsstnd.patch.bz2 and adding yet another alternative
  (from /usr/bin/X11 to /usr/X11R6/bin to /usr/bin ...), but was kept as
  it is still required to tell how to link with libXpm (could also just
  be merged in another patch).

* Wed May 21 2008 Paulo Andrade <pcpa@mandriva.com.br> 1:1.24r-27mdv2009.0
+ Revision: 209604
- Don't install files under /usr/X11R6.
  These changes should allow rebuilding the package and passing build
  system tests.
  Directly install data files in /usr/share/X11.

* Thu Jan 03 2008 Thierry Vignaud <tv@mandriva.org> 1:1.24r-26mdv2008.1
+ Revision: 141940
- auto-convert XDG menu entry
- adjust file list
- fix man pages directory
- BR imake
- kill re-definition of %%buildroot on Pixel's request
- buildrequires X11-devel instead of XFree86-devel
- use %%mkrel
- import fvwm

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot


* Sun Mar 13 2005 Franck Villaume <fvill@freesurf.fr> 1.24r-26mdk
- add missing files

* Thu Feb 26 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 1.24r-25mdk
- own /etc/X11/fvwm

* Mon Dec 29 2003 Marcel Pol <mpol@mandrake.org> 1.24r-24mdk
- add startfvwm script to set cursor
- unzip icons

* Sat Mar 15 2003 Marcel Pol <mpol@gmx.net> 1.24r-23mdk
- buildrequires: XFree86

* Mon Mar 11 2002 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.24r-22mdk
- resurrected by popular demand 
- s/Copyright/License/
- used png icons

* Mon Jan 07 2002 David BAUDENS <baudens@mandrakesoft.com> 1.24r-21mdk
- Rebuild

* Mon Nov 13 2000 David BAUDENS <baudens@mandrakesoft.com> 1.24r-20mdk
- Build with glibc-2.2 & gcc-2.96

* Mon Aug 07 2000 Frederic Lepied <flepied@mandrakesoft.com> 1.24r-19mdk
- automatically added BuildRequires

* Wed Jul 12 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.24r-18mdk
- Add support for the new chksession.

* Sun May 13 2000 David BAUDENS <baudens@mandrakesoft.com> 1.24r-17mdk
- Fix build for i486

* Tue May  2 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.24r-16mdk
- moved icons' ratio to 1.0 because some wm won't resize keeping aspect ratio
- added a mini icon

* Mon May  1 2000 Guillaume Cottenceau <gc@mandrakesoft.com> 1.24r-15mdk
- fixed postun script
- added url
- added icons
- cleaned up specfile
- removed version in menu entry

* Fri Apr 28 2000 damien <damien@mandrakesoft.com> 1.24r-14mdk
- added fndSession call.

* Fri Apr  7 2000 DindinX <odin@mandrakesoft.com> 1.24r-13mdk
- Still better default configuration
- Added support for the 'Menu' key.

* Wed Apr  5 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.24r-12mdk
- Better default configuration.
- Menu can do more than 50 entry.
- Add menu support.

* Mon Mar 27 2000 DindinX <odin@mandrakesoft.com> 1.24r-11mdk
- Spec fixes

* Wed Jan 12 2000 Pixel <pixel@mandrakesoft.com>
- fix build as non-root (defattr)

* Wed Nov 03 1999 Jerome Martin <jerome@mandrakesoft.com>
- rebuild for new distribution
- minor specfile cleanup

* Tue May 11 1999 Bernhard Rosenkraenzer <bero@mandrakesoft.com>
- Mandrake adaptions

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 17)

* Wed Dec 30 1998 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri May 01 1998 Cristian Gafton <gafton@redhat.com>
- tagged config files correctly
- buildroot

* Thu Oct 23 1997 Cristian Gafton <gafton@redhat.com>
- fixed it for AnotherLevel (icon paths, etc)

* Thu Jul 10 1997 Erik Troan <ewt@redhat.com>
- built against glibc

* Mon Mar 24 1997 Michael Fulbright <msf@redhat.com>
- Fixed system.fvwmrc to point at /usr/X11R6/include/X11/bitmaps and pixmaps. 
  Fvwm wasn't find icons otherwise, which is why they disappeared if someone
  upgraded from 4.0 to 4.1! 


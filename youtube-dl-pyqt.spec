%global oname youtube-dl-GUI
%global lname %(echo %oname |tr [:upper:] [:lower:])

Summary:	Front-end GUI of the popular youtube-dl written in PyQt
Name:		youtube-dl-pyqt
Version:	0.4.3
Release:	1
License:	MIT
Group:		Video
Url:		https://github.com/yasoob/youtube-dl-GUI
Source0:	https://github.com/yasoob/youtube-dl-GUI/archive/v%{version}/youtube-dl-GUI-%{version}.tar.gz
Patch0:		youtube-dl-pyqt-0.4.3_fix-packages.patch
BuildRequires:	imagemagick
BuildRequires:	librsvg
BuildRequires:	pkgconfig(python)
BuildRequires:	python3dist(pip)
BuildRequires:	python3dist(qtpy)
BuildRequires:	python3dist(setuptools)
BuildRequires:	python3dist(wheel)
# tests
#BuildRequires:	ffmpeg

Requires:	python3
Requires:	youtube-dl
Recommends:	ffmpeg

BuildArch:	noarch

%rename %lname
Conflicts:	yt-dlg

%description
A cross platform front-end GUI of the popular youtube-dl written in PyQt.

%files
%license LICENSE
%doc README.md
%{_bindir}/%{lname}
%{py_puresitedir}/youtube_dl_gui/
%{py_puresitedir}/youtube_dl_gui-*.*-info
%{_datadir}/applications/*%{lname}.desktop
%{_iconsdir}/hicolor/*/apps/%{lname}.png
%{_datadir}/pixmaps/%{lname}.xpm

#-----------------------------------------------------------------------------

%prep
%autosetup -p1  -n %{oname}-%{version}

# remove executables
find . -name \*exe -delete

# use system youtube-dl
sed -i -e '/"youtube_dl",/d' \
	-e '/"youtube_dl.downloader",/d' \
	-e '/"youtube_dl.extractor",/d' \
	-e '/"youtube_dl.postprocessor",/d' \
	setup.py

%build
%py_build

%install
%py_install

# fix path
install -dm 0755 %{buildroot}%{py_puresitedir}/youtube_dl_gui/
mv %{buildroot}%{py_puresitedir}/{main.py,GUI,Threads,UI} %{buildroot}%{py_puresitedir}/youtube_dl_gui/

# icons
for d in 16 32 48 64 72 128 256
do
	install -dm 0755 %{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/
	convert -background none -resize ${d}x${d} -extent ${d}x${d} -gravity center resources/logo.png \
			%{buildroot}%{_iconsdir}/hicolor/${d}x${d}/apps/%{lname}.png
done
install -dm 0755 %{buildroot}%{_datadir}/pixmaps/
convert -background none -resize 32x32 -extent 32x32 -gravity center resources/logo.png \
	%{buildroot}%{_datadir}/pixmaps/%{lname}.xpm

# .desktop
# from upstream commit commit effd7b72bf1cc4d37ab98dd745fe573a1eb1c292
install -pm 0755 -d %{buildroot}%{_datadir}/applications/
cat > %{buildroot}%{_datadir}/applications/openmandriva-%{lname}.desktop << EOF
[Desktop Entry]
Name=Youtube Downloader GUI
GenericName=Youtube Downloader GUI
Comment=A cross platform front-end GUI of the popular youtube-dl written in written in PyQt
Exec=%{lname}
Icon=%{lname}
MimeType=
Terminal=False
Type=Application
Categories=AudioVideo;Utility;
Keywords=Multimedia;Video;Audio;
EOF


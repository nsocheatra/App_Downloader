[Setup]
AppName=App_Downloader
; Keep in sync with app/version.py
AppVersion=2.1.1
DefaultDirName={autopf}\App_Downloader
DefaultGroupName=App_Downloader
OutputDir=output
OutputBaseFilename=App_Downloader_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
SetupIconFile=app\assets\icons\logo.ico
UninstallDisplayIcon={app}\App_Downloader.exe


[Files]
Source: "dist\App_Downloader.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "bin\ffmpeg.exe"; DestDir: "{app}\bin"; Flags: ignoreversion


[Icons]
Name: "{group}\App_Downloader"; Filename: "{app}\App_Downloader.exe"
Name: "{autodesktop}\App_Downloader"; Filename: "{app}\App_Downloader.exe"


[Run]
Filename: "{app}\App_Downloader.exe"; Description: "Launch App_Downloader"; Flags: nowait postinstall skipifsilent
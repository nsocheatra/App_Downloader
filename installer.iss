[Setup]
AppName=App_Downloader
AppVersion=1.2.0
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


[Icons]
Name: "{group}\App_Downloader"; Filename: "{app}\App_Downloader.exe"
Name: "{autodesktop}\App_Downloader"; Filename: "{app}\App_Downloader.exe"


[Run]
Filename: "{app}\App_Downloader.exe"; Description: "Launch App_Downloader"; Flags: nowait postinstall skipifsilent
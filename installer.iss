[Setup]
AppName=App_Downloader
AppVersion=1.0.0
AppPublisher=App_Downloader
DefaultDirName={autopf}\App_Downloader
DefaultGroupName=App_Downloader
OutputDir=dist
OutputBaseFilename=App_Downloader_Setup
SetupIconFile=app\assets\icons\logo.ico
UninstallDisplayIcon={app}\App_Downloader.exe
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin

[Files]
Source: "dist\App_Downloader.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\App_Downloader"; Filename: "{app}\App_Downloader.exe"
Name: "{group}\Uninstall App_Downloader"; Filename: "{uninstallexe}"
Name: "{commondesktop}\App_Downloader"; Filename: "{app}\App_Downloader.exe"

[Run]
Filename: "{app}\App_Downloader.exe"; Description: "Launch App_Downloader"; Flags: postinstall nowait skipifsilent

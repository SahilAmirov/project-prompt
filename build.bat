@echo off
echo ========================================================
echo  Project Context Scanner - Build Islemi Baslatiliyor...
echo ========================================================

:: Varsa eski build klasörlerini temizle
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del *.spec

:: PyInstaller Komutu
:: --noconsole: Konsol penceresini gizle
:: --onefile: Tek dosya yap
:: --icon: Exe ikonu
:: --add-data: Ikonu iceri gom (Program calisinca gorunmesi icin)
pyinstaller --noconsole --onefile --icon=fav.ico --add-data "fav.ico;." --name="ProjectContextScanner" project_scanner.py

echo.
echo ========================================================
echo  ISLEM TAMAMLANDI!
echo  Dosyaniz "dist" klasorunun icindedir.
echo ========================================================
pause
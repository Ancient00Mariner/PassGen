echo off
pyinstaller --onefile --windowed --noconfirm --icon=SEPfield.ico --add-data wordlist;. PassGen.py
pause
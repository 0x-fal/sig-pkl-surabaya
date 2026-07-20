@echo off
echo ========================================================
echo MENGHUBUNGKAN DAN MENGUPLOAD KE GITHUB
echo ========================================================
echo.

"C:\Program Files\Git\cmd\git.exe" remote remove origin
"C:\Program Files\Git\cmd\git.exe" remote add origin https://github.com/0x-fal/sig-pkl-surabaya.git
"C:\Program Files\Git\cmd\git.exe" branch -M main

echo Memulai proses upload (push)...
echo Jika muncul pop-up login browser, silakan login!
echo.
"C:\Program Files\Git\cmd\git.exe" push -u origin main

echo.
echo ========================================================
echo SELESAI! Tekan tombol apa saja untuk menutup jendela ini.
pause >nul

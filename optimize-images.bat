@echo off
echo ==========================================
echo   IMAGE OPTIMIZATION PIPELINE
echo ==========================================
echo.

echo [1/2] Generating thumbnails...
python tools/generate_thumbnails.py
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Thumbnail generation failed!
    pause
    exit /b 1
)

echo.
echo [2/2] Updating gallery data...
node tools/generate-gallery.js
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Gallery data generation failed!
    pause
    exit /b 1
)

echo.
echo ==========================================
echo   OPTIMIZATION COMPLETE!
echo ==========================================
echo.
echo Your images are now optimized for fast loading:
echo - Blurred thumbnails for instant placeholders
echo - Dimensions for zero layout shift
echo - Progressive loading enabled
echo.
echo Ready to commit and push to GitHub!
pause

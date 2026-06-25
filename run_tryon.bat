@echo off
setlocal enabledelayedexpansion

:: Check arguments
if "%~1"=="" (
    echo Usage: run_tryon.bat [person_image.jpg] [cloth_image.jpg]
    echo Example: run_tryon.bat 01409_00.jpg 01190_00.jpg
    exit /b 1
)
if "%~2"=="" (
    echo Usage: run_tryon.bat [person_image.jpg] [cloth_image.jpg]
    echo Example: run_tryon.bat 01409_00.jpg 01190_00.jpg
    exit /b 1
)

set PERSON=%~1
set CLOTH=%~2

echo ===================================================
echo [1/4] Writing pair configuration...
echo ===================================================
:: Write the pairing to test_pairs.txt in VITON-HD
echo %PERSON% %CLOTH%> D:\projects\VITON-HD\test_pairs.txt
echo Pair configured: %PERSON% -^> %CLOTH%

echo ===================================================
echo [2/4] Running Warp model (cloth alignment)...
echo ===================================================
:: Save current directory and switch to warp/test
pushd warp\test

:: Run the warp model
set PYTHONPATH=../../PF-AFN/PF-AFN_test
..\..\dci-vton\python.exe eval_PBAFN_viton.py --name=unpaired-cloth-warp --resize_or_crop=none --batchSize=1 --gpu_ids=0 --warp_checkpoint=../../checkpoints/warp_viton.pth --label_nc=13 --dataroot=D:/projects/VITON-HD --fineSize=512 --unpaired

:: Copy the warped cloth and mask
copy /Y results\unpaired-cloth-warp\%PERSON% D:\projects\VITON-HD\test\unpaired-cloth-warp\%PERSON%
copy /Y results\unpaired-cloth-warp-mask\%PERSON% D:\projects\VITON-HD\test\unpaired-cloth-warp-mask\%PERSON%

:: Restore directory
popd

echo ===================================================
echo [3/4] Running Diffusion model (inference)...
echo ===================================================
set PYTHONPATH=src/taming-transformers;src/clip;.
.\dci-vton\python.exe test.py --plms --gpu_id 0 --ddim_steps 30 --outdir results/viton --config configs/viton512.yaml --dataroot D:/projects/VITON-HD --ckpt checkpoints/viton512_v2.ckpt --n_samples 1 --seed 23 --scale 1 --H 512 --W 512 --unpaired

echo ===================================================
echo [4/4] Generating comparison image...
echo ===================================================
.\dci-vton\python.exe make_comparison.py --person %PERSON% --cloth %CLOTH%

echo ===================================================
echo Try-on completed successfully!
echo Final output: results/viton/result/%PERSON:.jpg=.png%
echo Comparison: results/viton/comparisons/
echo ===================================================

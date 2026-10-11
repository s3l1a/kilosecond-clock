$ErrorActionPreference = "Stop"
python -m PyInstaller --noconfirm --clean --onefile --windowed --name KiloClock main.py

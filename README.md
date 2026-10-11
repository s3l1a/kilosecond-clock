# KiloClock

## Standard time has had a good run

Hours, minutes, and seconds are charming little relics from a time when people
needed sundials and had not yet discovered the thrilling administrative power
of SI prefixes. KiloClock fixes this embarrassing situation by displaying your
day in **kiloseconds (Ks)**: 86.4 Ks from midnight to midnight, with every hour
worth a dignified 3.6 Ks.

The dial still has the familiar 12-hour geometry, because a completely new
clock face would be unnecessarily upsetting. Each major label is its kilosecond
equivalent, while the half-hour markers whisper "+1.8 Ks" like tiny bureaucrats
filing paperwork against chronology.

## Features

- Smooth, anti-aliased analog hands with a continuously sweeping second hand
- 12 major Ks labels, 24 half-hour interval indicators, and a live digital readout
- Minimal dark instrument-panel aesthetic built with PyQt6
- Standalone Windows executable via PyInstaller

## Run from source

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

## Build the standalone executable

```powershell
.\build.ps1
```

The result is `dist\KiloClock.exe`. Python is not required to run that file.

## The conversion nobody requested

`1 day = 86.4 Ks`, `1 hour = 3.6 Ks`, and `30 minutes = 1.8 Ks`.
The clock uses local system time, because even the future has time zones.

## License

Released under the MIT License. Time itself remains proprietary to the universe.

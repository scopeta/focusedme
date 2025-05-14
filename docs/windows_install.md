# Windows Installation Guide

## Installing focusedMe on Windows

`focusedMe` now supports Windows without requiring Microsoft Visual C++ Build Tools. To install:

```
pip install focusedme
```

## Troubleshooting

If you encounter any issues:

1. Make sure you have the latest version of pip:
   ```
   python -m pip install --upgrade pip
   ```

2. If you're still experiencing problems, please report the issue on our GitHub repository:
   https://github.com/scopeta/focusedme/issues

## Features on Windows

- Audio notifications use the `playsound` library instead of `simpleaudio`
- All other functionality works the same as on other platforms

## Usage

After installation, run the timer using:

```
focusedme
```

For help and options:

```
focusedme -h
```

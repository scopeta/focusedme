# FocusedMe v0.1.79 Release Notes

## Windows Support Improvements

We're excited to announce that FocusedMe now has improved support for Windows platforms! This release eliminates the need for Microsoft Visual C++ Build Tools, making installation significantly easier for Windows users.

### What's New

- **Simplified Windows Installation**: No more C++ compiler errors! FocusedMe now uses the `playsound` library on Windows instead of `simpleaudio`.
- **Platform-Specific Audio Playback**: Added intelligent detection of platform to use the most appropriate audio library:
  - Windows: Uses `playsound`
  - macOS: Uses built-in `afplay` command
  - Linux/Other: Uses `simpleaudio`
- **Windows Installation Guide**: Added dedicated documentation for Windows users
- **Windows Installation Script**: Added `windows_install.bat` for one-click installation

### Installation Options

Windows users can now install FocusedMe in multiple ways:

1. **Standard installation**:
   ```
   pip install focusedme
   ```

2. **Using requirements file**:
   ```
   pip install -r requirements-windows.txt
   pip install focusedme
   ```

3. **Using installation script**:
   - Download and run `windows_install.bat`

### Documentation Updates

- Added Windows-specific installation documentation
- Updated platform support information in main documentation
- Added platform-specific notes to code docstrings

### Test Coverage

- Added tests for platform-specific audio playback

### Bug Fixes

- Fixed installation issues on Windows platform that required Visual C++ Build Tools

## Contributors

- Special thanks to the FocusedMe community for reporting this issue and helping with testing.

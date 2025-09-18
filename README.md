## Arabic Learning Game / Battleship – Web and Desktop

This project contains two Pygame-based games:
- `zaid.py`: Arabic learning game (letters, numbers, and “who’s sound”).
- `game.py`: Battleship game (Pygame and a separate Tkinter version embedded in the same file).

You can run locally on desktop, and also build a WebAssembly version with pygbag to host on GitHub Pages.

### Local Desktop (Windows/macOS/Linux)
- Install Python 3.10–3.11
- Create a venv (optional) and install dependencies:
```bash
pip install pygame
```
- Run the Arabic game:
```bash
python zaid.py
```
- Or run the Battleship (Pygame version):
```bash
python game.py
```

Note: The Tkinter variant inside `game.py` is desktop-only and not used on the web.

### Build for Web with pygbag (WebAssembly)
pygbag compiles Python/Pygame to run in the browser via WebAssembly (Pyodide).

1) Install pygbag:
```bash
pip install pygbag
```

2) Ensure the web entry is `main.py` (this repo includes a tiny launcher that calls `zaid.main()`).

3) Build:
```bash
python -m pygbag --build .
```
This creates `build/web/` with an `index.html` you can open locally or deploy.

4) Test locally (serves at http://127.0.0.1:8000):
```bash
python -m pygbag --host 8000 .
```

### Deploy to GitHub Pages
This repo includes a GitHub Actions workflow that builds with pygbag and publishes `build/web/` to GitHub Pages.

Steps:
- Commit and push this project to a GitHub repository.
- In GitHub, go to Settings → Pages → Build and deployment and set Source to “GitHub Actions”.
- Push to `main` and the workflow in `.github/workflows/deploy.yml` will build and deploy automatically.

After it finishes, your game will be live at: https://<your-username>.github.io/<your-repo>/

### Project structure
- `main.py`: Web entry point calling `zaid.main()`.
- `zaid.py`: Main Arabic learning game (loads assets from `images/`, `letter_images/`, `number_images/`, `who_images/`, `who_sounds/`, `sounds/`).
- `game.py`: Battleship game (Pygame + embedded Tkinter version).
- Asset folders: keep their relative paths; pygbag packages them automatically.

### Tips for Web build
- Avoid using blocking dialogs or OS-specific APIs on the web path.
- Large audio files can delay loading; compress where reasonable.
- If you add new asset folders, keep them adjacent to `main.py` so pygbag can bundle them.



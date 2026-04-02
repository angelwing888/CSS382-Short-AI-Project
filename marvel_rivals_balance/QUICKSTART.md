# Getting Started - Local Development

Quick guide to run the Marvel Rivals Balance Tracker on your machine.

## System Requirements

- **Python**: 3.8 or higher
- **pip**: Usually comes with Python
- **Git**: (Optional, for cloning)
- **RAM**: 512 MB minimum
- **Disk Space**: 50 MB

## Option 1: Fastest Setup (Recommended)

### macOS/Linux Users

1. **Navigate to project:**
   ```bash
   cd marvel_rivals_balance
   ```

2. **Make script executable:**
   ```bash
   chmod +x run.sh
   ```

3. **Run the script:**
   ```bash
   ./run.sh
   ```

The script will:
- ✅ Create virtual environment
- ✅ Install dependencies
- ✅ Scrape balance data
- ✅ Start the web server

**Access at**: http://localhost:5000

### Windows Users

1. **Navigate to project in PowerShell or Command Prompt:**
   ```cmd
   cd marvel_rivals_balance
   ```

2. **Run the batch file:**
   ```cmd
   run.bat
   ```

**Access at**: http://localhost:5000

---

## Option 2: Manual Setup (Step-by-Step)

### 1. Create Virtual Environment

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

You should see output like:
```
Collecting Flask==3.0.0
  Downloading Flask-3.0.0-py3-none-any.whl
...
Successfully installed Flask-3.0.0 ...
```

### 3. Download Balance Data

```bash
python scraper.py
```

This will:
- Fetch all Marvel Rivals balance patches
- Parse character adjustments
- Save to `balance_data.json`
- **Takes 2-5 minutes**

You'll see:
```
Fetching Marvel Rivals balance patches...
Found 42 heroes with adjustments
Data saved to balance_data.json
```

### 4. Start the Application

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

### 5. Open in Browser

Visit: **http://localhost:5000**

---

## Option 3: Docker Setup

### Prerequisites
- Install Docker: https://www.docker.com/products/docker-desktop

### Run

```bash
# Build image
docker build -t marvel-rivals .

# Run container
docker run -p 5000:5000 marvel-rivals

# Access at http://localhost:5000
```

### With Docker Compose

```bash
# Run
docker-compose up

# Access at http://localhost:5000

# Stop
docker-compose down
```

---

## Testing the Installation

### 1. Check Data File
```bash
# Should exist and contain JSON data
cat balance_data.json | head -20
```

### 2. Test API Endpoints

Open in browser or use curl:

```bash
# Get all heroes
curl http://localhost:5000/api/heroes

# Get hero stats
curl http://localhost:5000/api/stats

# Get specific hero (replace with actual hero name)
curl "http://localhost:5000/api/hero/Spider-Man"
```

### 3. Check Web Interface
- Visit http://localhost:5000
- Should see list of heroes
- Search bar should work
- Click a hero to see adjustments

---

## Troubleshooting

### "Command not found: python3"

**Windows:**
```cmd
python app.py
```

**macOS/Linux:**
- Make sure Python is in your PATH
- Try: `/usr/local/bin/python3 app.py`
- Or install Python from https://www.python.org

---

### "ModuleNotFoundError: No module named 'flask'"

```bash
# Verify virtual environment is activated
# You should see (venv) at the start of your terminal line

# Reinstall requirements
pip install -r requirements.txt
```

---

### "Port 5000 is already in use"

Option A: Stop the other app using port 5000

Option B: Use different port
```python
# Edit app.py, line at bottom:
app.run(debug=False, host='0.0.0.0', port=8000)  # Change 5000 to 8000
```

Then visit: http://localhost:8000

---

### "balance_data.json not found"

```bash
# Run the scraper first
python scraper.py
```

Wait 2-5 minutes for it to complete.

---

### Scraper is slow or times out

```bash
# Check your internet connection
ping marvelrivals.com

# Try running scraper with verbose output
python scraper.py
```

The scraper includes rate limiting (delays between requests) to be respectful to the server.

---

### Browser shows "Connection refused"

- Make sure Flask app is still running
- Check terminal where you ran `python app.py`
- Make sure you visited http://localhost:5000 (not https)
- Try different port if 5000 is in use

---

## Development Mode

For development/debugging with auto-reload:

```bash
# Edit app.py, last line:
app.run(debug=True)  # Auto-reloads on file changes
```

---

## Updating the Data

To refresh hero adjustment data:

```bash
python scraper.py
```

This will:
- Fetch latest balance patches from Marvel Rivals
- Overwrite `balance_data.json`
- Take 2-5 minutes

---

## File Structure

```
marvel_rivals_balance/
├── app.py                 # Flask web server
├── scraper.py            # Data scraper
├── balance_data.json     # Hero adjustment data (generated)
├── requirements.txt      # Python dependencies
├── run.sh               # Quick start (Linux/macOS)
├── run.bat              # Quick start (Windows)
├── templates/
│   └── index.html       # Web interface
├── README.md            # Main documentation
├── DEPLOYMENT.md        # Deployment guide
└── QUICKSTART.md        # This file
```

---

## Next Steps

Once the app is running locally:

1. **Explore the UI**
   - Search for heroes
   - Click hero names to see adjustment history
   - View statistics

2. **Customize** (optional)
   - Edit `templates/index.html` to change colors
   - Modify `app.py` to add features
   - Improve the scraper in `scraper.py`

3. **Deploy** (when ready)
   - See [DEPLOYMENT.md](DEPLOYMENT.md)
   - Choose a platform (Heroku, Railway, etc.)
   - Follow deployment steps

---

## Need Help?

1. **Check logs** - Look at terminal output for error messages
2. **Verify files** - Make sure all files exist: `ls` (macOS/Linux) or `dir` (Windows)
3. **Update Python** - `pip install --upgrade pip`
4. **Clean install** - Delete venv and start fresh

---

## Performance Tips

- First data load takes 2-5 minutes (scraping ~21 pages)
- After that, web interface loads instantly
- Search is instant (client-side filtering)
- Hero details load when you click (lazy loading)

---

## Security Notes (Local Use)

- `debug=False` in production
- Set SECRET_KEY in production
- Use HTTPS when deployed (most platforms handle this)
- Don't expose `.env` file with secrets

---

## What to Do Next

✅ **You now have a working app!**

- Test it locally
- Make customizations if desired
- Deploy to cloud (see DEPLOYMENT.md)
- Set up data refresh schedule

Enjoy tracking Marvel Rivals balance changes! 🦸

# Marvel Rivals Balance Adjustments Tracker

Deployed website: https://marvel-rivals-adj-tracker.netlify.app

Idea: Build a web app that shows all of the balance adjustments for heroes in Marvel Rivals throughout the previous patches. It should list out the characters, and then underneath, include the patch they were adjusted and the adjustment that was made.

A web application that displays all balance adjustments for Marvel Rivals heroes across patches.

## Features

- 🦸 Browse all Marvel Rivals heroes
- 📊 View adjustment history by patch
- 🔍 Search functionality to find heroes quickly
- 📈 Statistics showing most adjusted heroes
- 📱 Responsive design for mobile and desktop

## Project Structure

```
marvel_rivals_balance/
├── app.py                 # Flask web application
├── scraper.py            # Web scraper for balance data
├── requirements.txt      # Python dependencies
├── Procfile             # Heroku deployment config
├── package.json         # Project metadata
├── README.md            # This file
├── templates/
│   └── index.html       # Web UI
└── balance_data.json    # Cached balance data (generated)
```

## Local Setup

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone or download the project:**
   ```bash
   cd marvel_rivals_balance
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Scrape the balance data:**
   ```bash
   python3 scraper.py
   ```
   This will create `balance_data.json` with all hero adjustments.

5. **Run the application:**
   ```bash
   python3 app.py
   ```

6. **Open your browser:**
   Navigate to `http://localhost:5000`

## Deployment

### Option 1: Heroku (Recommended for Quick Deployment)

1. **Create a Heroku account** at https://www.heroku.com

2. **Install Heroku CLI** from https://devcenter.heroku.com/articles/heroku-cli

3. **Login to Heroku:**
   ```bash
   heroku login
   ```

4. **Create a Heroku app:**
   ```bash
   heroku create your-app-name
   ```

5. **Add buildpacks:**
   ```bash
   heroku buildpacks:add heroku/python
   ```

6. **Deploy:**
   ```bash
   git push heroku main
   # OR if not using git:
   heroku deploy --source-dir . --app your-app-name
   ```

7. **Run the scraper on the deployed app:**
   ```bash
   heroku run python scraper.py --app your-app-name
   ```

8. **Visit your app:**
   ```bash
   heroku open --app your-app-name
   ```

### Option 2: AWS Elastic Beanstalk

1. **Install AWS CLI** and configure credentials

2. **Install EB CLI:**
   ```bash
   pip install awsebcli
   ```

3. **Initialize EB:**
   ```bash
   eb init -p python-3.11 marvel-rivals-balance
   ```

4. **Create environment:**
   ```bash
   eb create marvel-rivals-env
   ```

5. **Deploy:**
   ```bash
   eb deploy
   ```

6. **Run scraper:**
   ```bash
   eb ssh
   python scraper.py
   ```

7. **Open application:**
   ```bash
   eb open
   ```

### Option 3: Docker + Any Cloud Provider

1. **Create a Dockerfile** in the project root:
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   
   # Run scraper on startup
   RUN python scraper.py
   
   EXPOSE 5000
   CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
   ```

2. **Build and run locally:**
   ```bash
   docker build -t marvel-rivals-balance .
   docker run -p 5000:5000 marvel-rivals-balance
   ```

3. **Deploy to your cloud provider** (GCP, AWS, Azure, DigitalOcean, etc.)

### Option 4: PythonAnywhere

1. Go to https://www.pythonanywhere.com and create an account

2. Upload your project files

3. Set up a virtual environment in PythonAnywhere console

4. Configure the WSGI file to point to your Flask app

5. Run: `python scraper.py` in the terminal

6. Reload the web app

## Data Refreshing

The `balance_data.json` file is generated when you run `scraper.py`. To keep data updated:

### Automated (Heroku Scheduler)

1. Add the Heroku Scheduler add-on to your app

2. Create a new scheduled job:
   ```bash
   python scraper.py
   ```

3. Set it to run daily

### Manual

Simply run the scraper again whenever you want to update the data:
```bash
python scraper.py
```

## How It Works

1. **Scraper (`scraper.py`)**:
   - Fetches the Marvel Rivals official balance post API
   - Parses each balance post for character adjustments
   - Organizes data by hero and patch
   - Saves to `balance_data.json`

2. **Web App (`app.py`)**:
   - Flask backend serving the API
   - Routes:
     - `/` - Main page
     - `/api/heroes` - Get all heroes with adjustment counts
     - `/api/hero/<name>` - Get adjustments for a specific hero
     - `/api/stats` - Get overall statistics

3. **Frontend (`templates/index.html`)**:
   - Modern, responsive UI
   - Real-time search
   - Click to expand hero details
   - Shows patch name, date, and adjustment description

## Troubleshooting

### "balance_data.json not found"
Run the scraper first: `python3 scraper.py`

### "Import error for requests/beautifulsoup4"
Make sure you've installed dependencies: `pip install -r requirements.txt`

### "Port 5000 already in use"
Change the port in `app.py`:
```python
app.run(debug=False, host='0.0.0.0', port=8000)  # Change 5000 to 8000
```

### Scraper is slow or timing out
- The scraper includes rate limiting (0.5-1 second delays) to be respectful to the server
- Check your internet connection
- Verify the Marvel Rivals website is accessible

## Environment Variables

You can optionally configure via `.env` file:

```
FLASK_ENV=production
FLASK_DEBUG=0
```

## Performance Notes

- The scraper can take 2-5 minutes to fetch all ~21 pages of balance data
- The HTML/CSS/JS is optimized for fast loading and searching
- Data is cached in `balance_data.json` for instant page loads

## Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Web Scraping**: BeautifulSoup, Requests
- **Deployment**: Gunicorn, Heroku/AWS/Docker

## License

This project is for educational purposes. Marvel Rivals is developed by NetEase.

## Contributing

Feel free to improve the scraper, UI, or deployment configurations!

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify the Marvel Rivals website is still accessible
3. Ensure all dependencies are installed with correct versions

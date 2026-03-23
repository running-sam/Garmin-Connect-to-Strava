Strava Bulk Turbo Uploader
A specialized Python utility designed to handle massive Garmin history exports (10,000+ files) by intelligently managing file priorities and Strava API rate limits.

📥 Data Source
This script is designed to process data exported using the garminexport tool.

It specifically handles the "Triple Format" export (where Garmin provides .fit, .gpx, and .tcx for a single activity).

It ignores the .json metadata files during the upload phase to save API bandwidth.

🚀 Key Features
Format Prioritization: Automatically selects the highest quality data source (.fit first, then .tcx, then .gpx).

Turbo-Skip Logic: Instantly identifies and archives duplicates (0.5s delay) while slowing down for new uploads (15s delay) to stay safe.

Reverse Chronological: Processes 2026/2025 activities first so your recent profile is updated immediately.

Auto-Cleanup: Moves processed groups to a /Done folder to allow for easy stopping and resuming.

🛠️ Prerequisites
Python 3.x

Stravalib: pip install stravalib

Strava API Credentials: See the Setup guide below.

🚦 How to Setup the Strava API
To use this script, you must register your own "Application" with Strava to get your unique keys.

Create the App:

Go to Strava Developers - My App.

Log in and fill out the form:

Application Name: "My Bulk Uploader" (or anything you like).

Category: "Data Tools".

Website: http://localhost.

Authorization Callback Domain: localhost.

Get your Secret:

Once created, you will see a Client ID and a Client Secret.

Important: Do not share your Client Secret on GitHub!

Configure the Script:

Open strava_upload.py and paste your CLIENT_ID and CLIENT_SECRET into the configuration section.

💻 Usage Instructions
Prepare your Folder:
Point the FOLDER variable in the script to your Garmin export directory (e.g., /Users/sam/activities).

Run the Script:

Bash
python3 strava_upload.py
The OAuth Handshake:

The script will print a URL. Copy and paste it into your browser.

Click Authorize.

Your browser will redirect to a broken "localhost" page. Look at the URL bar.

Find the part that says code=xxxxxxxx. Copy that code and paste it back into your terminal.

Rate Limit Management:
Strava limits you to 100 requests every 15 minutes. If you hit this, the script will automatically "nap" for 15 minutes and then resume.

🧹 Post-Processing (JSON Cleanup)
Once the script finishes (it will say "All unique activities processed!"), you will still have thousands of .json files in your main folder. Use this command to move them to your archive:

Bash
find /your-path/activities -name "*.json" -exec mv {} /your-path/activities/Done/ \;
Pro-Tip for New Zealand Users:
If you are running this on a MacBook, use the caffeinate command in a separate Terminal window. This prevents your Mac from sleeping and dropping the WiFi connection during the 2.5-day upload process.

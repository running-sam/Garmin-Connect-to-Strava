# Strava Bulk Turbo Uploader

A specialized Python utility designed to handle massive Garmin history exports (10,000+ files) by intelligently managing file priorities and Strava API rate limits.

## 📥 Data Source
This script is designed to process data exported using the [garminexport](https://github.com/petergardfjall/garminexport) tool. 
* It handles the "Triple Format" export (where Garmin provides `.fit`, `.gpx`, and `.tcx` for a single activity).
* It ignores `.json` metadata files during the upload phase to save API bandwidth and focus on GPS data.

## 🚀 Key Features
* **Format Prioritization:** Automatically selects the highest quality data source (**`.fit`** first, then `.tcx`, then `.gpx`).
* **Turbo-Skip Logic:** Instantly identifies and archives duplicates (0.5s delay) while slowing down for new uploads (15s delay) to stay safe.
* **Reverse Chronological:** Processes your most recent activities (2025/2026) first so your profile updates immediately.
* **Auto-Cleanup:** Moves processed groups to a `/Done` folder to allow for easy stopping and resuming without re-processing files.

## 🛠️ Prerequisites
1. **Python 3.x**
2. **Stravalib:** `pip install stravalib`
3. **Strava API Credentials:** (See the Setup guide below)

---

## 🚦 How to Setup the Strava API

To use this script, you must register your own "Application" with Strava to obtain your unique keys.

1. **Create the App:**
   * Go to the [Strava Developers Settings](https://www.strava.com/settings/api).
   * Fill out the form:
     * **Application Name:** `My Bulk Uploader`
     * **Category:** `Data Tools`
     * **Website:** `http://localhost`
     * **Authorization Callback Domain:** `localhost`
2. **Get your Credentials:**
   * Once created, you will see a **Client ID** and a **Client Secret**. 
   * **Note:** Keep your Client Secret private. Do not commit it to public repositories.
3. **Configure the Script:**
   * Open `strava_upload.py` and paste your `CLIENT_ID`, `CLIENT_SECRET`, and the local `FOLDER` path into the configuration section.

---

## 💻 Usage Instructions

1. **Prepare your Folder:**
   Ensure all your exported files are in the directory defined in the script.
2. **Run the Script:**
   ```bash
   python3 strava_upload.py

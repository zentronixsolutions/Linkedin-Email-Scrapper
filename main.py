import subprocess
import time

def run_script(path):
    print(f"Running: {path}")
    result = subprocess.run(["python", path], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Error:", result.stderr)

if __name__ == "__main__":
    print("Starting LinkedIn Scraper Pipeline...")

    run_script("src/cookies.py")
    print("Cookies extracted. Please complete login in the browser window (if not headless).")
    time.sleep(2)

    run_script("src/profile_links.py")
    print("Profile links extracted and saved.")
    time.sleep(2)

    run_script("src/profile_data.py")
    print("Profile data (names & emails) extracted and saved.")

    print("All steps completed successfully!")

from subprocess import Popen, check_output, run, PIPE
from time import sleep
from argparse import ArgumentParser

ap = ArgumentParser(prog="Browser Kiosk mode",
                    description="Opens a list of tabs in chromium, and cycles throught the tabs every given interval.",
                    epilog="This program requires xdotools be installed on the system locally.")

ap.add_argument("-f", "--file", dest="filename", help="The file containing the urls to cycle through.")
ap.add_argument("-i", "--interval", dest="interval", help="The time each tab should be displayed before going to the next.", default=30)

parse = ap.parse_args()

# List of URLs you want to open
try:
    urls = []
    with open(parse.filename, "r") as f:
        for line in f:
            print(line.rstrip())
            urls.append(line.rstrip())
except Exception as err:
    print(err)
    urls = [
            "[URL1]",
            "[URL2]"
    ]

# Command to launch Chromium with the first URL and get the window ID
command = ["chromium", "--start-fullscreen", "--incognito", "--disable-infobars"]
#Dynamically adding the urls to the command list
for url in urls:
    print(type(url), url)
    command.append(url)

process = Popen(command, stdout=PIPE)

# Wait a bit to ensure the browser has opened
sleep(5)

# Get the window ID of the last active window (which should be Chromium)
window_id = check_output(["xdotool", "getactivewindow"]).strip().decode('utf-8')

# Function to cycle through tabs
def cycle_tabs(window_id, i):
    run(["xdotool", "windowfocus", window_id])
    run(["xdotool", "key", "ctrl+Tab"])  # Cycle to the next tab
    sleep(i)

# Start cycling through tabs every 30 seconds
while True:
    try:
        cycle_tabs(window_id, parse.interval)
    except KeyboardInterrupt:
        break

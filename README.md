# TUCaN Grades

__Update:__ Since this feature has been implemented as a first party solution this repository has been archived.

TUCaN Grades is a small script to check [TUCaN](https://www.tucan.tu-darmstadt.de) for new grades.

## Setup

Requirements:

- Python 3
- MechanicalSoup

Add your TUCaN user, password and your @stud.tu-darmstadt.de email address to the initializer.

```bash
# Install MechanicalSoup if necessary
pip3 install MechanicalSoup

# Add a crontab to run grades automatically
# Edit crontab file
crontab -e

# Add this line to run grades every 15 minutes
*/15 * * * * cd ~/tucan-grades && python3 grades.py
```

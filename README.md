# analyzeAuthLogs
Python script that reads auth.log files and saves usernames and counts of attempted logins.

**Reads multiple log files at once.**
## Requirements
- Python2 (tested with python2.7.12)

## Install & Run
- Download or clone this repo
- Extract all log files 

- Run script via 

```bash
python /path/to/repo/analyzeLogs.py path/to/logs number-of-files
````


**Note:** Files need to be in the structure `filename.extension`, `filename.extension.1`, `filename.extension.2`, `filename.extension.n`.

## Output
The script creates a `authlist.csv` into the path from where the script was started. 

## Example
Given following file structure

```
fofo/analyzeLogs.py
foo/bar/
foo/bar/auth.log
foo/bar/auth.log.1
foo/bar/auth.log.2
```
You can run the script with 

```bash
python fofo/analyzeLogs.py foo/bar/auth.log 3
```
Which will create `fofo/authlist.csv`.

## License
This code is licensed under the GNU GENERAL PUBLIC LICENSE version 3 (GNU GPL v3). For more information see [LICENSE](https://github.com/jansule/analyzeAuthLogs/blob/master/LICENSE).


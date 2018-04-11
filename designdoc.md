components:

- `server.py`
  - everything is read-only
  - `links.csv` contains the links; re-read on every GET for now
    - format: `path/to/file,key,expiry-date` (expiry-date can be None)
  - if key (in the URL) isn't the correct format, throw
  - if file doesn't exist, throw
  - if file can't be read, throw
  - catch all exceptions and return a 404 (we don't want to leak file existence or such)
- `url`: shell script which SSH's and appends to csv => don't deal with auth

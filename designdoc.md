components:

- `server.py`
  - everything is read-only
  - `links.csv` contains the links; re-read on every GET for now
    - format: `key,path/to/file,expiry-date` (expiry-date can be None)
  - if key (in the URL) isn't the correct format, throw
  - if filename doesn't match, throw
  - if file doesn't exist or can't be read, throw
  - catch all exceptions and return a 404 (we don't want to leak file existence or such)
- `url`: shell script which SSH's and appends to csv => don't deal with auth

# Amplitude Pipeline — Pseudocode

---

## Function 1: `extract_amplitude_data(start_time, end_time, api_key, secret_key)`

**Purpose:** Request a day's worth of event data from the Amplitude Export API and save it as a zip file.

```
LOAD secret credentials from a .env file

DEFINE FUNCTION extract_amplitude_data(start_time, end_time, api_key, secret_key)

  SET url      = Amplitude EU export API endpoint
  SET params   = { start: start_time, end: end_time }

  SEND GET request to url
    WITH Basic Auth credentials (api_key, secret_key)
    AND  query parameters = params

  IF response status is 200 (success) THEN
    PRINT "Data successfully retrieved"
    SAVE response bytes to ./data/data.zip
    PRINT "The data.zip file has been saved"
    RETURN True

  ELSE
    PRINT error status code and error message
    RETURN False

  END IF

END FUNCTION

-- MAIN EXECUTION --
READ api_key    FROM environment variable AMP_API_KEY
READ secret_key FROM environment variable AMP_SECRET_KEY

SET yesterday   = today's date minus 1 day
SET start_time  = yesterday formatted as YYYYMMDD + "T00"   (midnight, start of day)
SET end_time    = yesterday formatted as YYYYMMDD + "T23"   (11 PM, end of day)

CALL extract_amplitude_data(start_time, end_time, api_key, secret_key)
```

---

## Function 2: `extract_json_files(zip_path, output_dir)`

**Purpose:** Decompress a two-level archive (`.zip` → `.gz` → newline-delimited JSON) and save individual JSON files grouped by hour into an output directory.

> **Naming note:** `read_filepath` → `zip_path` (clarifies it must be a zip), `write_filepath` → `output_dir` (clarifies it's a folder, not a single file).

```
ACTIVATE virtual environment

IMPORT libraries for:
  - logging
  - reading zip archives
  - reading gz (gzip) files
  - parsing JSON

INSTALL any missing libraries into the virtual environment

DEFINE FUNCTION extract_json_files(zip_path = "./data/data.zip", output_dir = "./data/")

  OPEN zip_path as an archive

  IF zip_path is NOT a valid zip file THEN
    LOG error and stop
  END IF

  LOG size of the zip file
  LOG "Zip file opened successfully"

  FOR each compressed .gz file inside the zip archive DO

    IF the inner file is NOT a .gz file THEN
      SKIP to next file
    END IF

    OPEN the .gz file and decompress it

    LOG size of the .gz file
    LOG ".gz file decompressed successfully"

    TRY
      FOR each line in the decompressed content DO

        PARSE the line as a JSON object

        READ the "hour" field from the JSON object
          (format expected: YYYY-MM-DD HH)

        IF the date in "hour" is on or between start_time and end_time THEN
          SAVE the JSON object to output_dir
            using filename based on the hour value
          LOG "File saved successfully"
          PRINT "File saved successfully"
        END IF

      END FOR

    CATCH any exception DO
      LOG the exception details

    END TRY

  END FOR

END FUNCTION

-- MAIN EXECUTION --
CALL extract_json_files()
```

---

## Notes for implementation

| Pseudocode term        | Likely Python equivalent                        |
|------------------------|-------------------------------------------------|
| `zip_path`             | `str` or `pathlib.Path` parameter               |
| `output_dir`           | `str` or `pathlib.Path` parameter               |
| "valid zip file"       | `zipfile.is_zipfile()`                          |
| "open zip archive"     | `zipfile.ZipFile()`                             |
| "open .gz file"        | `gzip.open()`                                   |
| "parse line as JSON"   | `json.loads(line)`                              |
| "READ hour field"      | `record["hour"]` or `record.get("hour")`        |
| "LOG"                  | `logging.info()` / `logging.exception()`        |
| "CATCH any exception"  | `except Exception as e:`                        |

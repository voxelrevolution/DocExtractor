# Invoice Benchmark Data

Store expected and predicted invoice extraction outputs as JSON.

## Format Options

### Option A: JSON Array
```
[
  {"extraction_id": "doc-1", "vendor": {"value": "ACME"}, "total": {"value": "11.00"}, "line_items": []}
]
```

### Option B: JSON Object with `records`
```
{
  "records": [
    {"extraction_id": "doc-1", "vendor": {"value": "ACME"}, "total": {"value": "11.00"}, "line_items": []}
  ]
}
```

## Usage
Run the evaluation script with paths to expected and predicted files.

### CSV Output
Use `--csv` for a compact CSV summary.

## Manifest
Use manifest.example.json as a template to track benchmark documents.

# PMC Document Verification UI

A modern, responsive HTML/CSS/JavaScript interface for the PMC Document Verification API.

## Features

- ✅ Support for multiple document types: Index 2, NOC, and No Dues
- ✅ Add multiple documents in a single request
- ✅ Dynamic form fields based on selected document type
- ✅ Support for array fields (e.g., multiple names, buyers, sellers)
- ✅ Real-time validation
- ✅ Beautiful, modern UI with responsive design
- ✅ Detailed accuracy results with field-level breakdown
- ✅ Error handling and loading states

## Usage

### Option 1: Open directly in browser

Simply open `index.html` in your web browser. The API URL defaults to `http://localhost:5002`.

### Option 2: Serve with a local web server

For better compatibility (especially with CORS), you can serve the files using a simple HTTP server:

```bash
# Using Python 3
cd ui_html
python3 -m http.server 8080

# Using Python 2
python -m SimpleHTTPServer 8080

# Using Node.js (if you have http-server installed)
npx http-server -p 8080
```

Then open `http://localhost:8080` in your browser.

## API Configuration

1. Make sure your API server is running on `http://localhost:5002` (or update the API URL in the UI)
2. Start the API server:
   ```bash
   ./run_api.sh
   # or
   uvicorn api.main:app --host 0.0.0.0 --port 5002
   ```

## How to Use

1. **Configure API URL** (if different from default)
   - Enter the API base URL in the configuration section

2. **Add Documents**
   - Click "+ Add Document" to add a new document
   - Select the document type (Index 2, NOC, or No Dues)
   - Enter the download URL for the document
   - Fill in all required fields based on the document type

3. **Array Fields**
   - For fields that accept multiple values (like Name, Seller, Buyer), you can add multiple entries
   - Click "+ Add [Field Name]" to add more entries
   - Click "Remove" to remove an entry

4. **Submit**
   - Click "🚀 Submit for Verification" to process all documents
   - Wait for processing (this may take 10-30 seconds per document)
   - View results with accuracy scores

5. **View Results**
   - See summary statistics (total documents, successful, failed, average accuracy)
   - View detailed results for each document including:
     - Overall accuracy score
     - Field-level accuracy breakdown
     - Comparison of actual vs predicted values
     - Extracted fields

## Document Types and Fields

### Index 2
- Document_number/ दस्त क्रमांक (text)
- Seller/देनारा (array of text)
- Buyer/घेणारा (array of text)
- property_address_with_gat_numbers/ पत्ता (textarea)

### NOC
- Name (array of text)
- Flat No (text)
- Address (textarea)

### No Dues
- Name (array of text)
- Address (textarea)
- Amount (text)

## File Structure

```
ui_html/
├── index.html      # Main HTML structure
├── styles.css      # Styling and layout
├── script.js       # JavaScript functionality
└── README.md       # This file
```

## Browser Compatibility

- Chrome/Edge (recommended)
- Firefox
- Safari
- Modern mobile browsers

## Notes

- The UI makes requests to the API endpoint at `/api/v1/verify`
- All documents are sent in a single API request
- Processing time depends on document size and complexity (typically 10-30 seconds per document)
- Accuracy scores range from 0.0 to 1.0 (displayed as percentages)

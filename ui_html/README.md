# PMC/RTS Document Verification UI

A modern, responsive HTML/CSS/JavaScript interface for the upgraded PMC/RTS Document Verification API.

## Features

- ✅ Support for multiple document types: Index 2, NOC, and No Dues
- ✅ Add multiple documents in a single request
- ✅ Dynamic form fields based on selected document type
- ✅ Support for array fields (e.g., multiple names, buyers, sellers)
- ✅ Real-time validation
- ✅ Beautiful, modern UI with responsive design
- ✅ Detailed accuracy results with field-level breakdown
- ✅ Error handling and loading states
- ✅ **Updated for new async API** - Bearer token authentication
- ✅ **Test Mode** - Manual webhook result entry for local testing

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

### Required Setup

1. **Set Bearer Token** in your API server `.env` file:
   ```bash
   BEARER_TOKEN=your_bearer_token_here
   ```

2. Make sure your API server is running on `http://localhost:5002` (or update the API URL in the UI)

3. Start the API server:
   ```bash
   ./run_api.sh
   # or
   uvicorn api.main:app --host 0.0.0.0 --port 5002
   ```

4. Start Celery worker (required for async processing):
   ```bash
   ./run_celery_worker.sh
   # or
   celery -A core.celery worker --loglevel=info
   ```

### New System Requirements

- **Bearer Token Authentication**: Required for `/api/v1/verify` endpoint
- **Application Number (appNo)**: Required field in request
- **Asynchronous Processing**: Results are sent via webhook (not in HTTP response)
- **Celery**: Background task processing required

## How to Use

1. **Configure API Settings**
   - Enter the API base URL (default: `http://localhost:5002`)
   - **Enter Bearer Token** (REQUIRED) - Must match `BEARER_TOKEN` in server `.env`
   - Enter API Token (optional) - Only if `API_TOKEN` is set on server
   - **Enter Application Number (appNo)** (REQUIRED) - Unique identifier for this request

2. **Enable Test Mode (for Local Testing)**
   - Check "Test Mode - Manual Result Entry" checkbox
   - This allows you to manually paste webhook results JSON after submission
   - Useful for local testing without setting up a webhook receiver

3. **Add Documents**
   - Click "+ Add Document" to add a new document
   - Select the document type (Index 2, NOC, or No Dues)
   - Enter the download URL for the document
   - Fill in all required fields based on the document type

4. **Array Fields**
   - For fields that accept multiple values (like Name, Seller, Buyer), you can add multiple entries
   - Click "+ Add [Field Name]" to add more entries
   - Click "Remove" to remove an entry

5. **Submit**
   - Click "🚀 Submit for Verification" to process all documents
   - **New System**: You'll receive an immediate acknowledgment (not full results)
   - Processing happens asynchronously in the background (10-30 seconds per document)
   - Results are sent via webhook when processing completes

6. **View Results (Test Mode)**
   - After submission, if Test Mode is enabled, you'll see a section to paste webhook results
   - Copy the webhook response JSON from your server logs or webhook receiver
   - Paste it into the textarea and click "Process Results"
   - View detailed results with accuracy scores

7. **View Results (Production/Webhook)**
   - In production, results are automatically sent to your webhook URL
   - Your webhook endpoint should receive a POST request with the full results
   - Results include:
     - Summary statistics (total documents, successful, failed, average accuracy)
     - Detailed results for each document including:
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

### API Changes (New System)

- **Bearer Token Required**: The `/api/v1/verify` endpoint now requires `Authorization: Bearer <token>` header
- **Asynchronous Processing**: API returns immediately with acknowledgment, processing happens in background
- **Webhook Delivery**: Results are sent via POST to configured `WEBHOOK_URL` (not in HTTP response)
- **appNo Field**: Required field in request body for tracking

### Request Format

```json
{
  "service_name": "PT5",
  "appNo": "SJG635YS",
  "documents": [...]
}
```

### Response Format (Immediate)

```json
{
  "success": true,
  "service_name": "PT5",
  "appNo": "SJG635YS"
}
```

### Webhook Response Format

The webhook receives the full results (same structure as old system's HTTP response):

```json
{
  "success": true,
  "service_name": "PT5",
  "total_documents": 2,
  "successful": 2,
  "failed": 0,
  "average_accuracy": 0.92,
  "results": [...]
}
```

### Local Testing

- Use **Test Mode** to manually paste webhook results for testing
- Check server logs or Celery logs to see when processing completes
- Copy webhook response JSON and paste into Test Mode section

### Production Setup

- Configure `WEBHOOK_ENABLE=true` in server `.env`
- Set `WEBHOOK_URL` to your webhook receiver endpoint
- Set `WEBHOOK_TOKEN` for webhook authentication
- Your webhook endpoint should accept POST requests with results

### Processing

- All documents are sent in a single API request
- Processing time depends on document size and complexity (typically 10-30 seconds per document)
- Accuracy scores range from 0.0 to 1.0 (displayed as percentages)
- Processing happens asynchronously via Celery workers

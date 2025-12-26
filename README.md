# Document Verification System - Production Version

A modular, production-ready document verification system for Maharashtra Government (PMC) integration.

## 🎯 Overview

This system verifies government documents (Index 2, NOC, No Dues) by:
1. Processing documents through LLM models
2. Extracting information using pre-defined prompts
3. Calculating accuracy by comparing with actual data
4. Returning field-level accuracy results

## 🏗️ Architecture

```
Doc Verifier/
├── api/                    # FastAPI application (API layer)
│   ├── main.py            # FastAPI app entry point
│   ├── routes/            # API route handlers
│   │   └── verification.py
│   └── models/            # Pydantic models for API
│       └── schemas.py
├── core/                   # Core business logic (modular)
│   ├── document_processor.py
│   ├── accuracy_calculator.py
│   └── service_registry.py
├── ui_html/                # HTML/CSS/JavaScript frontend
│   ├── index.html         # Main UI
│   ├── script.js          # JavaScript logic
│   ├── styles.css         # Styling
│   ├── start.sh           # Start script
│   └── stop.sh            # Stop script
├── config/                 # Configuration management
│   ├── settings.py        # Settings from .env
│   └── document_types.py  # Document type definitions
├── utils/                  # Utility functions
│   └── file_handler.py
├── prompts/                # Prompt templates
│   └── Prompts.Md
├── .env                    # Environment variables
├── requirements.txt       # Python dependencies
└── README.md
```

## ✨ Features

- ✅ **Modular Architecture**: API, Core, UI completely separated
- ✅ **RESTful API**: FastAPI with Swagger/OpenAPI documentation
- ✅ **Token Optimization**: Per document type toggle via `.env`
- ✅ **Production Frontend**: HTML/CSS/JavaScript UI
- ✅ **Service Registry**: Easy extensibility for future services
- ✅ **Hybrid Accuracy**: Fuzzy matching + semantic embeddings
- ✅ **Production Ready**: Error handling, timeouts, logging

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file (see `SETUP.md` for details):

```env
GITHUB_TOKEN=your_github_token_here
TOKEN_OPTIMIZATION_INDEX_2=false
TOKEN_OPTIMIZATION_NOC=true
TOKEN_OPTIMIZATION_NO_DUES=true
```

### 3. Run API Server

```bash
./run_api.sh
# Or: uvicorn api.main:app --host 0.0.0.0 --port 5002 --reload
```

Visit: http://localhost:5002/docs

### 4. Run HTML UI

```bash
cd ui_html
./start.sh
```

Visit: http://localhost:8081

## 📚 Documentation

- **[SETUP.md](SETUP.md)**: Detailed setup instructions
- **[API_INTEGRATION.md](API_INTEGRATION.md)**: PMC integration guide
- **Swagger UI**: http://localhost:5002/docs (when API is running)

## 🔧 Token Optimization

Control token optimization per document type via `.env`:

```env
# Disable for Index 2 (keeps full resolution)
TOKEN_OPTIMIZATION_INDEX_2=false

# Enable for NOC and No Dues (reduces tokens by 60-80%)
TOKEN_OPTIMIZATION_NOC=true
TOKEN_OPTIMIZATION_NO_DUES=true
```

## 🔌 API Usage

### Verify Documents

**POST** `/api/v1/verify`

```json
{
  "service_name": "PT5",
  "documents": [
    {
      "download_url": "https://pmc.gov.in/docs/doc1.pdf",
      "document_type": "Index 2",
      "actual_data": {
        "Document_number/ दस्त क्रमांक": "13862/2021",
        "Seller/देनारा": ["..."],
        "Buyer/घेणारा": ["..."],
        "property_address_with_gat_numbers/ पत्ता": "..."
      }
    }
  ]
}
```

See [API_INTEGRATION.md](API_INTEGRATION.md) for complete integration guide.

## 🎨 Extensibility

### Adding New Services

1. Register in `core/service_registry.py`:
```python
service_registry.register_service(
    service_name="NEW_SERVICE",
    document_types=["Document Type 1", "Document Type 2"],
    display_name="New Service",
    description="Description"
)
```

2. Add document type in `config/document_types.py`
3. Add prompt in `prompts/Prompts.Md`

### Adding New Document Types

1. Add to `config/document_types.py`
2. Add prompt section in `prompts/Prompts.Md`
3. Register with service in `core/service_registry.py`

## 📊 Accuracy Calculation

The system uses hybrid accuracy calculation:
- **Fuzzy Matching**: RapidFuzz for string similarity
- **Semantic Embeddings**: multilingual-e5-base for semantic understanding
- **Field-Level**: Individual accuracy for each field
- **Overall**: Average accuracy across all fields

## 🔒 Security

- Environment variables for sensitive data
- Input validation via Pydantic models
- Error handling and logging
- Timeout protection (120s per document)

## 📝 License

[Add your license here]

## 🤝 Support

For issues or questions:
- Check [SETUP.md](SETUP.md) for setup issues
- Review [API_INTEGRATION.md](API_INTEGRATION.md) for integration help
- Check API docs: http://localhost:5002/docs


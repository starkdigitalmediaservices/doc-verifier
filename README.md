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

- ✅ **Asynchronous Processing**: Celery-based background task processing
- ✅ **Modular Architecture**: API, Core, UI completely separated
- ✅ **RESTful API**: FastAPI with Swagger/OpenAPI documentation
- ✅ **Webhook Integration**: Results delivered via webhook POST
- ✅ **Bearer Token Auth**: Industry-standard OAuth 2.0 authentication
- ✅ **Token Optimization**: Per document type toggle via `.env`
- ✅ **Production Frontend**: HTML/CSS/JavaScript UI
- ✅ **Service Registry**: Easy extensibility for future services
- ✅ **Hybrid Accuracy**: Fuzzy matching + semantic embeddings
- ✅ **Production Ready**: Error handling, timeouts, logging, scalability

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# 1. Create .env file
cp .env.example .env
# Edit .env and add your GITHUB_TOKEN and BEARER_TOKEN

# 2. Start all services
docker-compose up -d

# 3. Check services
docker-compose ps
curl http://localhost:5002/api/v1/health
```

**Services started:**
- ✅ API Server: http://localhost:5002
- ✅ API Docs: http://localhost:5002/docs
- ✅ Redis: Running on port 6379
- ✅ Celery Worker: Processing background tasks

### Option 2: Local Development

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start Redis (required)
docker run -d -p 6379:6379 --name redis redis:7-alpine
# Or: sudo systemctl start redis (if installed)

# 3. Create .env file
cp .env.example .env
# Edit .env and add your tokens

# 4. Start all services
./start_local.sh
# Or manually:
# Terminal 1: ./run_api.sh
# Terminal 2: ./run_celery_worker.sh
```

### 4. Run HTML UI (Optional)

```bash
cd ui_html
./start.sh
```

Visit: http://localhost:8081

**📖 For detailed setup instructions, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)**

## 📚 Documentation

- **[PMC_RTS_INTEGRATION_GUIDE.md](PMC_RTS_INTEGRATION_GUIDE.md)**: Complete integration guide for PMC/RTS developers ⭐
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)**: Quick reference card for API integration
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)**: Complete deployment guide (local & production)
- **[CHANGES_ANALYSIS.md](CHANGES_ANALYSIS.md)**: Detailed analysis of backend upgrades
- **[API_FORMAT_COMPARISON.md](API_FORMAT_COMPARISON.md)**: Old vs New API format comparison
- **[SALES_DEMO_GUIDE.md](SALES_DEMO_GUIDE.md)**: Guide for demonstrating the system
- **Swagger UI**: http://localhost:5002/docs (when API is running)

## 🔄 Architecture Changes

This system has been upgraded to use **asynchronous processing**:

- **Old System**: Synchronous API (blocks client for 10-30 seconds)
- **New System**: Asynchronous API (instant response, results via webhook)

**Key Components:**
- **FastAPI**: REST API server
- **Celery**: Background task queue
- **Redis**: Message broker for Celery
- **Webhook**: Results delivery mechanism

See [CHANGES_ANALYSIS.md](CHANGES_ANALYSIS.md) for complete details.

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

**Headers:**
```http
Authorization: Bearer your_bearer_token_here
Content-Type: application/json
```

**Request:**
```json
{
  "service_name": "PT5",
  "appNo": "SJG635YS",
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

**Response (Immediate):**
```json
{
  "success": true,
  "service_name": "PT5",
  "appNo": "SJG635YS"
}
```

**Results Delivery:**
- Results are sent via **webhook POST** to configured `WEBHOOK_URL`
- Processing happens asynchronously in background
- Full results structure same as old system

**⚠️ Important:** 
- Bearer token is **REQUIRED** for this endpoint
- Results are delivered via webhook, not in HTTP response
- See [API_FORMAT_COMPARISON.md](API_FORMAT_COMPARISON.md) for migration guide

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


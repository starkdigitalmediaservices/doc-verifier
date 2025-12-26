// Document type configurations
const DOCUMENT_TYPES = {
    'Index 2': {
        fields: [
            { name: 'Document_number/ दस्त क्रमांक', type: 'text', isArray: false },
            { name: 'Seller/देनारा', type: 'text', isArray: true },
            { name: 'Buyer/घेणारा', type: 'text', isArray: true },
            { name: 'property_address_with_gat_numbers/ पत्ता', type: 'textarea', isArray: false }
        ]
    },
    'NOC': {
        fields: [
            { name: 'Name', type: 'text', isArray: true },
            { name: 'Flat No', type: 'text', isArray: false },
            { name: 'Address', type: 'textarea', isArray: false }
        ]
    },
    'No Dues': {
        fields: [
            { name: 'Name', type: 'text', isArray: true },
            { name: 'Address', type: 'textarea', isArray: false },
            { name: 'Amount', type: 'text', isArray: false }
        ]
    }
};

let documentCounter = 0;
const documents = [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('addDocumentBtn').addEventListener('click', addDocument);
    document.getElementById('submitBtn').addEventListener('click', submitDocuments);
    document.getElementById('clearBtn').addEventListener('click', clearAll);
});

function addDocument() {
    documentCounter++;
    const docId = `doc-${documentCounter}`;
    
    const docCard = document.createElement('div');
    docCard.className = 'document-card';
    docCard.id = docId;
    
    docCard.innerHTML = `
        <div class="document-card-header">
            <h3>Document #${documentCounter}</h3>
            <button class="btn btn-danger" onclick="removeDocument('${docId}')">Remove</button>
        </div>
        <div class="form-group">
            <label>Document Type:</label>
            <select class="doc-type-select" onchange="updateDocumentFields('${docId}', this.value)">
                <option value="">Select Document Type</option>
                <option value="Index 2">Index 2</option>
                <option value="NOC">NOC</option>
                <option value="No Dues">No Dues</option>
            </select>
        </div>
        <div class="form-group">
            <label>Download URL:</label>
            <input type="url" class="doc-url-input" placeholder="https://pmc.gov.in/uploads/doc.pdf or Google Drive link">
            <small style="color: var(--text-secondary); font-size: 0.85rem; display: block; margin-top: 5px;">
                💡 Supports direct URLs and Google Drive sharing links (automatically converted)
            </small>
        </div>
        <div class="doc-fields-container"></div>
    `;
    
    document.getElementById('documentsContainer').appendChild(docCard);
    documents.push({ id: docId, type: null, url: '', fields: {} });
    
    // Add event listener for URL input
    const urlInput = docCard.querySelector('.doc-url-input');
    if (urlInput) {
        urlInput.addEventListener('input', () => updateDocumentData(docId));
    }
    
    updateSubmitButton();
}

function removeDocument(docId) {
    const docCard = document.getElementById(docId);
    if (docCard) {
        docCard.remove();
        const index = documents.findIndex(d => d.id === docId);
        if (index > -1) {
            documents.splice(index, 1);
        }
        updateSubmitButton();
    }
}

function updateDocumentFields(docId, docType) {
    const docCard = document.getElementById(docId);
    const fieldsContainer = docCard.querySelector('.doc-fields-container');
    const docIndex = documents.findIndex(d => d.id === docId);
    
    if (docIndex === -1) return;
    
    documents[docIndex].type = docType;
    fieldsContainer.innerHTML = '';
    
    if (!docType || !DOCUMENT_TYPES[docType]) {
        updateSubmitButton();
        return;
    }
    
    const fields = DOCUMENT_TYPES[docType].fields;
    
    fields.forEach(field => {
        const fieldGroup = document.createElement('div');
        fieldGroup.className = 'form-group';
        
        if (field.isArray) {
            fieldGroup.className += ' array-field-group';
            fieldGroup.innerHTML = `
                <label>${field.name}:</label>
                <div class="array-items-container" data-field="${field.name}">
                    <div class="array-item">
                        <input type="${field.type === 'textarea' ? 'text' : field.type}" 
                               class="array-field-input" 
                               data-field="${field.name}" 
                               placeholder="Enter ${field.name}">
                        <button type="button" class="btn btn-danger" onclick="removeArrayItem(this)">Remove</button>
                    </div>
                </div>
                <button type="button" class="add-item-btn" onclick="addArrayItem('${docId}', '${field.name}', '${field.type}')">+ Add ${field.name}</button>
            `;
        } else {
            if (field.type === 'textarea') {
                fieldGroup.innerHTML = `
                    <label>${field.name}:</label>
                    <textarea class="doc-field-input" data-field="${field.name}" placeholder="Enter ${field.name}"></textarea>
                `;
            } else {
                fieldGroup.innerHTML = `
                    <label>${field.name}:</label>
                    <input type="${field.type}" class="doc-field-input" data-field="${field.name}" placeholder="Enter ${field.name}">
                `;
            }
        }
        
        fieldsContainer.appendChild(fieldGroup);
    });
    
    // Initialize fields in documents array
    documents[docIndex].fields = {};
    fields.forEach(field => {
        if (field.isArray) {
            documents[docIndex].fields[field.name] = [''];
        } else {
            documents[docIndex].fields[field.name] = '';
        }
    });
    
    // Add event listeners for field changes
    fieldsContainer.querySelectorAll('.doc-field-input, .array-field-input').forEach(input => {
        input.addEventListener('input', () => updateDocumentData(docId));
    });
    
    updateSubmitButton();
}

function addArrayItem(docId, fieldName, fieldType) {
    const docCard = document.getElementById(docId);
    const container = docCard.querySelector(`[data-field="${fieldName}"]`);
    
    const arrayItem = document.createElement('div');
    arrayItem.className = 'array-item';
    arrayItem.innerHTML = `
        <input type="${fieldType === 'textarea' ? 'text' : fieldType}" 
               class="array-field-input" 
               data-field="${fieldName}" 
               placeholder="Enter ${fieldName}">
        <button type="button" class="btn btn-danger" onclick="removeArrayItem(this)">Remove</button>
    `;
    
    container.appendChild(arrayItem);
    
    // Add event listener
    arrayItem.querySelector('input').addEventListener('input', () => updateDocumentData(docId));
    
    updateDocumentData(docId);
}

function removeArrayItem(button) {
    const container = button.closest('.array-items-container');
    if (container && container.children.length > 1) {
        button.closest('.array-item').remove();
        const docId = button.closest('.document-card').id;
        updateDocumentData(docId);
    } else {
        alert('At least one item is required for this field.');
    }
}

function updateDocumentData(docId) {
    const docCard = document.getElementById(docId);
    const docIndex = documents.findIndex(d => d.id === docId);
    
    if (docIndex === -1) return;
    
    // Update URL
    const urlInput = docCard.querySelector('.doc-url-input');
    documents[docIndex].url = urlInput ? urlInput.value : '';
    
    // Update fields
    const fields = DOCUMENT_TYPES[documents[docIndex].type]?.fields || [];
    
    fields.forEach(field => {
        if (field.isArray) {
            const inputs = docCard.querySelectorAll(`.array-field-input[data-field="${field.name}"]`);
            documents[docIndex].fields[field.name] = Array.from(inputs).map(input => input.value).filter(v => v.trim() !== '');
        } else {
            const input = docCard.querySelector(`.doc-field-input[data-field="${field.name}"]`);
            documents[docIndex].fields[field.name] = input ? input.value : '';
        }
    });
    
    updateSubmitButton();
}

function updateSubmitButton() {
    const submitBtn = document.getElementById('submitBtn');
    const hasValidDocuments = documents.some(doc => 
        doc.type && 
        doc.url && 
        doc.url.trim() !== '' &&
        Object.values(doc.fields).some(val => 
            Array.isArray(val) ? val.length > 0 && val.some(v => v.trim() !== '') : val.trim() !== ''
        )
    );
    
    submitBtn.disabled = !hasValidDocuments;
}

function clearAll() {
    if (confirm('Are you sure you want to clear all documents?')) {
        document.getElementById('documentsContainer').innerHTML = '';
        documents.length = 0;
        documentCounter = 0;
        document.getElementById('resultsSection').classList.add('hidden');
        document.getElementById('errorSection').classList.add('hidden');
        updateSubmitButton();
    }
}

async function submitDocuments() {
    const apiUrl = document.getElementById('apiUrl').value.trim();
    if (!apiUrl) {
        showError('Please provide an API URL');
        return;
    }
    
    // Validate all documents
    const validDocuments = documents.filter(doc => 
        doc.type && 
        doc.url && 
        doc.url.trim() !== '' &&
        Object.values(doc.fields).some(val => 
            Array.isArray(val) ? val.length > 0 && val.some(v => v.trim() !== '') : val.trim() !== ''
        )
    );
    
    if (validDocuments.length === 0) {
        showError('Please add at least one valid document with all required fields filled.');
        return;
    }
    
    // Build request payload
    const payload = {
        service_name: 'PT5',
        documents: validDocuments.map(doc => {
            // Ensure array fields are arrays (not empty arrays if they have no values)
            const actualData = { ...doc.fields };
            const docTypeConfig = DOCUMENT_TYPES[doc.type];
            if (docTypeConfig) {
                docTypeConfig.fields.forEach(field => {
                    if (field.isArray) {
                        // Ensure it's an array and has at least one value
                        if (!Array.isArray(actualData[field.name]) || actualData[field.name].length === 0) {
                            // This shouldn't happen due to validation, but handle it gracefully
                            actualData[field.name] = actualData[field.name] || [];
                        }
                    }
                });
            }
            return {
                download_url: doc.url,
                document_type: doc.type,
                actual_data: actualData
            };
        })
    };
    
    // Show loading
    document.getElementById('loadingSection').classList.remove('hidden');
    document.getElementById('resultsSection').classList.add('hidden');
    document.getElementById('errorSection').classList.add('hidden');
    document.getElementById('submitBtn').disabled = true;
    
    // Get API token if provided
    const apiTokenInput = document.getElementById('apiToken');
    const apiToken = apiTokenInput ? apiTokenInput.value.trim() : '';
    
    console.log('API Token from input:', apiToken ? `"${apiToken.substring(0, 3)}..." (${apiToken.length} chars)` : '(empty)');
    
    const headers = {
        'Content-Type': 'application/json'
    };
    
    // Add API token to headers if provided
    if (apiToken) {
        headers['X-API-Token'] = apiToken;
        console.log('✅ API Token will be sent in headers');
    } else {
        console.warn('⚠️ API Token is empty - request may fail if API_TOKEN is set on server');
    }
    
    // Debug: Log what we're sending
    console.log('Sending request to:', `${apiUrl}/api/v1/verify`);
    console.log('Headers:', Object.keys(headers));
    console.log('Payload:', payload);
    
    try {
        const response = await fetch(`${apiUrl}/api/v1/verify`, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(payload)
        });
        
        // Check if response is OK before parsing JSON
        if (!response.ok) {
            // Try to get error message from JSON response
            let errorMessage = `HTTP ${response.status}: ${response.statusText}`;
            try {
                const errorData = await response.json();
                errorMessage = errorData.detail || errorData.message || errorMessage;
            } catch (e) {
                // If response is not JSON, use status text
                const text = await response.text();
                if (text) {
                    errorMessage = text.substring(0, 200); // Limit length
                }
            }
            
            // Special handling for 401 (missing token)
            if (response.status === 401) {
                errorMessage = `Authentication Error: ${errorMessage}. Please check your API token.`;
            }
            
            throw new Error(errorMessage);
        }
        
        const data = await response.json();
        displayResults(data);
    } catch (error) {
        // Better error message handling
        let errorMsg = error.message;
        if (errorMsg === 'Failed to fetch') {
            errorMsg = 'Failed to connect to API. Please check:\n1. API is running at the URL shown\n2. API token is correct (if required)\n3. No CORS issues';
        }
        showError(`Error: ${errorMsg}`);
    } finally {
        document.getElementById('loadingSection').classList.add('hidden');
        document.getElementById('submitBtn').disabled = false;
        updateSubmitButton();
    }
}

function displayResults(data) {
    const resultsSection = document.getElementById('resultsSection');
    const summarySection = document.getElementById('summarySection');
    const detailedResults = document.getElementById('detailedResults');
    
    // Display summary
    summarySection.innerHTML = `
        <div class="summary-card">
            <h4>Total Documents</h4>
            <div class="value">${data.total_documents || 0}</div>
        </div>
        <div class="summary-card">
            <h4>Successful</h4>
            <div class="value success">${data.successful || 0}</div>
        </div>
        <div class="summary-card">
            <h4>Failed</h4>
            <div class="value error">${data.failed || 0}</div>
        </div>
        <div class="summary-card">
            <h4>Average Accuracy</h4>
            <div class="value ${getAccuracyClass(data.average_accuracy)}">${formatAccuracy(data.average_accuracy)}</div>
        </div>
        ${data.processing_time_seconds ? `
        <div class="summary-card">
            <h4>Processing Time</h4>
            <div class="value">${data.processing_time_seconds.toFixed(2)}s</div>
        </div>
        ` : ''}
    `;
    
    // Display detailed results
    detailedResults.innerHTML = '';
    
    if (data.results && data.results.length > 0) {
        data.results.forEach((result, index) => {
            const resultCard = document.createElement('div');
            resultCard.className = 'document-result';
            
            const accuracyClass = getAccuracyClass(result.accuracy);
            const accuracyBadgeClass = getAccuracyBadgeClass(result.accuracy);
            
            resultCard.innerHTML = `
                <div class="document-result-header">
                    <div>
                        <span class="success-indicator ${result.success ? 'success' : 'failed'}"></span>
                        <strong>${result.document_type}</strong>
                    </div>
                    <div class="accuracy-badge ${accuracyBadgeClass}">
                        ${formatAccuracy(result.accuracy)}
                    </div>
                </div>
                <div class="form-group">
                    <label>Document URL:</label>
                    <a href="${result.document_url}" target="_blank" style="color: var(--primary-color); word-break: break-all;">${result.document_url}</a>
                </div>
                ${result.error ? `
                    <div class="error-section" style="margin-top: 15px;">
                        <strong>Error:</strong> ${result.error}
                    </div>
                ` : ''}
                ${result.fields_accuracy && Object.keys(result.fields_accuracy).length > 0 ? `
                    <h4 style="margin-top: 20px; margin-bottom: 15px;">Field Accuracy Details:</h4>
                    ${Object.entries(result.fields_accuracy).map(([fieldName, fieldData]) => {
                        const fieldAccClass = getAccuracyClass(fieldData.accuracy);
                        return `
                            <div class="field-accuracy ${fieldAccClass}">
                                <h5>${fieldName} - ${formatAccuracy(fieldData.accuracy)}</h5>
                                <div class="field-comparison">
                                    <div class="comparison-item">
                                        <label>Actual:</label>
                                        <div class="value">${escapeHtml(String(fieldData.actual || ''))}</div>
                                    </div>
                                    <div class="comparison-item">
                                        <label>Predicted:</label>
                                        <div class="value">${escapeHtml(String(fieldData.predicted || ''))}</div>
                                    </div>
                                </div>
                                ${fieldData.method ? `
                                    <div class="method-badge">
                                        Method: ${fieldData.method}${fieldData.details ? ` - ${fieldData.details}` : ''}
                                    </div>
                                ` : ''}
                            </div>
                        `;
                    }).join('')}
                ` : ''}
                ${result.extracted_fields && Object.keys(result.extracted_fields).length > 0 ? `
                    <details style="margin-top: 20px;">
                        <summary style="cursor: pointer; font-weight: 600; margin-bottom: 10px;">Extracted Fields</summary>
                        <pre style="background: var(--bg-color); padding: 15px; border-radius: 6px; overflow-x: auto; font-size: 0.9rem;">${JSON.stringify(result.extracted_fields, null, 2)}</pre>
                    </details>
                ` : ''}
            `;
            
            detailedResults.appendChild(resultCard);
        });
    }
    
    resultsSection.classList.remove('hidden');
}

function showError(message) {
    const errorSection = document.getElementById('errorSection');
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.textContent = message;
    errorSection.classList.remove('hidden');
    resultsSection.classList.add('hidden');
}

function formatAccuracy(accuracy) {
    if (accuracy === null || accuracy === undefined) return 'N/A';
    return `${(accuracy * 100).toFixed(2)}%`;
}

function getAccuracyClass(accuracy) {
    if (accuracy === null || accuracy === undefined) return '';
    if (accuracy >= 0.9) return 'success';
    if (accuracy >= 0.7) return 'medium';
    return 'error';
}

function getAccuracyBadgeClass(accuracy) {
    if (accuracy === null || accuracy === undefined) return '';
    if (accuracy >= 0.9) return 'high';
    if (accuracy >= 0.7) return 'medium';
    return 'low';
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

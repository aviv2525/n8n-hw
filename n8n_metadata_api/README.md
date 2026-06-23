# Intelligent Cloud Document Analyst

## Overview

Intelligent Cloud Document Analyst is an end-to-end document intelligence system built with **n8n**, **Google Gemini**, **Python Flask**, **Google Sheets**, and **Gmail**.

The system automatically detects new documents uploaded to Google Drive, extracts their content, analyzes them using Google Gemini, enriches the results through a custom Metadata API, stores the results in Google Sheets, and sends real-time email notifications.

The solution supports both **TXT** and **PDF** documents and simulates a real-world enterprise Document Intelligence workflow.

---

# Project Workflow

```text
Google Drive Trigger
        ↓
Download File
        ↓
PDF Text Extractor API (Flask + PyMuPDF)
        ↓
Build Prompt
        ↓
Gemini Analysis API
        ↓
Metadata Enrichment API
        ↓
Google Sheets
        ↓
Gmail Notification
```
![Workflow](screenshots/WorkFlow%20-%20whitout%20Agent.png)

# Features

- Automatic document detection from Google Drive
- TXT document processing
- PDF document processing using PyMuPDF
- AI-powered document analysis using Google Gemini
- Structured JSON output generation
- Metadata enrichment via custom Flask API
- Department routing logic
- Sensitivity classification
- UUID generation
- Google Sheets integration
- Gmail notifications
- Fully automated end-to-end workflow

---

# Technologies Used

| Component           | Technology        |
| ------------------- | ----------------- |
| Workflow Automation | n8n               |
| AI Analysis         | Google Gemini API |
| Metadata Service    | Python Flask      |
| PDF Processing      | PyMuPDF           |
| Storage             | Google Sheets     |
| Notifications       | Gmail             |
| Container Platform  | Docker            |
| Cloud Storage       | Google Drive      |

---

# PDF Text Extraction

PDF files are processed using a custom Flask endpoint and the PyMuPDF library.

The API extracts human-readable text from uploaded PDF files before sending the content to Gemini for analysis.

Endpoint:

```http
POST /extract-text
```

Supported file types:

- TXT
- PDF

Response example:

```json
{
  "filename": "invoice.pdf",
  "file_type": "pdf",
  "data": "Invoice Number: 1001..."
}
```

---

# Gemini Analysis

The extracted document text is sent to Google Gemini using an HTTP Request node.

Gemini returns structured JSON containing:

- Summary
- Classification
- Sentiment
- Entities
- Action Items
- Confidence Score

Supported classifications:

- invoice
- report
- contract
- ticket
- article
- other

---

# Metadata Enrichment

The custom Flask Metadata API enriches Gemini results by adding:

- Document ID (UUID)
- Department Routing
- Sensitivity Level
- Routing Tag
- Processing Timestamp
- Adjusted Confidence Score

Department Mapping:

| Classification | Department |
| -------------- | ---------- |
| invoice        | Finance    |
| contract       | Legal      |
| report         | Management |
| ticket         | Support    |
| article        | Research   |
| other          | General    |

---

# Google Sheets Output

Each processed document generates a new row containing:

- document_id
- filename
- file_type
- processed_at
- classification
- department
- sentiment
- confidence_score
- adjusted_confidence_score
- sensitivity
- routing_tag
- summary
- people
- organizations
- dates
- amounts
- action_items

---

# Email Notifications

After successful processing, Gmail automatically sends a notification containing:

- File name
- Classification
- Department
- Sensitivity Level
- Routing Tag
- Document Summary

---

# Sample Documents

The project was tested using:

### TXT Documents

- invoice_january.txt
- invoice_february.txt
- supplier_contract.txt
- monthly_report.txt
- purchase_order.txt
- security_incident.txt
- confidential_financial_report.txt

### PDF Documents

- INVOICE PDF VERSION.pdf

---

# API Endpoints

### Health Check

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

### Categories

```http
GET /categories
```

### Sensitivity Classification

```http
POST /sensitivity
```

### PDF/TXT Extraction

```http
POST /extract-text
```

### Metadata Enrichment

```http
POST /enrich
```

---

# Screenshots

The repository includes screenshots demonstrating:

- Complete n8n Workflow
- PDF Text Extraction
- Google Sheets Results Database
- Gmail Notification
- Flask Health Endpoint
- Successful Workflow Executions

---

# Author

Aviv Malul

B.Sc. Computer Science Graduate

Oz VeRuach – AI Engineering Program

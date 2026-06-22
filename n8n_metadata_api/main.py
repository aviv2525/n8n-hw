from flask import Flask, request, jsonify
import fitz  # PyMuPDF
import uuid
from datetime import datetime

app = Flask(__name__)

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

@app.get("/categories")
def categories():
    return jsonify({
        "categories": ["invoice", "report", "contract", "ticket", "article", "other"]
    })

@app.post("/sensitivity")
def sensitivity():
    data = request.get_json()
    text = str(data).lower()

    if any(word in text for word in ["confidential", "internal executive", "do not distribute"]):
        level = "confidential"
    elif any(word in text for word in ["amount", "$", "contract", "invoice", "revenue", "profit"]):
        level = "internal"
    else:
        level = "public"

    return jsonify({"sensitivity": level})

@app.post("/extract-text")
def extract_text():
    uploaded_file = request.files.get("file")

    if not uploaded_file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = uploaded_file.filename
    file_type = filename.split(".")[-1].lower()

    if file_type == "pdf":
        pdf_bytes = uploaded_file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        text = ""
        for page in doc:
            text += page.get_text() + "\n"

        doc.close()

    elif file_type == "txt":
        text = uploaded_file.read().decode("utf-8", errors="ignore")

    else:
        return jsonify({"error": "Unsupported file type"}), 400

    return jsonify({
        "filename": filename,
        "file_type": file_type,
        "data": text
    })

@app.post("/enrich")
def enrich():
    data = request.get_json()

    classification = data.get("classification", "other")
    confidence_score = float(data.get("confidence_score", 0))

    dept_map = {
        "invoice": "Finance",
        "contract": "Legal",
        "report": "Management",
        "ticket": "Support",
        "article": "Research",
        "other": "General"
    }

    text = str(data).lower()

    if any(word in text for word in ["confidential", "internal executive", "do not distribute"]):
        sensitivity_level = "confidential"
    elif any(word in text for word in ["amount", "$", "contract", "invoice", "revenue", "profit"]):
        sensitivity_level = "internal"
    else:
        sensitivity_level = "public"

    if sensitivity_level == "confidential":
        routing_tag = "escalate"
    elif confidence_score < 0.7:
        routing_tag = "needs-review"
    else:
        routing_tag = "auto-approved"

    entities = data.get("entities", {})

    return jsonify({
        **data,
        "document_id": str(uuid.uuid4()),
        "department": dept_map.get(classification, "General"),
        "sensitivity": sensitivity_level,
        "routing_tag": routing_tag,
        "processed_at": datetime.utcnow().isoformat(),
        "adjusted_confidence_score": round(confidence_score, 2),

        "people": ", ".join(entities.get("people", [])),
        "organizations": ", ".join(entities.get("organizations", [])),
        "dates": ", ".join(entities.get("dates", [])),
        "amounts": ", ".join(entities.get("amounts", [])),
        "action_items": " | ".join(data.get("action_items", []))
    })

if __name__ == "__main__":
    app.run(port=8000, debug=True)
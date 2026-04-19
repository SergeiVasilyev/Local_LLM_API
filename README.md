# Local LLM API – Receipt Processing with Python

This project demonstrates how to use a **local Large Language Model (LLM)** to extract structured data from receipt images and process it in Python.

The main idea:
> Convert unstructured data (image of a receipt) → into structured JSON → and use it in code.

---

## 🚀 Features

- Run LLM locally using LM Studio
- Send image + prompt via API
- Extract structured JSON from model response
- Process and save data using Python
- Works fully offline

---

## 🧠 How It Works

Pipeline:

```
Image → LLM (LM Studio) → JSON → Python processing
```

Steps:
1. Load receipt image
2. Convert image to base64
3. Send request to LM Studio API
4. Model analyzes image and returns response
5. Extract JSON from response
6. Save or process the data

---

## 🛠️ Technologies Used

- Python 3
- LM Studio (local LLM server)
- Model: `qwen3.5-0.8b`
- REST API (HTTP requests)

---

## 📦 Project Structure

```
.
├── main.py              # Main script
├── data/                # Input images (receipts)
├── *.json               # Output files (results)
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Install LM Studio

Download and install:
👉 https://lmstudio.ai

---

### 2. Download Model

Inside LM Studio:
- Search for: `qwen3.5-0.8b`
- Download the model
- Load it into memory (RAM)

---

### 3. Start Local Server

In LM Studio:
- Go to **Local Server**
- Start server on:
```
http://127.0.0.1:1234
```

---

### 4. Install Python Dependencies

```bash
pip install requests
```

---

## ▶️ How to Run

1. Put your receipt image into `data/` folder

2. Update image path in `main.py`:

```python
image_path = "data/your_image.jpg"
```

3. Run script:

```bash
python main.py
```

---

## 🧾 Example Prompt

```text
The image shows a receipt from a store.
Extract the data and return JSON with fields:
store, date, items, total.
If something is missing, leave it empty.
```

---

## 📤 Example Output

```json
{
  "store": "BILTEMMA",
  "date": "03.04.2026 16:57",
  "items": [
    {
      "name": "PANEL WIPE",
      "price": "6.55"
    }
  ],
  "total": "14.10"
}
```

---

## 🧩 Main Functions

### `image_to_base64()`
Converts image into base64 format for API request.

---

### `lmstudio_generate_with_image()`
Sends request to LM Studio with image and prompt.

---

### `extract_json_from_response()`
Extracts clean JSON from model response (removes markdown).

---

### `save_result_to_file()`
Saves JSON result into `.json` file.

---

## ⚠️ Limitations

- Small models may make mistakes
- Processing can be slow on weak hardware
- OCR quality depends on image quality
- Not all receipts are perfectly parsed

---

## 💡 Possible Improvements

- Use a larger model
- Add GUI (web app)
- Store results in database
- Add analytics (expense tracking)
- Improve prompt engineering

---

## 🔄 Other Use Cases

The same approach can be used for:

- 📄 Document processing
- 📊 Log analysis
- 📚 Language learning (flashcards)
- 💼 Accounting automation
- 🧾 Expense tracking

---

## 📌 Notes

- Make sure LM Studio server is running before starting Python script
- Increase timeout if your model is slow
- Use clear images for better results

---

## 🎓 Purpose

This project was created as part of a university assignment to demonstrate practical use of local LLMs.

---

## 🙌 Acknowledgements

- LM Studio
- Qwen model creators

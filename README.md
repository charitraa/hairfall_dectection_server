# HairFall Detection 🩺 — Smart Hair & Scalp Analysis Assistant

Detect hair loss, dandruff, and scalp issues instantly from photos.

HairFall Detection is an intelligent backend server that uses Deep Learning with Django to analyze scalp images, detect hairfall stages, dandruff, and other common hair/scalp conditions, providing users with insights and care recommendations.

**Workflow:**
Upload a scalp photo ➔ Get instant analysis ➔ View detection results ➔ Receive personalized advice (via Gemini integration)

---

## Features

* Hairfall & Dandruff Detection using custom-trained CNN models
* Scalp Condition Analysis (hair thinning, density estimation, flake detection)
* Gemini AI Integration for natural language advice and chat
* User-Specific Image Storage and history
* Secure & Protected API with authentication
* RESTful API built with Django REST Framework
* Future-ready for mobile integration, reports & recommendations

---

## Tech Stack

| Component           | Technology                                                         |
| ------------------- | ------------------------------------------------------------------ |
| Backend             | Django, Django REST Framework                                      |
| API                 | Django REST Framework                                              |
| Deep Learning Model | TensorFlow / Keras (CNN) – `checkpoints.keras` & `cnn_model.keras` |
| Database            | SQLite (dev)                                                       |
| Image Processing    | OpenCV, Pillow                                                     |
| Authentication      | Django JWT / Session Auth                                          |
| AI Chat             | Google Gemini API                                                  |
| Deployment          | Standard Django (Gunicorn/Nginx ready)                             |

---

## Project Structure

```
texthairfall_dectection_server/
├── detection/              # Main detection app
│   ├── gemini_hair_analysis.py  # Gemini integration for advice
│   └── ...
├── hairfall_detection/     # Core ML app
│   └── ...
├── media/scans/user_<id>/  # User-uploaded scalp images
│   └── ...
├── models/
│   ├── checkpoints.keras
│   └── cnn_model.keras
├── user/                   # User authentication app
│   └── ...
├── .gitignore
├── db.sqlite3
├── manage.py
└── requirements.txt
```

---

## API Endpoints (Protected)

| Method | Endpoint             | Description                             |
| ------ | -------------------- | --------------------------------------- |
| POST   | `/api/user/create/`  | User signup                             |
| POST   | `/api/user/login/`   | User login                              |
| GET    | `/api/user/me/`      | Get user profile                        |
| POST   | `/api/detect/`       | Upload scalp image → Analyze hair/scalp |
| GET    | `/api/scans/my/`     | List user's scans                       |
| POST   | `/api/chat/`         | Chat with Gemini for hair care advice   |
| GET    | `/api/chat/history/` | Retrieve chat history                   |

**Example Detection Response:**

```json
{
  "message": "Scalp analyzed successfully",
  "data": {
    "id": "user_scan_123",
    "image": "/media/scans/user_123/test_dandruff_1.jpg",
    "detected_issues": ["Moderate Dandruff", "Early Hair Thinning"],
    "confidence": 88.5,
    "created_at": "2025-11-30T09:05:35Z"
  },
  "recommendations": "Use anti-dandruff shampoo, consult if thinning progresses."
}
```

**Gemini Chat Example:**

```json
{
  "reply": "Based on your scalp photo, I see signs of dandruff. Try tea tree oil shampoo twice a week!"
}
```

---

## Setup & Installation

```bash
git clone https://github.com/charitraa/hairfall_dectection_server.git
cd hairfall_dectection_server

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start server
python manage.py runserver
```

**Server runs at:** `http://127.0.0.1:8000`

> Note: Add your Google Gemini API key in `settings.py` or `.env` if required.

---

## Future Roadmap

* Disease/condition severity scoring (Norwood scale for baldness)
* Personalized treatment recommendations
* Mobile app integration
* User progress tracking over time
* Enhanced model with more conditions (psoriasis, alopecia, etc.)
* Push notifications for care reminders

---

## Contributing

Contributions are welcome!

1. Fork the repo
2. Create a feature branch
3. Commit changes
4. Open a Pull Request

---

## License

MIT License (add LICENSE file if needed)
Made with ❤️ for better hair health!
⭐ Star the repo: [GitHub](https://github.com/charitraa/hairfall_dectection_server) if you find it useful!

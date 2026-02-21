# 🛡️ NoorGuard Ultimate - Islamic Digital Protection Ecosystem

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.0.0-brightgreen" alt="Version">
  <img src="https://img.shields.io/badge/License-MIT-blue" alt="License">
  <img src="https://img.shields.io/badge/Platforms-Android%20%7C%20Web%20%7C%20iOS-orange" alt="Platforms">
</p>

## 📱 Overview

**NoorGuard Ultimate** is an enterprise-level Islamic Digital Protection Ecosystem designed to protect families with AI-powered content filtering, behavioral monitoring, and Islamic features. It includes a Parent App, Child App, Web Dashboard, and comprehensive backend services.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     NoorGuard Ultimate                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │  Android     │  │  Android     │  │   Web        │   │
│  │  Parent App  │  │  Child App   │  │  Dashboard   │   │
│  │   (Kotlin)   │  │   (Kotlin)   │  │  (Next.js)   │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
│          │                 │                  │           │
│          └─────────────────┴──────────────────┘           │
│                           │                               │
│                    ┌──────▼──────┐                      │
│                    │  FastAPI    │                      │
│                    │  Backend    │                      │
│                    │  (Python)   │                      │
│                    └─────────────┘                      │
│                           │                               │
│         ┌─────────────────┼─────────────────┐           │
│         │                 │                 │           │
│    ┌────▼────┐      ┌────▼────┐      ┌────▼────┐      │
│    │PostgreSQL│      │  Redis  │      │    AI   │      │
│    │Database │      │  Cache  │      │ Engine  │      │
│    └─────────┘      └─────────┘      └─────────┘      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## ✨ Features

### 🔒 Smart Content Shield
- Local VPN-based traffic inspection
- DNS-level adult website blocking
- Custom DNS server support
- AI NSFW image detection (offline model)
- Keyword-based filtering engine
- Encrypted browsing log

### 🤖 AI Behavioral Monitoring
- Suspicious search pattern detection
- Late night usage anomaly detection
- Addiction risk scoring system
- AI-based content classification

### 📱 App Control System
- App lock with biometric
- Time-based restriction
- Daily usage quota
- Salah-time auto lock
- Ramadan special lock mode
- School focus mode

### 👨‍👩‍👧‍👦 Parent Control Panel
- Real-time device status
- Screen time analytics (charts)
- Remote lock / unlock
- Instant alert system
- Multi-child management
- Device group management

### 🕌 Salah & Islamic Integration
- Auto prayer time (GPS based)
- Adhan notification
- App pause during Salah
- Daily Hadith push
- Quran Ayah widget
- Dhikr reminder mode

### 🔐 Security Layer
- AES-256 encryption
- JWT + Refresh tokens
- Device binding
- Root detection
- Anti-uninstall protection
- Anti-tamper protection
- Screenshot block for sensitive screens
- Biometric authentication

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Android Apps** | Kotlin + Jetpack Compose + Material 3 |
| **Backend** | FastAPI (Python 3.11+) |
| **Database** | PostgreSQL 15 |
| **Cache** | Redis 7 |
| **Web Dashboard** | Next.js 14 + Tailwind CSS |
| **Real-time** | WebSocket |
| **AI** | TensorFlow Lite + scikit-learn |
| **Deployment** | Docker + Nginx |

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+
- Android Studio (for Android apps)
- Docker & Docker Compose

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
```

### Web Dashboard Setup

```bash
cd web-dashboard

# Install dependencies
npm install

# Run development server
npm run dev
```

### Docker Deployment

```bash
cd docker

# Start all services
docker-compose up -d
```

## 📁 Project Structure

```
noorguard-ultimate/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── api/              # API Routes
│   │   ├── core/             # Configuration
│   │   ├── models/           # SQLAlchemy Models
│   │   ├── schemas/          # Pydantic Schemas
│   │   ├── services/         # Business Logic
│   │   └── ml/               # AI/ML Modules
│   └── requirements.txt
│
├── android-parent/            # Parent App (Kotlin)
│   └── app/src/main/
│
├── android-child/             # Child App (Kotlin)
│   └── app/src/main/
│
├── web-dashboard/            # Next.js Dashboard
│   └── src/
│
├── docker/                   # Docker Configuration
│   ├── docker-compose.yml
│   └── nginx/
│
└── README.md
```

## 🔧 API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/refresh` - Refresh token
- `GET /api/v1/auth/me` - Get current user

### Children Management
- `GET /api/v1/children` - List children
- `POST /api/v1/children` - Create child
- `GET /api/v1/children/{id}` - Get child details
- `PUT /api/v1/children/{id}` - Update child
- `DELETE /api/v1/children/{id}` - Delete child

### Monitoring
- `POST /api/v1/children/activity` - Log activity
- `GET /api/v1/children/{id}/activities` - Get activities
- `GET /api/v1/children/{id}/analytics` - Get analytics

### Prayer Times
- `GET /api/v1/prayers/times` - Get prayer times
- `GET /api/v1/prayers/hadith/random` - Get random hadith
- `GET /api/v1/prayers/dhikr/morning` - Morning dhikr

## 📱 Mobile Apps

### Parent App Features
- Dashboard with child status overview
- Real-time monitoring
- Device management
- Screen time analytics
- Remote lock/unlock
- Prayer times widget

### Child App Features
- Protected browsing experience
- Prayer time notifications
- Daily hadith and dhikr
- Screen time limits
- Ramadan mode

## 🔒 Security Features

1. **AES-256 Encryption** - All sensitive data is encrypted
2. **JWT Authentication** - Secure token-based auth
3. **Biometric Support** - Fingerprint/Face ID authentication
4. **Device Binding** - Limit devices per user
5. **Rate Limiting** - Prevent abuse
6. **IP Blocking** - Security against attacks

## 📈 Deployment

### Production Deployment

1. **Configure Environment Variables**
```bash
cp backend/.env.example backend/.env
# Edit .env with production values
```

2. **Build Docker Images**
```bash
cd docker
docker-compose build
```

3. **Start Services**
```bash
docker-compose up -d
```

4. **Setup Nginx (Optional)**
```bash
# Add SSL certificates to docker/nginx/ssl/
docker-compose restart nginx
```

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) first.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Islamic prayer time calculations from [PrayTimes](http://praytimes.org/)
- UI components from [Material Design 3](https://m3.material.io/)
- Icons from [Material Icons](https://fonts.google.com/icons)

---

<p align="center">
  Made with ❤️ for Muslim families
</p>

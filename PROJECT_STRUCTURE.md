# NoorGuard Ultimate - Islamic Digital Protection Ecosystem
# Project Directory Structure

```
noorguard-ultimate/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── api/               # API Routes
│   │   │   ├── v1/
│   │   │   │   ├── auth.py
│   │   │   │   ├── devices.py
│   │   │   │   ├── children.py
│   │   │   │   ├── monitoring.py
│   │   │   │   ├── settings.py
│   │   │   │   ├── analytics.py
│   │   │   │   ├── prayers.py
│   │   │   │   └── websocket.py
│   │   │   └── __init__.py
│   │   ├── core/              # Core Configuration
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   ├── encryption.py
│   │   │   └── database.py
│   │   ├── models/            # SQLAlchemy Models
│   │   │   ├── user.py
│   │   │   ├── device.py
│   │   │   ├── child.py
│   │   │   ├── activity.py
│   │   │   ├── prayer.py
│   │   │   └── analytics.py
│   │   ├── schemas/           # Pydantic Schemas
│   │   │   ├── user.py
│   │   │   ├── device.py
│   │   │   ├── child.py
│   │   │   ├── activity.py
│   │   │   └── prayer.py
│   │   ├── services/          # Business Logic
│   │   │   ├── auth_service.py
│   │   │   ├── device_service.py
│   │   │   ├── monitoring_service.py
│   │   │   ├── prayer_service.py
│   │   │   ├── analytics_service.py
│   │   │   └── ai_service.py
│   │   ├── ml/               # AI/ML Modules
│   │   │   ├── classifier.py
│   │   │   ├── anomaly_detector.py
│   │   │   └── content_filter.py
│   │   ├── utils/             # Utilities
│   │   │   ├── prayer_times.py
│   │   │   ├── location.py
│   │   │   └── helpers.py
│   │   ├── websocket/         # WebSocket Manager
│   │   │   └── manager.py
│   │   ├── cache/            # Redis Cache
│   │   │   └── redis_client.py
│   │   └── main.py           # Application Entry
│   ├── requirements.txt
│   ├── .env.example
│   └── alembic.ini
│
├── android-parent/            # Parent App (Kotlin)
│   ├── app/
│   │   ├── src/main/
│   │   │   ├── java/com/noorguard/parent/
│   │   │   │   ├── ui/
│   │   │   │   │   ├── theme/
│   │   │   │   │   ├── screens/
│   │   │   │   │   │   ├── auth/
│   │   │   │   │   │   ├── dashboard/
│   │   │   │   │   │   ├── devices/
│   │   │   │   │   │   ├── children/
│   │   │   │   │   │   ├── analytics/
│   │   │   │   │   │   ├── settings/
│   │   │   │   │   │   └── prayer/
│   │   │   │   │   └── components/
│   │   │   │   ├── data/
│   │   │   │   │   ├── repository/
│   │   │   │   │   ├── api/
│   │   │   │   │   └── local/
│   │   │   │   ├── domain/
│   │   │   │   │   ├── model/
│   │   │   │   │   ├── repository/
│   │   │   │   │   └── usecase/
│   │   │   │   ├── service/
│   │   │   │   │   ├── WebSocketService.kt
│   │   │   │   │   ├── NotificationService.kt
│   │   │   │   │   ├── PrayerService.kt
│   │   │   │   │   └── BackgroundService.kt
│   │   │   │   ├── di/
│   │   │   │   └── NoorguardApp.kt
│   │   │   ├── res/
│   │   │   │   ├── values/
│   │   │   │   ├── drawable/
│   │   │   │   └── mipmap/
│   │   │   └── AndroidManifest.xml
│   │   └── build.gradle.kts
│   └── gradle.properties
│
├── android-child/             # Child App (Kotlin)
│   ├── app/
│   │   ├── src/main/
│   │   │   ├── java/com/noorguard/child/
│   │   │   │   ├── ui/
│   │   │   │   ├── data/
│   │   │   │   ├── domain/
│   │   │   │   ├── service/
│   │   │   │   ├── di/
│   │   │   │   └── NoorguardChildApp.kt
│   │   │   ├── res/
│   │   │   └── AndroidManifest.xml
│   │   └── build.gradle.kts
│   └── gradle.properties
│
├── web-dashboard/            # Next.js Dashboard
│   ├── src/
│   │   ├── app/
│   │   │   ├── (auth)/
│   │   │   │   ├── login/
│   │   │   │   └── register/
│   │   │   ├── (dashboard)/
│   │   │   │   ├── dashboard/
│   │   │   │   ├── devices/
│   │   │   │   ├── children/
│   │   │   │   ├── analytics/
│   │   │   │   ├── settings/
│   │   │   │   └── prayer/
│   │   │   ├── api/
│   │   │   │   ├── auth/
│   │   │   │   ├── devices/
│   │   │   │   ├── children/
│   │   │   │   └── websocket/
│   │   │   ├── layout.tsx
│   │   │   └── page.tsx
│   │   ├── components/
│   │   │   ├── ui/
│   │   │   ├── charts/
│   │   │   ├── forms/
│   │   │   └── layout/
│   │   ├── lib/
│   │   │   ├── api.ts
│   │   │   ├── auth.ts
│   │   │   ├── websocket.ts
│   │   │   └── utils.ts
│   │   ├── hooks/
│   │   ├── types/
│   │   └── store/
│   ├── public/
│   ├── tailwind.config.ts
│   ├── next.config.js
│   ├── package.json
│   └── tsconfig.json
│
├── docker/
│   ├── backend/
│   │   └── Dockerfile
│   ├── web/
│   │   └── Dockerfile
│   ├── nginx/
│   │   ├── nginx.conf
│   │   └── ssl/
│   ├── postgres/
│   │   └── init.sql
│   ├── redis/
│   │   └── redis.conf
│   └── docker-compose.yml
│
├── docs/
│   ├── API.md
│   ├── DEPLOYMENT.md
│   ├── ARCHITECTURE.md
│   └── ISLAMIC_FEATURES.md
│
├── .gitignore
├── README.md
├── LICENSE
└── SETUP.md
```

## Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT + Refresh Tokens
- **WebSocket**: Socket.IO
- **AI**: TensorFlow Lite + scikit-learn

### Android Apps
- **Language**: Kotlin 1.9+
- **UI**: Jetpack Compose + Material 3
- **Architecture**: MVVM + Clean Architecture
- **DI**: Hilt
- **Networking**: Retrofit + OkHttp
- **Local DB**: Room
- **Security**: AES-256, Biometric

### Web Dashboard
- **Framework**: Next.js 14 (App Router)
- **UI**: Tailwind CSS + Material UI
- **State**: Zustand
- **Charts**: Recharts
- **Auth**: NextAuth.js

### Deployment
- **Container**: Docker + Docker Compose
- **Web Server**: Nginx
- **CI/CD**: GitHub Actions
- **Cloud**: Railway / Render / VPS Ready

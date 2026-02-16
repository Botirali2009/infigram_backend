# 🚀 INFIGRAM API ENDPOINTS

## 🔐 Authentication

### Register
**POST** `/api/auth/register/`
```json
{
  "username": "botirali",
  "email": "botirali@example.com",
  "password": "password123",
  "password2": "password123",
  "first_name": "Botirali",
  "last_name": "Xamidjonov"
}
```

**Response:**
```json
{
  "user": {
    "id": 1,
    "username": "botirali",
    "email": "botirali@example.com",
    "plan": "free"
  },
  "token": "abc123xyz789..."
}
```

---

### Login
**POST** `/api/auth/login/`
```json
{
  "username": "botirali",
  "password": "password123"
}
```

---

### Logout
**POST** `/api/auth/logout/`
Headers: `Authorization: Token abc123xyz789...`

---

### Get Profile
**GET** `/api/auth/profile/`
Headers: `Authorization: Token abc123xyz789...`

---

### Update Profile
**PUT** `/api/auth/profile/`
```json
{
  "first_name": "Yangi",
  "last_name": "Ism",
  "phone": "+998901234567"
}
```

---

## 🤖 Bots

### Get All Bots
**GET** `/api/bots/`
Headers: `Authorization: Token abc123xyz789...`

---

### Create Bot
**POST** `/api/bots/`
```json
{
  "name": "Support Bot",
  "token": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
  "description": "Customer support bot"
}
```

---

### Get Bot Detail
**GET** `/api/bots/{id}/`

---

### Update Bot
**PUT** `/api/bots/{id}/`
```json
{
  "name": "Updated Name",
  "welcome_message": "Salom! Xush kelibsiz",
  "auto_reply_enabled": true,
  "status": "active"
}
```

---

### Delete Bot
**DELETE** `/api/bots/{id}/`

---

### Get Bot Stats
**GET** `/api/bots/{id}/stats/`

---

## 🔄 Auto Replies

### Get Auto Replies
**GET** `/api/bots/{bot_id}/auto-replies/`

---

### Create Auto Reply
**POST** `/api/bots/{bot_id}/auto-replies/`
```json
{
  "keywords": "narx, price, qancha",
  "reply_text": "Narxlar haqida ma'lumot olish uchun /katalog ni yuboring",
  "is_active": true,
  "priority": 1
}
```

---

### Update Auto Reply
**PUT** `/api/auto-replies/{id}/`

---

### Delete Auto Reply
**DELETE** `/api/auto-replies/{id}/`

---

## ❓ FAQs

### Get FAQs
**GET** `/api/bots/{bot_id}/faqs/`

---

### Create FAQ
**POST** `/api/bots/{bot_id}/faqs/`
```json
{
  "question": "Ish vaqtingiz qanday?",
  "answer": "Biz har kuni 9:00 dan 20:00 gacha ishlaymiz",
  "is_active": true,
  "order": 1
}
```

---

## 💬 Chats

### Get All Chats for Bot
**GET** `/api/bot/{bot_id}/chats/`

---

### Get Chat Detail
**GET** `/api/chats/{id}/`

---

### Block/Unblock Chat
**POST** `/api/chats/{id}/block/`

---

### Delete Chat
**DELETE** `/api/chats/{id}/delete/`

---

## 📨 Messages

### Get Messages for Chat
**GET** `/api/messages/chat/{chat_id}/messages/`

---

### Send Message
**POST** `/api/messages/send/`
```json
{
  "chat": 1,
  "text": "Salom! Sizga qanday yordam bera olaman?",
  "message_type": "text"
}
```

---

### Mark as Read
**POST** `/api/messages/{id}/read/`

---

## 📊 Analytics

### Get Daily Stats
**GET** `/api/analytics/bot/{bot_id}/daily/`

---

### Get Bot Overview
**GET** `/api/analytics/bot/{bot_id}/overview/`

---

## 🔑 Authentication

Barcha API endpoints (login va register'dan tashqari) uchun token kerak:

**Header:**
```
Authorization: Token abc123xyz789...
```

---

## 📝 Error Responses

**400 Bad Request:**
```json
{
  "error": "Invalid data"
}
```

**401 Unauthorized:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**404 Not Found:**
```json
{
  "detail": "Not found."
}
```

---

## 🧪 Testing

### Postman Collection
Import qiling va test qiling!

### cURL Example
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```
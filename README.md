# PollEase - A Simple Polling System

PollEase is a web application that allows users to create polls and vote on them. It consists of a **FastAPI** backend and a **React** frontend.

## Features
- Create polls with multiple options
- Fetch latest poll details
- Vote for an option in a poll
- View real-time updates

---

## 🛠️ Tech Stack
### **Backend (FastAPI)**
- FastAPI
- Uvicorn
- SQLite
- Pydantic

### **Frontend (React.js)**
- React (Vite)
- Axios
- TailwindCSS (Optional for styling)

---

## 🚀 How to Run the Project

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/poll-ease.git
cd poll-ease
```

### 2️⃣ Backend Setup (FastAPI)
#### Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```
#### Run Backend
```bash
uvicorn main:app --reload
```
The backend will be available at **http://localhost:8000**.

### 3️⃣ Frontend Setup (React)
#### Install Dependencies
```bash
cd frontend
npm install
```
#### Run Frontend
```bash
npm run dev
```
The frontend will be available at **http://localhost:5173**.

---

## 📌 API Endpoints

### 1️⃣ Create a Poll
```http
POST /polls/
```
**Request Body:**
```json
{
  "question": "Your favorite language?",
  "options": ["Python", "JavaScript", "C++"]
}
```
**Response:**
```json
{
  "message": "Poll created successfully",
  "data": {
    "id": 1,
    "question": "Your favorite language?",
    "options": [{"id": 1, "text": "Python"}, {"id": 2, "text": "JavaScript"}]
  }
}
```

### 2️⃣ Get Latest Poll
```http
GET /polls/latest
```
**Response:**
```json
{
  "id": 1,
  "question": "Your favorite language?",
  "options": [
    {"id": 1, "text": "Python"},
    {"id": 2, "text": "JavaScript"},
    {"id": 3, "text": "C++"}
  ]
}
```

### 3️⃣ Submit a Vote
```http
POST /vote/
```
**Request Body:**
```json
{
  "poll_id": 1,
  "option_id": 2
}
```
**Response:**
```json
{
  "message": "Vote submitted successfully"
}
```

---

## 🎨 Frontend Implementation

### `App.jsx` (React Component)
```jsx
import { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [poll, setPoll] = useState(null);
  const [selectedOption, setSelectedOption] = useState(null);
  const [message, setMessage] = useState("");

  useEffect(() => {
    axios.get("http://localhost:8000/polls/latest")
      .then(response => {
        setPoll(response.data);
      })
      .catch(error => {
        console.error("Error fetching poll:", error);
      });
  }, []);

  const submitVote = () => {
    if (!selectedOption) {
      setMessage("Please select an option before voting.");
      return;
    }
    axios.post("http://localhost:8000/vote/", {
      poll_id: poll.id,
      option_id: selectedOption
    })
      .then(response => {
        setMessage(response.data.message);
      })
      .catch(error => {
        console.error("Error voting:", error);
        setMessage("Failed to submit vote. Try again.");
      });
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Quick Poll</h1>
      {poll ? (
        <div>
          <h2>{poll.question}</h2>
          {poll.options.map(option => (
            <div key={option.id}>
              <input
                type="radio"
                id={option.id}
                name="poll"
                value={option.id}
                onChange={() => setSelectedOption(option.id)}
              />
              <label htmlFor={option.id}>{option.text}</label>
            </div>
          ))}
          <button onClick={submitVote} style={{ marginTop: "20px" }}>Vote</button>
        </div>
      ) : (
        <p>Loading poll...</p>
      )}
      {message && <p>{message}</p>}
    </div>
  );
}

export default App;
```

---

## 🎯 Contributing
- Fork the repository
- Create a new branch
- Make changes and commit
- Open a pull request

## 💬 Support
For any questions, reach out to **your-email@example.com** or create an issue in GitHub.

Happy Coding! 🚀
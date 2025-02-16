const express = require('express');
const app = express();
const port = 8000;

// Example route to handle GET requests for polls
app.get('/polls', (req, res) => {
  // Replace with your logic to fetch polls from the database
  const polls = [
    { id: 1, question: 'What is your favorite color?' },
    { id: 2, question: 'What is your favorite food?' },
  ];
  res.json(polls);
});

app.listen(port, () => {
  console.log(`Server is running on http://127.0.0.1:${port}`);
});

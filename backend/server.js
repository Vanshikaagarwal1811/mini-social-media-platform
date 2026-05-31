const express = require("express");

const app = express();

app.use(express.json());

app.post("/api/users", (req, res) => {
  console.log(req.body);

  res.json({
    success: true,
    message: "User created successfully",
    user: req.body
  });
});

const PORT = 5000;

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
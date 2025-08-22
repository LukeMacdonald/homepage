const express = require("express");

const app = express();

const port = 3033;

app.use(express.json());

app.listen(port, () => {
  console.log(`Server is listening on port ${port}`);
});

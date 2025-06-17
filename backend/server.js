const express = require('express');
const multer = require('multer');
const cors = require('cors');
const path = require('path');
const remixProcessor = require('./remixProcessor');

const app = express();
const port = process.env.PORT || 5000;

app.use(cors());
app.use(express.static('uploads'));

const storage = multer.diskStorage({
  destination: './uploads/',
  filename: (req, file, cb) => {
    cb(null, 'input_' + Date.now() + path.extname(file.originalname));
  }
});
const upload = multer({ storage });

app.post('/api/remix', upload.single('video'), async (req, res) => {
  const inputPath = req.file.path;
  const outputPath = `uploads/remixed_${Date.now()}.mp4`;
  
  try {
    await remixProcessor(inputPath, outputPath);
    res.json({ success: true, url: `${req.protocol}://${req.get('host')}/${path.basename(outputPath)}` });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

app.listen(port, () => {
  console.log(`✅ Server running on http://localhost:${port}`);
});
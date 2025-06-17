const ffmpeg = require('fluent-ffmpeg');
const fs = require('fs');

function remixProcessor(inputPath, outputPath) {
  return new Promise((resolve, reject) => {
    ffmpeg(inputPath)
      // 🎵 Audio Filters
      .audioFilters([
        'asetrate=44100*1.04',    // Pitch slightly up
        'atempo=0.96',            // Speed slightly down
        'equalizer=f=1000:t=q:w=1:g=3' // Boost mids
      ])
      // 🎥 Video Filters
      .videoFilters([
        'hue=s=0', // Black & white tint
        'scale=iw*1.01:ih*1.01', // Slight zoom
        'eq=brightness=0.02:saturation=1.3' // Slight visual change
      ])
      .on('end', () => {
        console.log('✅ Remix complete');
        resolve();
      })
      .on('error', (err) => {
        console.error('❌ Remix failed:', err.message);
        reject(err);
      })
      .save(outputPath);
  });
}

module.exports = remixProcessor;
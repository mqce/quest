#!/usr/bin/env node

const fs = require('fs').promises;
const path = require('path');
const https = require('https');
const http = require('http');
const { URL } = require('url');

// Simple HTTP client
async function fetch(url, options = {}) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const client = urlObj.protocol === 'https:' ? https : http;
    
    const req = client.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; ThumbnailBot/1.0)',
        ...options.headers
      }
    }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return fetch(res.headers.location, options).then(resolve).catch(reject);
      }
      
      const chunks = [];
      res.on('data', chunk => chunks.push(chunk));
      res.on('end', () => {
        const body = Buffer.concat(chunks).toString('utf8');
        resolve({
          ok: res.statusCode >= 200 && res.statusCode < 300,
          status: res.statusCode,
          text: () => Promise.resolve(body),
          buffer: () => Promise.resolve(Buffer.concat(chunks))
        });
      });
    });
    
    req.on('error', reject);
    req.setTimeout(15000, () => {
      req.destroy();
      reject(new Error('Timeout'));
    });
  });
}

// Download image
async function downloadImage(url, outputPath) {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const buffer = await response.buffer();
    await fs.mkdir(path.dirname(outputPath), { recursive: true });
    await fs.writeFile(outputPath, buffer);
    return buffer.length;
  } catch (err) {
    console.error(`  ✗ Failed to download ${url}: ${err.message}`);
    return 0;
  }
}

// Extract images from HTML
function extractImages(html, baseUrl) {
  const images = [];
  
  // Match img tags
  const imgRegex = /<img[^>]+src=["']([^"']+)["'][^>]*>/gi;
  let match;
  while ((match = imgRegex.exec(html)) !== null) {
    try {
      const url = new URL(match[1], baseUrl).href;
      images.push(url);
    } catch (e) {}
  }
  
  // Match og:image
  const ogImageRegex = /<meta[^>]+property=["']og:image["'][^>]+content=["']([^"']+)["'][^>]*>/i;
  match = html.match(ogImageRegex);
  if (match) {
    try {
      const url = new URL(match[1], baseUrl).href;
      images.push(url);
    } catch (e) {}
  }
  
  // Match twitter:image
  const twitterImageRegex = /<meta[^>]+name=["']twitter:image["'][^>]+content=["']([^"']+)["'][^>]*>/i;
  match = html.match(twitterImageRegex);
  if (match) {
    try {
      const url = new URL(match[1], baseUrl).href;
      images.push(url);
    } catch (e) {}
  }
  
  return [...new Set(images)]; // Remove duplicates
}

// Filter out unwanted images
function filterImages(images) {
  const excludePatterns = [
    /logo/i,
    /icon/i,
    /banner/i,
    /avatar/i,
    /profile/i,
    /ad[s_-]/i,
    /button/i,
    /badge/i,
    /emoji/i,
    /favicon/i,
    /sprite/i,
    /thumbnail.*\d+x\d+/i // Tiny thumbnails
  ];
  
  return images.filter(url => {
    // Check size indicators
    if (url.match(/\d+x\d+/)) {
      const sizeMatch = url.match(/(\d+)x(\d+)/);
      if (sizeMatch) {
        const [, w, h] = sizeMatch;
        if (parseInt(w) < 300 || parseInt(h) < 200) {
          return false;
        }
      }
    }
    
    // Check exclude patterns
    return !excludePatterns.some(pattern => pattern.test(url));
  });
}

// Extract YouTube/Vimeo links
function extractVideoLinks(html, baseUrl) {
  const videos = [];
  
  // YouTube
  const youtubeRegex = /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]+)/g;
  let match;
  while ((match = youtubeRegex.exec(html)) !== null) {
    const videoId = match[1];
    videos.push({
      type: 'video',
      src: `https://www.youtube.com/embed/${videoId}`,
      poster: `https://img.youtube.com/vi/${videoId}/maxresdefault.jpg`
    });
  }
  
  // Vimeo
  const vimeoRegex = /vimeo\.com\/(\d+)/g;
  while ((match = vimeoRegex.exec(html)) !== null) {
    const videoId = match[1];
    videos.push({
      type: 'video',
      src: `https://player.vimeo.com/video/${videoId}`,
      poster: null // We'd need Vimeo API for this
    });
  }
  
  return videos;
}

// Collect candidates for a work
async function collectCandidates(work) {
  console.log(`\n${work.title} (${work.id}):`);
  
  const candidates = [];
  const seenUrls = new Set();
  
  // Add existing thumbnail as first candidate if it exists
  if (work.thumbnail) {
    candidates.push({
      type: 'image',
      src: work.thumbnail,
      origin: 'existing'
    });
    console.log(`  + Existing thumbnail: ${work.thumbnail}`);
  }
  
  try {
    // Fetch source page
    console.log(`  Fetching ${work.sourceUrl}...`);
    const response = await fetch(work.sourceUrl);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    
    const html = await response.text();
    
    // Extract and filter images
    let images = extractImages(html, work.sourceUrl);
    images = filterImages(images);
    
    // Extract video links
    const videos = extractVideoLinks(html, work.sourceUrl);
    
    console.log(`  Found ${images.length} candidate images, ${videos.length} videos`);
    
    // Download up to 6-7 images
    const maxImages = 7;
    let downloaded = 0;
    
    for (const imageUrl of images) {
      if (downloaded >= maxImages) break;
      if (seenUrls.has(imageUrl)) continue;
      
      seenUrls.add(imageUrl);
      const ext = imageUrl.match(/\.(jpe?g|png|gif|webp)/i)?.[1] || 'jpg';
      const filename = `${String(candidates.length + 1).padStart(2, '0')}.${ext}`;
      const outputPath = path.join(__dirname, 'media', 'candidates', work.id, filename);
      
      const size = await downloadImage(imageUrl, outputPath);
      if (size > 0) {
        candidates.push({
          type: 'image',
          src: `media/candidates/${work.id}/${filename}`,
          origin: work.sourceUrl
        });
        console.log(`  ✓ Downloaded: ${filename} (${Math.round(size / 1024)}KB)`);
        downloaded++;
      }
    }
    
    // Add video candidates
    for (const video of videos.slice(0, 2)) { // Max 2 videos
      candidates.push(video);
      console.log(`  ✓ Video: ${video.src}`);
    }
    
    console.log(`  Total candidates: ${candidates.length}`);
    
  } catch (err) {
    console.error(`  ✗ Error: ${err.message}`);
  }
  
  return candidates;
}

// Main
async function main() {
  console.log('Thumbnail Candidate Collector\n');
  
  // Load works
  const worksData = await fs.readFile('data/works.json', 'utf8');
  const works = JSON.parse(worksData);
  
  console.log(`Found ${works.length} works to process`);
  
  // Process each work
  const stats = {
    total: works.length,
    withCandidates: 0,
    noCandidates: 0,
    totalCandidates: 0
  };
  
  for (const work of works) {
    const candidates = await collectCandidates(work);
    work.candidates = candidates;
    
    if (candidates.length > 0) {
      stats.withCandidates++;
      stats.totalCandidates += candidates.length;
    } else {
      stats.noCandidates++;
    }
    
    // Small delay to be polite
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  // Save updated works.json
  await fs.writeFile('data/works.json', JSON.stringify(works, null, 2));
  
  console.log('\n=== Summary ===');
  console.log(`Total works: ${stats.total}`);
  console.log(`Works with candidates: ${stats.withCandidates}`);
  console.log(`Works with no candidates: ${stats.noCandidates}`);
  console.log(`Total candidates collected: ${stats.totalCandidates}`);
  console.log(`Average per work: ${(stats.totalCandidates / stats.total).toFixed(1)}`);
  
  if (stats.noCandidates > 0) {
    console.log('\nWorks with no candidates:');
    works.filter(w => !w.candidates || w.candidates.length === 0).forEach(w => {
      console.log(`  - ${w.title} (${w.id})`);
    });
  }
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});

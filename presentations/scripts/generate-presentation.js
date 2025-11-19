#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const pptxgen = require('pptxgenjs');
const html2pptx = require('/home/becker/.claude/skills/pptx/scripts/html2pptx.js');

// Professional orange color scheme for Little Caesars
const colors = {
  primaryOrange: 'F96D00',
  deepOrange: 'E85D04',
  charcoal: '222831',
  coolGray: '546E7A',
  lightBg: 'F5F5F5',
  accentTeal: '4A90A4',
  white: 'FFFFFF'
};

// Parse markdown file
function parseMarkdown(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');

  // Remove YAML frontmatter
  const withoutFrontmatter = content.replace(/^---\n[\s\S]*?\n---\n/, '');

  const slides = [];
  const parts = withoutFrontmatter.split(/\n---\n/);

  for (let part of parts) {
    const slideContent = part.trim();
    if (slideContent) {
      const parsed = parseSlide(slideContent);
      // Only add slides with actual content (title, bullets, or text)
      if (parsed.title || parsed.bullets.length > 0 || parsed.text.length > 0) {
        slides.push(parsed);
      }
    }
  }

  return slides;
}

function parseSlide(content) {
  const lines = content.split('\n');
  let title = '';
  let subtitle = '';
  let bullets = [];
  let text = [];
  let codeBlocks = [];
  let isModule = false;
  let inComment = false;
  let inCodeBlock = false;
  let currentCodeBlock = [];

  for (let line of lines) {
    const trimmed = line.trim();

    // Handle multi-line comments
    if (trimmed.startsWith('<!--')) {
      inComment = true;
    }
    if (trimmed.includes('-->')) {
      inComment = false;
      continue;
    }
    if (inComment) continue;

    // Handle code blocks
    if (trimmed.startsWith('```')) {
      if (inCodeBlock) {
        // End of code block
        codeBlocks.push(currentCodeBlock.join('\n'));
        currentCodeBlock = [];
        inCodeBlock = false;
      } else {
        // Start of code block
        inCodeBlock = true;
      }
      continue;
    }

    if (inCodeBlock) {
      // Preserve original line (not trimmed) to keep indentation
      currentCodeBlock.push(line);
      continue;
    }

    // Skip empty lines and tables
    if (!trimmed || trimmed.startsWith('|')) continue;

    // Headers
    if (trimmed.startsWith('# ')) {
      if (trimmed.includes('Module')) isModule = true;
      title = trimmed.replace(/^# /, '').trim();
    } else if (trimmed.startsWith('## ')) {
      subtitle = trimmed.replace(/^## /, '').trim();
    } else if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
      const bullet = trimmed.replace(/^[- *] /, '').trim();
      // Clean markdown formatting in bullets
      const cleaned = bullet.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')
                           .replace(/_(.*?)_/g, '<i>$1</i>')
                           .replace(/`(.*?)`/g, '$1');
      bullets.push(cleaned);
    } else if (trimmed && !trimmed.startsWith('#')) {
      // Regular text - clean markdown formatting
      const cleaned = trimmed.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>')
                            .replace(/_(.*?)_/g, '<i>$1</i>')
                            .replace(/`(.*?)`/g, '$1');
      text.push(cleaned);
    }
  }

  return { title, subtitle, bullets, text, codeBlocks, isModule, raw: content };
}

function createSlideHTML(slide, index) {
  const { title, subtitle, bullets, text, codeBlocks, isModule } = slide;

  // Determine slide type
  const isTitleSlide = index === 0;
  const isModuleDivider = isModule || title.startsWith('Module');
  const isSummary = title.includes('Takeaway') || title.includes('Summary');

  let html = `<!DOCTYPE html>
<html>
<head>
<style>
html { background: #ffffff; }
body {
  width: 720pt; height: 405pt; margin: 0; padding: 0;
  font-family: Arial, sans-serif;
  display: flex;
  flex-direction: column;
}
</style>
</head>
<body>
`;

  if (isTitleSlide) {
    // Title slide with dark background and orange accent
    html += `
<div style="width: 720pt; height: 405pt; background: #${colors.charcoal}; padding: 0; margin: 0; position: relative;">
  <!-- Content wrapper -->
  <div style="position: absolute; top: 50%; left: 36pt; transform: translateY(-50%); width: 648pt;">
    <div style="border-left: 10pt solid #${colors.primaryOrange}; padding-left: 20pt;">
      <h1 style="color: #${colors.white}; font-size: 38pt; font-weight: bold; margin: 0 0 12pt 0;">${escapeHtml(title)}</h1>
      ${subtitle ? `<h2 style="color: #${colors.white}; font-size: 24pt; font-weight: normal; margin: 0 0 14pt 0;">${escapeHtml(subtitle)}</h2>` : ''}
      ${text.length > 0 ? text.map(t => `<p style="color: #${colors.lightBg}; font-size: 17pt; margin: 6pt 0;">${t}</p>`).join('') : ''}
    </div>
  </div>
</div>`;
  } else if (isModuleDivider) {
    // Module divider - full orange background
    html += `
<div style="width: 720pt; height: 405pt; background: #${colors.primaryOrange}; padding: 0; margin: 0; position: relative;">
  <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 648pt;">
    <h1 style="color: #${colors.white}; font-size: 36pt; font-weight: bold; text-align: center; margin: 0 0 14pt 0;">${escapeHtml(title)}</h1>
    ${subtitle ? `<h2 style="color: #${colors.white}; font-size: 21pt; font-weight: normal; text-align: center; margin: 0;">${escapeHtml(subtitle)}</h2>` : ''}
    ${bullets.length > 0 ? `
      <ul style="color: #${colors.white}; font-size: 17pt; margin-top: 22pt; list-style-type: disc; padding-left: 25pt;">
        ${bullets.map(b => `<li style="margin: 6pt 0;">${b}</li>`).join('')}
      </ul>` : ''}
  </div>
</div>`;
  } else {
    // Content slide with left orange accent bar
    // Dimensions: 720pt × 405pt total
    // Orange bar: 8pt, leaving 712pt
    // Padding: 36pt (top/bottom) = 0.5", 40pt (left/right) for margins
    // Content area: 632pt wide × 333pt tall maximum

    // Limit bullets to prevent overflow (max 6-7 bullets fits comfortably)
    const maxBullets = 7;
    const displayBullets = bullets.slice(0, maxBullets);

    // Adjust font size based on content density
    const totalLines = displayBullets.length + text.length;
    const fontSize = totalLines > 10 ? '11pt' : '12pt';
    const lineHeight = totalLines > 10 ? '1.15' : '1.2';

    html += `
<div style="width: 720pt; height: 405pt; display: flex; background: #${colors.white};">
  <!-- Orange accent bar -->
  <div style="width: 8pt; background: #${colors.primaryOrange};"></div>

  <div style="flex: 1; padding: 36pt 40pt; max-width: 632pt;">
    <!-- Header -->
    <div style="margin-bottom: ${subtitle ? '10pt' : '14pt'};">
      <h1 style="color: #${colors.primaryOrange}; font-size: 26pt; font-weight: bold; margin: 0 0 4pt 0; line-height: 1.1;">${escapeHtml(title)}</h1>
      ${subtitle ? `<h2 style="color: #${colors.coolGray}; font-size: 17pt; font-weight: normal; margin: 0; line-height: 1.2;">${escapeHtml(subtitle)}</h2>` : ''}
    </div>

    <!-- Content -->
    <div style="color: #${colors.charcoal}; font-size: ${fontSize}; line-height: ${lineHeight};">
      ${codeBlocks && codeBlocks.length > 0 ? codeBlocks.map(code => {
        // Convert code block to paragraphs (html2pptx doesn't support <pre>)
        const lines = code.split('\n').filter(line => line.trim() || line.length > 0);
        return `
        <div style="background: #F5F5F5; border-left: 3pt solid #${colors.primaryOrange}; padding: 8pt 12pt; margin: 6pt 0;">
          ${lines.map(line => {
            // Convert spaces to non-breaking spaces to preserve indentation
            const withNbsp = line.replace(/ /g, '\u00A0');
            return `<p style="font-family: 'Courier New', Courier, monospace; font-size: 10pt; margin: 2pt 0; line-height: 1.2;">${escapeHtml(withNbsp)}</p>`;
          }).join('')}
        </div>
      `;
      }).join('') : ''}

      ${text.length > 0 ? text.map(t => `<p style="margin: 4pt 0;">${t}</p>`).join('') : ''}

      ${displayBullets.length > 0 ? `
        <ul style="list-style-type: disc; padding-left: 22pt; margin: 0;">
          ${displayBullets.map(b => `<li style="margin: 4pt 0;">${b}</li>`).join('')}
        </ul>` : ''}
    </div>
  </div>
</div>`;
  }

  html += `
</body>
</html>`;

  return html;
}

function escapeHtml(text) {
  return text.replace(/&/g, '&amp;')
             .replace(/</g, '&lt;')
             .replace(/>/g, '&gt;')
             .replace(/"/g, '&quot;')
             .replace(/'/g, '&#39;');
}

async function main() {
  console.log('Parsing markdown...');
  const slides = parseMarkdown('CE101-Master-Presentation.md');
  console.log(`Found ${slides.length} slides`);

  // Create HTML files
  const htmlDir = path.join('workspace', 'slides-html');
  if (!fs.existsSync(htmlDir)) {
    fs.mkdirSync(htmlDir, { recursive: true });
  }

  console.log('\nGenerating HTML slides...');
  for (let i = 0; i < slides.length; i++) {
    const html = createSlideHTML(slides[i], i);
    const htmlPath = path.join(htmlDir, `slide-${String(i + 1).padStart(3, '0')}.html`);
    fs.writeFileSync(htmlPath, html);
    if ((i + 1) % 10 === 0) {
      console.log(`  Generated ${i + 1}/${slides.length} slides`);
    }
  }
  console.log(`  Generated all ${slides.length} slides`);

  // Create PowerPoint presentation
  console.log('\nCreating PowerPoint presentation...');
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.author = 'CE101 Training';
  pptx.title = 'Context Engineering 101';
  pptx.subject = 'AI Coding Assistant Training for SREs and DevOps';

  for (let i = 0; i < slides.length; i++) {
    const htmlPath = path.join(htmlDir, `slide-${String(i + 1).padStart(3, '0')}.html`);
    try {
      await html2pptx(htmlPath, pptx);
      if ((i + 1) % 10 === 0) {
        console.log(`  Converted ${i + 1}/${slides.length} slides to PowerPoint`);
      }
    } catch (error) {
      console.error(`Error on slide ${i + 1}:`, error.message);
      throw error;
    }
  }

  // Save presentation
  const outputPath = 'CE101-Master-Presentation-Styled.pptx';
  console.log(`\nSaving presentation to ${outputPath}...`);
  await pptx.writeFile({ fileName: outputPath });

  console.log('\n✓ Successfully created styled presentation!');
  console.log(`  Output: ${outputPath}`);
  console.log(`  Slides: ${slides.length}`);
}

main().catch(error => {
  console.error('Error:', error);
  process.exit(1);
});

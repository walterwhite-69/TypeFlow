# [TypeFlow](https://github.com/walterwhite-69/TypeFlow)

<div align="center">

**Create stunning animated SVG text for your GitHub READMEs and projects**

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Vercel](https://img.shields.io/badge/Vercel-Deploy-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

[![Animations](https://img.shields.io/badge/Animations-20+-FF6B6B?style=flat-square)](#-animation-styles-26-types)
[![Fonts](https://img.shields.io/badge/Fonts-7_Local-4ECDC4?style=flat-square)](#-popular-font-options)
[![Customizable](https://img.shields.io/badge/100%25-Customizable-45B7D1?style=flat-square)](#-url-parameters)

<sub>Inspired by [readme-typing-svg](https://github.com/denvercoder1/readme-typing-svg) 💙</sub>

</div>

A beautiful, feature-rich Python Flask application that generates stunning dynamic animated SVGs with 20+ animation styles, custom dropdowns, and realistic effects like fire 🔥. Built with extensive customization options, local fonts for reliable GitHub embeds, and optimized for Vercel deployment.

## ✨ Features

### 🎭 Animation Styles (26+ Types!)

#### Classic Effects
- **typing** - Classic typewriter effect with cursor
- **typewriter** - Letter-by-letter reveal animation
- **fade** - Fade-in with letter stagger
- **slide** - Slide in from left
- **wave** - Smooth wave motion
- **zoom** - Zoom in reveal
- **pulse** - Pulsing scale effect
- **flip** - 3D flip rotation
- **bounce** - Bouncy spring animation
- **stroke** - Handwriting stroke animation

#### Glitch & Distortion
- **glitch** - RGB glitch effect
- **glitch-heavy** - Intense glitchy corruption
- **glitch-scan** - Scanline glitch with color shift
- **corrupt** - Scrambled corruption effect
- **static** - TV static noise effect
- **shake** - Vibrating shake motion

#### Light & Color Effects
- **glow** - Pulsing glow effect
- **neon** - Neon sign with realistic flicker
- **rainbow** - Cycling rainbow hue rotation
- **sparkle** - Sparkling brightness animation
- **gradient-shift** - Smooth gradient color cycling
- **blur-focus** - Blur to focus reveal

#### Special Effects
- **fire** 🔥 - **NEW!** Realistic flame animation with triple-layered glow, flickering, and upward movement
- **rotate3d** - 3D rotation animation
- **matrix** - Matrix rain cascade
- **terminal** - Terminal-style with cursor
- **obfuscated** - Minecraft-style scrambled text (supports `?(text)` syntax)

### 💡 Obfuscated Text Syntax

The `?(text)` syntax lets you scramble specific words while keeping others normal - perfect for creating Minecraft-style text effects!

**How to use:**
Wrap any word in `?()` to make it scramble:

<div align="center">
  <img src="https://animatedsvg.vercel.app/generate?lines=Hello%20%3F%28World%29&animation=flip&size=24" alt="Obfuscated Text">
</div>

This animates "Hello" normally while "World" rapidly scrambles through random characters!

**More Examples:**

<!-- Password with scrambled dots -->
<img src="https://animatedsvg.vercel.app/generate?lines=Password%3A%20%3F%28%E2%80%A2%E2%80%A2%E2%80%A2%E2%80%A2%E2%80%A2%E2%80%A2%29&animation=pulse&size=28" alt="Secret">

<!-- System error message -->
<img src="https://animatedsvg.vercel.app/generate?lines=System%20%3F%28ERROR%29%20Detected&animation=bounce&color=FF0000" alt="Error">

<!-- Mystery reveal -->
<img src="https://animatedsvg.vercel.app/generate?lines=The%20answer%20is%20%3F%2842%29&animation=rotate3d" alt="Mystery">

**Compatible Animations:** flip, bounce, zoom, rotate3d, pulse, slide, obfuscated

**Note:** The `obfuscated` animation scrambles all text by default. Use `?(text)` syntax with other animations for selective scrambling.

### 🎨 Advanced Customization

#### Text & Typography
- **Multi-line support** with semicolon separator
- **Local fonts** - 7 embedded TTF fonts (Fira Code, Inter, JetBrains Mono, Roboto, Poppins, Montserrat, Oswald)
- **Font size** - Customizable from 10px to 100px+
- **Letter spacing** - Adjust spacing between characters

#### Colors & Effects
- **Gradient support** - Use multiple colors separated by commas
- **Gradient angle** - Control gradient direction (0-360°)
- **Background color** - Solid or transparent backgrounds
- **Glow effects** - Neon and shadow effects

#### Animation Control
- **Duration** - Control animation speed (ms)
- **Pause** - Delay between loops (ms)
- **Repeat** - Loop infinitely or play once
- **Stagger delay** - Control letter-by-letter timing
- **Glitch intensity** - Adjust glitch effect strength (1-20)

#### Layout
- **Width & Height** - Custom dimensions
- **Center alignment** - Center or left-align text
- **Multiline** - Stack multiple lines vertically

## 🚀 Usage

### Quick Start

The endpoint is: `https://animatedsvg.vercel.app/generate`

Add parameters using `?` and `&`. **Important:** Use URL encoding for special characters (`;` = `%3B`, space = `%20`, etc.)

### Basic Examples

**Simple typing animation:**

<div align="center">
  <img src="https://animatedsvg.vercel.app/generate?lines=Hello%20World" alt="Typing SVG">
</div>

**Multiple lines (use %3B for semicolons):**

<div align="center">
  <img src="https://animatedsvg.vercel.app/generate?lines=Welcome%20to%20my%20profile%3BI'm%20a%20developer%3BLet's%20build%20something" alt="Multi-line SVG">
</div>

**Choose an animation:**

<!-- Glitch Effect -->
<img src="https://animatedsvg.vercel.app/generate?lines=GLITCH%20EFFECT&animation=glitch-heavy" alt="Glitch">

<!-- Neon Effect -->

<img src="https://animatedsvg.vercel.app/generate?lines=NEON+LIGHTS&animation=neon&font=Fira+Code&color=409EFF%2C+ffffff%2C+000000%2C+fcba03&bg_color=transparent&size=24&width=600&height=100&duration=3000&center=true&repeat=true&letter_spacing=0&glitch_intensity=5&stagger_delay=50&typing_mode=sequential&terminal_color_mode=rainbow&terminal_colors=FF0080%2CFF8000%2CFFFF00%2C00FF00%2C00FFFF%2C0080FF%2C8000FF&border_width=0&border_color=000000&border_radius=0&padding=0" alt="Animated SVG">


**Add colors (use commas for gradients):**

<img src="https://animatedsvg.vercel.app/generate?lines=Colorful%20Text&color=FF6B6B,4ECDC4,45B7D1&animation=fade" alt="Gradient">

**Customize font and size:**

<img src="https://animatedsvg.vercel.app/generate?lines=Custom%20Font&font=JetBrains%20Mono&size=32&animation=slide" alt="Custom Font">

**Complete customization:**

<img src="https://animatedsvg.vercel.app/generate?lines=Line%201%3BLine%202%3BLine%203&animation=wave&font=Poppins&color=FF00FF,00FFFF&size=28&duration=3000&center=true&multiline=true" alt="Custom SVG">

## 📋 URL Parameters Reference

| Parameter | Default | Description | Example Values |
|-----------|---------|-------------|----------------|
| `lines` | "Hello;World!" | Text content (use `%3B` for `;` separator, `%20` for spaces) | `lines=Hello%20World%3BLine%202` |
| `animation` | "typing" | Animation style (see list above) | `animation=wave` |
| `font` | "Fira Code" | Font family (local fonts available) | `font=JetBrains+Mono` |
| `color` | "409EFF" | Text color (hex without #) or gradient | `color=FF6B6B` or `color=FF6B6B,4ECDC4,45B7D1` |
| `bg_color` | "transparent" | Background color | `bg_color=000000` or `bg_color=transparent` |
| `size` | 20 | Font size in pixels | `size=32` |
| `width` | 600 | SVG width in pixels | `width=800` |
| `height` | 100 | SVG height in pixels | `height=150` |
| `duration` | 5000 | Animation duration in milliseconds | `duration=3000` |
| `pause` | 1000 | Pause between animation loops (ms) | `pause=2000` |
| `repeat` | true | Loop animation infinitely | `repeat=true` or `repeat=false` |
| `center` | true | Center text horizontally | `center=true` or `center=false` |
| `multiline` | auto | Stack lines vertically (auto enables for multiple lines) | `multiline=true` |
| `letter_spacing` | 0 | Spacing between letters in pixels | `letter_spacing=2` |
| `glitch_intensity` | 5 | Glitch effect strength (1-20) | `glitch_intensity=15` |
| `stagger_delay` | 50 | Delay between character animations (ms) | `stagger_delay=100` |
| `gradient_angle` | 45 | Gradient direction in degrees (0-360) | `gradient_angle=90` |

## 🎯 Preset Templates

Copy and paste these ready-to-use examples into your README:

### Cyberpunk Theme

<div align="center">
  <img src="https://animatedsvg.vercel.app/generate?lines=CYBERPUNK%3B2077%3BGLITCH&animation=glitch-heavy&color=FF006E,8338EC,3A86FF&size=32&glitch_intensity=10&multiline=true" alt="Cyberpunk">
</div>

### Terminal Style

<div align="center">
  <img src="https://animatedsvg.vercel.app/generate?lines=%24%20python%20app.py%3B%3E%20Server%20running...%3B%3E%20Ready!&animation=terminal&color=00FF00&bg_color=000000&size=24&center=false" alt="Terminal">
</div>

### Matrix Effect

<div align="center">
  <img src="https://animatedsvg.vercel.app/generate?lines=THE%20MATRIX&animation=matrix&color=00FF00&bg_color=000000&size=28" alt="Matrix">
</div>

### Neon Sign

<div align="center">
  <img src="https://animatedsvg.vercel.app/generate?lines=NEON%3BLIGHTS&animation=neon&color=FF00FF,00FFFF&bg_color=0A0A0A&size=36&multiline=true" alt="Neon">
</div>

### Fire Effect

<div align="center">
  <img src="https://animatedsvg.vercel.app/generate?lines=FIRE&animation=fire&color=FF4500,FF6B00,FFD700&size=48" alt="Fire">
</div>

### Rainbow Wave

<div align="center">
  <img src="https://animatedsvg.vercel.app/generate?lines=RAINBOW%20WAVE&animation=rainbow&size=32&duration=3000" alt="Rainbow">
</div>

### Glitch Corruption

<div align="center">
  <img src="https://animatedsvg.vercel.app/generate?lines=CORRUPTED&animation=corrupt&color=FF0000,00FF00,0000FF&size=40&glitch_intensity=15" alt="Corrupt">
</div>

### Retro Gaming

<div align="center">
  <img src="https://animatedsvg.vercel.app/generate?lines=GAME%3BOVER&animation=shake&color=FFD700&bg_color=000080&size=28&multiline=true" alt="Retro">
</div>

## 🛠️ Installation & Deployment

### Local Development

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run locally:**
```bash
python api/app.py
```

3. **Access:**
- Main endpoint: `http://localhost:5000/`

### Deploy to Vercel

1. **Install Vercel CLI:**
```bash
npm i -g vercel
```

2. **Deploy:**
```bash
vercel
```

3. **Production deployment:**
```bash
vercel --prod
```

### Configuration

The project includes `vercel.json` for automatic routing:
```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/api/app"
    }
  ]
}
```

## 🎨 Popular Font Options

- **Fira Code** - Clean coding font with ligatures
- **JetBrains Mono** - Modern monospace
- **Roboto Mono** - Geometric monospace
- **Space Mono** - Retro monospace
- **Orbitron** - Futuristic/sci-fi
- **Press Start 2P** - Retro 8-bit gaming
- **VT323** - Terminal/console style
- **Share Tech Mono** - Tech-inspired
- **Courier New** - Classic typewriter

## 🌟 Examples in the Wild

### GitHub Profile README

<div align="center">
  <img src="https://animatedsvg.vercel.app/generate?lines=Welcome%20to%20my%20profile!%3BI'm%20a%20Full%20Stack%20Developer%3BLet's%20build%20something%20amazing&animation=wave&font=Fira%20Code&color=58A6FF,1F6FEB&size=24" alt="Animated Header">
</div>

### Project Banner

<div align="center">
  <img src="https://animatedsvg.vercel.app/generate?lines=MY%20AWESOME%20PROJECT%3BBuilt%20with%20Python%20%F0%9F%90%8D&animation=neon&color=FF00FF,00FFFF&size=36&multiline=true" alt="Project Banner">
</div>

### Status Badge

<img src="https://animatedsvg.vercel.app/generate?lines=Server%20Online%20%E2%9C%85&animation=terminal&color=00FF00&bg_color=000000&size=20&center=true" alt="Status">

## 🔧 Tech Stack

- **Backend**: Flask 3.0.0 (Python 3.11)
- **Templating**: Jinja2
- **Deployment**: Vercel Serverless Functions
- **Frontend**: Tailwind CSS (demo page)

## 📝 Notes

- All SVGs include `Cache-Control: no-cache` headers for immediate updates
- Animations use CSS `@keyframes` for broad browser support
- Google Fonts are loaded dynamically via CDN
- Character-level animations (wave, fade, matrix) split text into individual `<tspan>` elements

## 🤝 Contributing

Feel free to fork, modify, and extend! Some ideas:
- Add emoji/icon animation support
- Implement path morphing effects
- Create sound wave visualizations
- Add particle effects around text
- Build export functionality (download as SVG/GIF)

## 📜 License

MIT License - Feel free to use in your projects!

---

<div align="center">
  <img src="https://animatedsvg.vercel.app/generate?lines=Made+By+%3F%28walter%29&animation=neon&font=Fira+Code&color=9a1919&bg_color=transparent&size=24&width=600&height=100&duration=3000&center=true&repeat=true&letter_spacing=0&glitch_intensity=5&stagger_delay=50&typing_mode=sequential&terminal_color_mode=rainbow&terminal_colors=FF0080%2CFF8000%2CFFFF00%2C00FF00%2C00FFFF%2C0080FF%2C8000FF&border_width=0&border_color=000000&border_radius=0&padding=0" alt="Animated SVG">
</div>

Built with ⚡ Python & Flask | Optimized for 🚀 Vercel

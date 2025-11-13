from flask import Flask, request, Response, render_template_string, send_from_directory
from urllib.parse import unquote
import os
import random
import re
import time

app = Flask(__name__, static_folder='../static')

# Local font mapping to font files
LOCAL_FONTS = {
    'Fira Code': {'regular': 'FiraCode-Regular.ttf', 'bold': 'FiraCode-Bold.ttf'},
    'Inter': {'regular': 'Inter-Regular.ttf', 'bold': 'Inter-Bold.ttf'},
    'JetBrains Mono': {'regular': 'JetBrainsMono-Regular.ttf', 'bold': 'JetBrainsMono-Regular.ttf'},
    'Roboto': {'regular': 'Roboto-Regular.ttf', 'bold': 'Roboto-Bold.ttf'},
    'Poppins': {'regular': 'Poppins-Regular.ttf', 'bold': 'Poppins-Bold.ttf'},
    'Montserrat': {'regular': 'Montserrat-Regular.ttf', 'bold': 'Montserrat-Bold.ttf'},
    'Oswald': {'regular': 'Oswald-Regular.ttf', 'bold': 'Oswald-Bold.ttf'},
}

# Animation presets - clean and minimalistic
ANIMATION_PRESETS = {
    'fade': {'duration': 2000, 'stagger': 50},
    'wave': {'duration': 3000, 'delay': 100},
    'glitch': {'duration': 2000, 'intensity': 3},
    'slide': {'duration': 2500, 'ease': True},
    'glow': {'duration': 3000, 'flicker': False},
    'pulse': {'duration': 2000, 'scale': 1.1},
    'zoom': {'duration': 2500, 'scale': 1.5},
    'flip': {'duration': 2000, 'axis': 'y'},
    'bounce': {'duration': 1800, 'elastic': True}
}

def get_param(key, default=''):
    """Get parameter from query string."""
    return unquote(request.args.get(key, default))

def safe_int(value, default):
    """Safely parse integer with fallback."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_float(value, default):
    """Safely parse float with fallback."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def parse_color(color_str):
    """Parse color string (supports hex, rgb, or gradient)."""
    if not color_str:
        return '#409EFF'
    
    # Remove # if present
    color_str = color_str.replace('#', '')
    
    # Check if it's a gradient (comma-separated colors)
    if ',' in color_str:
        colors = [f'#{c.strip()}' if not c.strip().startswith('#') else c.strip() 
                  for c in color_str.split(',')]
        return colors
    
    return f'#{color_str}'

def generate_font_css(font_name, absolute_urls=False):
    """Generate local @font-face CSS for a given font."""
    if font_name not in LOCAL_FONTS:
        return ''
    
    font_files = LOCAL_FONTS[font_name]
    
    # Add cache-busting timestamp to force browser to reload fonts
    cache_buster = int(time.time() * 1000)
    
    # Use absolute URLs if requested (for previews) or relative URLs (for GitHub embeds)
    if absolute_urls:
        base_url = request.url_root.rstrip('/')
        regular_url = f'{base_url}/fonts/{font_files["regular"]}?v={cache_buster}'
        bold_url = f'{base_url}/fonts/{font_files["bold"]}?v={cache_buster}'
    else:
        regular_url = f'/fonts/{font_files["regular"]}?v={cache_buster}'
        bold_url = f'/fonts/{font_files["bold"]}?v={cache_buster}'
    
    font_css = f'''
        @font-face {{
            font-family: '{font_name}';
            src: url('{regular_url}') format('truetype');
            font-weight: 400;
            font-style: normal;
        }}
        @font-face {{
            font-family: '{font_name}';
            src: url('{bold_url}') format('truetype');
            font-weight: 700;
            font-style: normal;
        }}'''
    return font_css

def get_random_char():
    """Get a random character for obfuscation effect."""
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()[]{}?'
    return random.choice(chars)

def parse_obfuscated_text(text):
    """Parse text with ?(text) syntax for obfuscated sections.
    Returns list of tuples: (text_segment, is_obfuscated)
    Example: "Hello ?(World)" -> [("Hello ", False), ("World", True)]
    """
    segments = []
    pattern = r'\?\(([^)]+)\)'
    last_end = 0
    
    for match in re.finditer(pattern, text):
        if match.start() > last_end:
            normal_text = text[last_end:match.start()]
            if normal_text:
                segments.append((normal_text, False))
        
        obfuscated_text = match.group(1)
        segments.append((obfuscated_text, True))
        last_end = match.end()
    
    if last_end < len(text):
        remaining = text[last_end:]
        if remaining:
            segments.append((remaining, False))
    
    if not segments:
        segments.append((text, False))
    
    return segments

def generate_obfuscated_frames(char, num_frames=10):
    """Generate random character frames for obfuscation animation.
    All frames are random - never shows the original character (true Minecraft style)."""
    frames = [get_random_char() for _ in range(num_frames)]
    return frames

def generate_svg(lines, **params):
    """Generate animated SVG based on parameters."""
    
    # Extract parameters with defaults and safe parsing
    animation = params.get('animation', 'typing')
    font = params.get('font', 'Fira Code')
    size = safe_int(params.get('size', 20), 20)
    color = parse_color(params.get('color', '409EFF'))
    bg_color = params.get('bg_color', 'transparent')
    width = safe_int(params.get('width', 600), 600)
    height = safe_int(params.get('height', 100), 100)
    duration = safe_int(params.get('duration', 5000), 5000)
    pause = safe_int(params.get('pause', 1000), 1000)
    repeat = params.get('repeat', 'true').lower() == 'true'
    center = params.get('center', 'true').lower() == 'true'
    # Auto-enable multiline if there are multiple lines
    multiline_param = params.get('multiline', 'auto')
    if multiline_param == 'auto':
        multiline = len(lines) > 1
    else:
        multiline = str(multiline_param).lower() == 'true'
    
    # Glitch-specific parameters
    glitch_intensity = safe_int(params.get('glitch_intensity', 5), 5)
    glitch_speed = safe_float(params.get('glitch_speed', 0.1), 0.1)
    
    # Gradient parameters
    gradient_angle = safe_int(params.get('gradient_angle', 45), 45)
    
    # Letter spacing and stagger
    letter_spacing = safe_int(params.get('letter_spacing', 0), 0)
    stagger_delay = safe_int(params.get('stagger_delay', 50), 50)
    
    # Typing mode (sequential or all)
    typing_mode = params.get('typing_mode', 'sequential')
    
    # Terminal color effect mode
    terminal_color_mode = params.get('terminal_color_mode', 'rainbow')
    terminal_colors = params.get('terminal_colors', 'FF0080,FF8000,FFFF00,00FF00,00FFFF,0080FF,8000FF')
    
    # Border/box styling
    border_width = safe_int(params.get('border_width', 0), 0)
    border_color = params.get('border_color', '000000')
    border_radius = safe_int(params.get('border_radius', 0), 0)
    padding = safe_int(params.get('padding', 0), 0)
    
    # Get preset if exists
    preset = ANIMATION_PRESETS.get(animation, {})
    
    # Build CSS animations based on animation type
    animation_props, keyframes = generate_css_animations(
        animation, duration, pause, repeat, 
        glitch_intensity, glitch_speed, stagger_delay, typing_mode,
        terminal_color_mode, terminal_colors
    )
    
    # Build gradient definition if color is a list
    gradient_def = ''
    fill_color = color
    if isinstance(color, list):
        gradient_def = f'''
        <defs>
            <linearGradient id="textGradient" x1="0%" y1="0%" x2="100%" y2="0%" gradientTransform="rotate({gradient_angle})">
                {generate_gradient_stops(color)}
            </linearGradient>
        </defs>'''
        fill_color = 'url(#textGradient)'
    
    # Calculate text positioning with better spacing
    line_height = size * 1.8
    total_height = len(lines) * line_height if multiline else line_height
    
    # Auto-adjust height if needed for multiline
    if multiline and total_height + 40 > height:
        height = int(total_height + 40)
    
    # Generate text elements
    vCenter = params.get('vCenter', 'false').lower() == 'true'
    text_elements = generate_text_elements(
        lines, animation, fill_color, font, size, 
        center, multiline, line_height, width, height,
        letter_spacing, stagger_delay, typing_mode, duration, vCenter, pause, repeat
    )
    
    # SVG template with border/box support
    xmlns_xlink = 'xmlns:xlink="http://www.w3.org/1999/xlink"' if animation in ['typing', 'terminal'] else ''
    
    # Generate border/box elements if border is enabled
    border_element = ''
    if border_width > 0:
        border_color_hex = f'#{border_color}' if not border_color.startswith('#') else border_color
        border_x = padding
        border_y = padding
        border_w = width - (padding * 2)
        border_h = height - (padding * 2)
        border_element = f'<rect x="{border_x}" y="{border_y}" width="{border_w}" height="{border_h}" fill="none" stroke="{border_color_hex}" stroke-width="{border_width}" rx="{border_radius}" ry="{border_radius}"/>'
    
    # Generate local font CSS with absolute URLs
    font_css = generate_font_css(font, absolute_urls=True)
    
    svg_template = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg" {xmlns_xlink} viewBox="0 0 {width} {height}" style="background-color: {bg_color};">
    <style>
        {font_css}
        
        .svg-text {{
            font-family: '{font}', monospace;
            font-size: {size}px;
            fill: {fill_color if not isinstance(color, list) else 'url(#textGradient)'};
            letter-spacing: {letter_spacing}px;
            {animation_props}
        }}
        
        .obf-char .obf-frame {{
            opacity: 0;
        }}
        
        .obf-char .obf-frame-0 {{ animation: obf-cycle-0 500ms steps(1) infinite; }}
        .obf-char .obf-frame-1 {{ animation: obf-cycle-1 500ms steps(1) infinite; }}
        .obf-char .obf-frame-2 {{ animation: obf-cycle-2 500ms steps(1) infinite; }}
        .obf-char .obf-frame-3 {{ animation: obf-cycle-3 500ms steps(1) infinite; }}
        .obf-char .obf-frame-4 {{ animation: obf-cycle-4 500ms steps(1) infinite; }}
        .obf-char .obf-frame-5 {{ animation: obf-cycle-5 500ms steps(1) infinite; }}
        .obf-char .obf-frame-6 {{ animation: obf-cycle-6 500ms steps(1) infinite; }}
        .obf-char .obf-frame-7 {{ animation: obf-cycle-7 500ms steps(1) infinite; }}
        .obf-char .obf-frame-8 {{ animation: obf-cycle-8 500ms steps(1) infinite; }}
        .obf-char .obf-frame-9 {{ animation: obf-cycle-9 500ms steps(1) infinite; }}
        
        @keyframes obf-cycle-0 {{ 0%, 10% {{ opacity: 1; }} 10.01%, 100% {{ opacity: 0; }} }}
        @keyframes obf-cycle-1 {{ 0%, 9.99% {{ opacity: 0; }} 10%, 20% {{ opacity: 1; }} 20.01%, 100% {{ opacity: 0; }} }}
        @keyframes obf-cycle-2 {{ 0%, 19.99% {{ opacity: 0; }} 20%, 30% {{ opacity: 1; }} 30.01%, 100% {{ opacity: 0; }} }}
        @keyframes obf-cycle-3 {{ 0%, 29.99% {{ opacity: 0; }} 30%, 40% {{ opacity: 1; }} 40.01%, 100% {{ opacity: 0; }} }}
        @keyframes obf-cycle-4 {{ 0%, 39.99% {{ opacity: 0; }} 40%, 50% {{ opacity: 1; }} 50.01%, 100% {{ opacity: 0; }} }}
        @keyframes obf-cycle-5 {{ 0%, 49.99% {{ opacity: 0; }} 50%, 60% {{ opacity: 1; }} 60.01%, 100% {{ opacity: 0; }} }}
        @keyframes obf-cycle-6 {{ 0%, 59.99% {{ opacity: 0; }} 60%, 70% {{ opacity: 1; }} 70.01%, 100% {{ opacity: 0; }} }}
        @keyframes obf-cycle-7 {{ 0%, 69.99% {{ opacity: 0; }} 70%, 80% {{ opacity: 1; }} 80.01%, 100% {{ opacity: 0; }} }}
        @keyframes obf-cycle-8 {{ 0%, 79.99% {{ opacity: 0; }} 80%, 90% {{ opacity: 1; }} 90.01%, 100% {{ opacity: 0; }} }}
        @keyframes obf-cycle-9 {{ 0%, 89.99% {{ opacity: 0; }} 90%, 100% {{ opacity: 1; }} }}
        
        {keyframes}
    </style>
    
    {gradient_def}
    {border_element}
    {text_elements}
</svg>'''
    
    return svg_template

def generate_gradient_stops(colors):
    """Generate SVG gradient stops from color list."""
    stops = []
    step = 100 / (len(colors) - 1) if len(colors) > 1 else 100
    for i, color in enumerate(colors):
        offset = i * step
        stops.append(f'<stop offset="{offset}%" stop-color="{color}" />')
    return '\n                '.join(stops)

def generate_color_keyframes(colors_str, with_shadow=False):
    """Generate color animation keyframes from comma-separated color list."""
    colors = [c.strip() for c in colors_str.split(',')]
    if len(colors) == 0:
        colors = ['FF0080']
    
    keyframes = []
    step = 100 / len(colors) if len(colors) > 0 else 100
    
    for i, color in enumerate(colors):
        color_hex = f'#{color}' if not color.startswith('#') else color
        percent = int(i * step)
        if with_shadow:
            keyframes.append(f'{percent}% {{ fill: {color_hex}; filter: drop-shadow(0 0 10px {color_hex}); }}')
        else:
            keyframes.append(f'{percent}% {{ fill: {color_hex}; }}')
    
    # Add 100% wrapping back to first color
    first_color = f'#{colors[0]}' if not colors[0].startswith('#') else colors[0]
    if with_shadow:
        keyframes.append(f'100% {{ fill: {first_color}; filter: drop-shadow(0 0 10px {first_color}); }}')
    else:
        keyframes.append(f'100% {{ fill: {first_color}; }}')
    
    return '\n            '.join(keyframes)

def generate_css_animations(animation, duration, pause, repeat, glitch_intensity, glitch_speed, stagger_delay, typing_mode='sequential', terminal_color_mode='rainbow', terminal_colors='FF0080,FF8000,FFFF00,00FF00,00FFFF,0080FF,8000FF'):
    """Generate CSS animations based on animation type.
    Returns: (animation_properties, keyframes)
    """
    
    repeat_count = 'infinite' if repeat else '1'
    
    # Calculate total cycle time and active percentage
    total_duration = duration + pause
    active_percent = (duration / total_duration * 100) if pause > 0 else 100
    
    # Calculate flicker iterations for fire animation
    import math
    flicker_duration = 150  # milliseconds
    flicker_iterations = 'infinite' if repeat else str(max(1, math.ceil(total_duration / flicker_duration)))
    
    # For sequential mode - calculate full cycle time for all lines
    num_lines = 5  # Support up to 5 lines
    type_time = duration  # Time to type one line
    delete_time = duration // 2  # Time to delete (faster)
    line_cycle = type_time + pause + delete_time  # Full cycle for one line
    total_cycle = line_cycle * num_lines
    
    # Set animation delays based on typing mode
    if typing_mode == 'sequential':
        # Sequential: each line types and deletes before next one starts
        line_animations = []
        for i in range(num_lines):
            delay = i * line_cycle
            # Calculate visibility windows as percentages of total cycle
            type_start = (delay / total_cycle) * 100
            type_end = ((delay + type_time) / total_cycle) * 100
            pause_end = ((delay + type_time + pause) / total_cycle) * 100
            delete_end = ((delay + line_cycle) / total_cycle) * 100
            
            line_animations.append(f'''
        .svg-text.line-{i} {{
            animation: typeLine{i} {total_cycle}ms steps(60) {repeat_count};
        }}
        
        @keyframes typeLine{i} {{
            0%, {type_start}% {{ clip-path: inset(0 100% 0 0); opacity: 1; }}
            {type_end}% {{ clip-path: inset(0 0% 0 0); opacity: 1; }}
            {pause_end}% {{ clip-path: inset(0 0% 0 0); opacity: 1; }}
            {delete_end}%, 100% {{ clip-path: inset(0 100% 0 0); opacity: 1; }}
        }}''')
        
        typing_css = '\n'.join(line_animations)
    else:  # 'all' mode - all lines type at once
        typing_css = f'''
        .svg-text {{
            clip-path: inset(0 100% 0 0);
            animation: typeReveal {duration}ms steps(60) {repeat_count};
        }}
        
        @keyframes typeReveal {{
            0% {{ clip-path: inset(0 100% 0 0); }}
            {active_percent}% {{ clip-path: inset(0 0% 0 0); }}
            100% {{ clip-path: inset(0 0% 0 0); }}
        }}'''
    
    # Typewriter animation with proper repeat
    typewriter_css = f'''
        .svg-text {{
            clip-path: inset(0 100% 0 0);
            animation: typewriter {total_duration}ms steps(40) {repeat_count};
        }}
        
        @keyframes typewriter {{
            0% {{ 
                clip-path: inset(0 100% 0 0); 
            }}
            {active_percent * 0.45}% {{ 
                clip-path: inset(0 0% 0 0); 
            }}
            {active_percent * 0.55}% {{ 
                clip-path: inset(0 0% 0 0); 
            }}
            100% {{ 
                clip-path: inset(0 100% 0 0); 
            }}
        }}
        
        .cursor {{
            animation: cursorBlink 0.5s step-end infinite;
        }}
        
        @keyframes cursorBlink {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0; }}
        }}'''
    
    animations = {
        'typewriter': typewriter_css,
        
        'typing': f'''
        {typing_css}
        
        .typing-cursor {{
            animation: cursorBlink 0.7s step-end infinite;
            opacity: 0.8;
            font-weight: 300;
        }}
        
        @keyframes cursorBlink {{
            0%, 100% {{ opacity: 0.8; }}
            50% {{ opacity: 0; }}
        }}
        ''',
        
        'wave': f'''
        .svg-text .char {{
            animation: wave {total_duration}ms ease-in-out infinite;
            animation-delay: calc(var(--char-index) * {stagger_delay}ms);
            transform-origin: center bottom;
        }}
        
        @keyframes wave {{
            0%, 100% {{ 
                transform: translateY(0) rotate(0deg);
            }}
            25% {{ 
                transform: translateY(-12px) rotate(-3deg);
            }}
            50% {{ 
                transform: translateY(-18px) rotate(0deg);
            }}
            75% {{ 
                transform: translateY(-12px) rotate(3deg);
            }}
        }}
        ''',
        
        'glitch': f'''
        .svg-text {{
            animation: glitch {total_duration}ms ease-in-out {repeat_count};
        }}
        
        @keyframes glitch {{
            0%, 100% {{ 
                transform: translate(0);
                opacity: 1;
            }}
            25% {{ 
                transform: translate(-{glitch_intensity//2}px, 0);
                opacity: 0.8;
            }}
            75% {{ 
                transform: translate({glitch_intensity//2}px, 0);
                opacity: 0.8;
            }}
        }}
        ''',
        
        
        'fade': f'''
        .svg-text .char {{
            opacity: 0;
            animation: fadeIn {total_duration}ms cubic-bezier(0.16, 1, 0.3, 1) {repeat_count};
            animation-delay: calc(var(--char-index) * {stagger_delay}ms);
            animation-fill-mode: forwards;
        }}
        
        @keyframes fadeIn {{
            0% {{ opacity: 0; transform: translateY(10px); }}
            100% {{ opacity: 1; transform: translateY(0); }}
        }}
        ''',
        
        'stroke': f'''
        .svg-text {{
            fill: transparent;
            stroke: currentColor;
            stroke-width: 1;
            stroke-dasharray: 1000;
            stroke-dashoffset: 1000;
            animation: strokeDraw {total_duration}ms ease-out {repeat_count};
            animation-fill-mode: forwards;
        }}
        
        @keyframes strokeDraw {{
            0% {{
                stroke-dashoffset: 1000;
            }}
            {active_percent}%, 100% {{
                stroke-dashoffset: 0;
                fill: currentColor;
            }}
        }}
        ''',
        
        'matrix': f'''
        .svg-text .char {{
            opacity: 0;
            animation: matrixRain {total_duration}ms linear {repeat_count};
            animation-delay: calc(var(--char-index) * 100ms);
        }}
        
        @keyframes matrixRain {{
            0% {{ opacity: 0; transform: translateY(-50px); }}
            {active_percent*0.1}% {{ opacity: 1; }}
            {active_percent*0.9}% {{ opacity: 1; }}
            {active_percent}% {{ opacity: 0; transform: translateY(50px); }}
            100% {{ opacity: 0; transform: translateY(50px); }}
        }}
        ''',
        
        
        'terminal': f'''
        .svg-text {{
            filter: drop-shadow(0 0 5px currentColor) drop-shadow(0 0 10px currentColor);
            {f"animation: rainbowText 3s linear infinite;" if terminal_color_mode == 'rainbow' else ""}
        }}
        
        .svg-text .char {{
            display: inline-block;
            animation: minecraftScramble {max(80, duration//12)}ms steps(8) forwards,
                       {f"charRainbow 2s linear infinite," if terminal_color_mode in ['rainbow', 'custom'] else ""}
                       microGlitch 100ms ease-in-out infinite;
            animation-delay: calc(var(--char-index) * {max(40, duration//50)}ms),
                            {f"calc(var(--char-index) * 0.1s)," if terminal_color_mode in ['rainbow', 'custom'] else ""}
                            0s;
            opacity: 0;
        }}
        
        @keyframes minecraftScramble {{
            0% {{ 
                opacity: 0.2;
                filter: blur(10px) brightness(2) hue-rotate(180deg) saturate(3);
                transform: translateX(-5px) translateY(-3px) scale(1.5) rotate(-15deg) skewX(-20deg);
            }}
            8% {{ 
                opacity: 0.3;
                filter: blur(9px) brightness(1.9) hue-rotate(160deg) saturate(2.8);
                transform: translateX(4px) translateY(2px) scale(0.7) rotate(12deg) skewX(15deg);
            }}
            16% {{ 
                opacity: 0.4;
                filter: blur(8px) brightness(1.8) hue-rotate(140deg) saturate(2.6);
                transform: translateX(-3px) translateY(-2px) scale(1.3) rotate(-10deg) skewX(-12deg);
            }}
            24% {{ 
                opacity: 0.5;
                filter: blur(7px) brightness(1.7) hue-rotate(120deg) saturate(2.4);
                transform: translateX(5px) translateY(1px) scale(0.8) rotate(8deg) skewX(10deg);
            }}
            32% {{ 
                opacity: 0.6;
                filter: blur(6px) brightness(1.6) hue-rotate(100deg) saturate(2.2);
                transform: translateX(-4px) translateY(-1px) scale(1.2) rotate(-6deg) skewX(-8deg);
            }}
            40% {{ 
                opacity: 0.7;
                filter: blur(5px) brightness(1.5) hue-rotate(80deg) saturate(2);
                transform: translateX(3px) translateY(2px) scale(0.9) rotate(5deg) skewX(6deg);
            }}
            48% {{ 
                opacity: 0.75;
                filter: blur(4px) brightness(1.4) hue-rotate(60deg) saturate(1.8);
                transform: translateX(-2px) translateY(-1px) scale(1.1) rotate(-4deg) skewX(-5deg);
            }}
            56% {{ 
                opacity: 0.8;
                filter: blur(3px) brightness(1.3) hue-rotate(45deg) saturate(1.6);
                transform: translateX(2px) translateY(1px) scale(0.95) rotate(3deg) skewX(4deg);
            }}
            64% {{ 
                opacity: 0.85;
                filter: blur(2.5px) brightness(1.25) hue-rotate(30deg) saturate(1.4);
                transform: translateX(-1px) translateY(0) scale(1.05) rotate(-2deg) skewX(-3deg);
            }}
            72% {{ 
                opacity: 0.9;
                filter: blur(2px) brightness(1.2) hue-rotate(20deg) saturate(1.3);
                transform: translateX(1px) translateY(-1px) scale(0.98) rotate(2deg) skewX(2deg);
            }}
            80% {{ 
                opacity: 0.93;
                filter: blur(1.5px) brightness(1.15) hue-rotate(10deg) saturate(1.2);
                transform: translateX(-0.5px) translateY(0.5px) scale(1.02) rotate(-1deg) skewX(-1deg);
            }}
            88% {{ 
                opacity: 0.96;
                filter: blur(1px) brightness(1.08) hue-rotate(5deg) saturate(1.1);
                transform: translateX(0.3px) translateY(-0.3px) scale(0.99) rotate(0.5deg) skewX(0.5deg);
            }}
            96% {{ 
                opacity: 0.99;
                filter: blur(0.3px) brightness(1.02) hue-rotate(1deg) saturate(1.05);
                transform: translateX(0) translateY(0) scale(1.01) rotate(0) skewX(0);
            }}
            100% {{ 
                opacity: 1;
                filter: blur(0) brightness(1) hue-rotate(0deg) saturate(1);
                transform: translateX(0) translateY(0) scale(1) rotate(0) skewX(0);
            }}
        }}
        
        @keyframes rainbowText {{
            0% {{ filter: hue-rotate(0deg) drop-shadow(0 0 5px currentColor); }}
            14% {{ filter: hue-rotate(51deg) drop-shadow(0 0 8px currentColor); }}
            28% {{ filter: hue-rotate(102deg) drop-shadow(0 0 6px currentColor); }}
            42% {{ filter: hue-rotate(153deg) drop-shadow(0 0 8px currentColor); }}
            57% {{ filter: hue-rotate(204deg) drop-shadow(0 0 7px currentColor); }}
            71% {{ filter: hue-rotate(255deg) drop-shadow(0 0 8px currentColor); }}
            85% {{ filter: hue-rotate(306deg) drop-shadow(0 0 6px currentColor); }}
            100% {{ filter: hue-rotate(360deg) drop-shadow(0 0 5px currentColor); }}
        }}
        
        @keyframes charRainbow {{
            {generate_color_keyframes(terminal_colors)}
        }}
        
        @keyframes microGlitch {{
            0%, 100% {{
                transform: translateX(0);
            }}
            33% {{
                transform: translateX(0.5px);
            }}
            66% {{
                transform: translateX(-0.5px);
            }}
        }}
        
        .cursor {{
            display: inline-block;
            animation: blink 0.7s step-end infinite{f", charRainbow 2s linear infinite" if terminal_color_mode in ['rainbow', 'custom'] else ""};
            font-weight: normal;
        }}
        
        @keyframes blink {{
            0%, 49% {{ opacity: 1; }}
            50%, 100% {{ opacity: 0; }}
        }}
        
        @keyframes cursorRainbow {{
            {generate_color_keyframes(terminal_colors, with_shadow=True)}
        }}
        
        @keyframes cursorPulse {{
            0%, 100% {{ 
                transform: scaleY(1);
                opacity: 1;
            }}
            50% {{ 
                transform: scaleY(1.2);
                opacity: 0.8;
            }}
        }}
        ''',
        
        'pulse': f'''
        .svg-text {{
            animation: pulse {total_duration}ms ease-in-out {repeat_count};
        }}
        
        @keyframes pulse {{
            0%, 100% {{ 
                transform: scale(1);
                opacity: 1;
            }}
            50% {{ 
                transform: scale(1.05);
                opacity: 0.9;
            }}
        }}
        ''',
        
        'zoom': f'''
        .svg-text {{
            opacity: 0;
            animation: zoom {total_duration}ms cubic-bezier(0.16, 1, 0.3, 1) {repeat_count};
            animation-fill-mode: forwards;
        }}
        
        @keyframes zoom {{
            0% {{ 
                transform: scale(0.5);
                opacity: 0;
            }}
            100% {{ 
                transform: scale(1);
                opacity: 1;
            }}
        }}
        ''',
        
        
        'flip': f'''
        .svg-text {{
            animation: flip {total_duration}ms ease-in-out {repeat_count};
            transform-origin: center;
        }}
        
        @keyframes flip {{
            0%, 100% {{ 
                transform: rotateY(0deg);
            }}
            50% {{ 
                transform: rotateY(180deg);
            }}
        }}
        ''',
        
        'slide': f'''
        .svg-text {{
            animation: slide {total_duration}ms cubic-bezier(0.16, 1, 0.3, 1) {repeat_count};
            animation-fill-mode: forwards;
            opacity: 0;
        }}
        
        @keyframes slide {{
            0% {{ 
                transform: translateX(-30px);
                opacity: 0;
            }}
            100% {{ 
                transform: translateX(0);
                opacity: 1;
            }}
        }}
        ''',
        
        'bounce': f'''
        .svg-text {{
            animation: bounce {total_duration}ms cubic-bezier(0.34, 1.56, 0.64, 1) {repeat_count};
        }}
        
        @keyframes bounce {{
            0%, {active_percent}%, 100% {{ 
                transform: translateY(0) scale(1);
            }}
            {active_percent*0.2}% {{ 
                transform: translateY(-30px) scale(1.1, 0.9);
            }}
            {active_percent*0.4}% {{ 
                transform: translateY(0) scale(0.95, 1.05);
            }}
            {active_percent*0.5}% {{ 
                transform: translateY(-15px) scale(1.05, 0.95);
            }}
            {active_percent*0.65}% {{ 
                transform: translateY(0) scale(0.98, 1.02);
            }}
            {active_percent*0.8}% {{ 
                transform: translateY(-7px) scale(1.02, 0.98);
            }}
        }}
        ''',
        
        'glitch-heavy': f'''
        .svg-text {{
            animation: glitchHeavy {total_duration}ms steps(3) {repeat_count};
            filter: contrast(1.2) brightness(1.1);
        }}
        
        @keyframes glitchHeavy {{
            0%, 100% {{ 
                transform: translate(0) skew(0deg);
                filter: hue-rotate(0deg) contrast(1.2);
            }}
            10% {{ 
                transform: translate(-{glitch_intensity}px, {glitch_intensity//2}px) skew(-5deg);
                filter: hue-rotate(90deg) contrast(1.5);
            }}
            20% {{ 
                transform: translate({glitch_intensity}px, -{glitch_intensity//2}px) skew(5deg);
                filter: hue-rotate(180deg) contrast(1.8);
            }}
            30% {{ 
                transform: translate(-{glitch_intensity//2}px, {glitch_intensity}px) skew(-3deg);
                filter: hue-rotate(270deg) contrast(1.3);
            }}
            40% {{ 
                transform: translate({glitch_intensity//2}px, -{glitch_intensity}px) skew(3deg);
                filter: hue-rotate(45deg) contrast(1.6);
            }}
            50% {{ 
                transform: translate(-{glitch_intensity*1.5}px, 0) skew(-7deg);
                filter: hue-rotate(135deg) contrast(2);
            }}
            60% {{ 
                transform: translate({glitch_intensity*1.5}px, 0) skew(7deg);
                filter: hue-rotate(225deg) contrast(1.4);
            }}
        }}
        ''',
        
        'glitch-scan': f'''
        .svg-text {{
            animation: glitchScan {total_duration}ms linear {repeat_count};
            position: relative;
        }}
        
        @keyframes glitchScan {{
            0%, 100% {{ 
                transform: translate(0);
                filter: hue-rotate(0deg);
                clip-path: inset(0 0 0 0);
            }}
            10% {{ 
                transform: translate(-2px, 0);
                filter: hue-rotate(30deg);
                clip-path: inset(0 0 80% 0);
            }}
            20% {{ 
                transform: translate(2px, 0);
                filter: hue-rotate(60deg);
                clip-path: inset(0 0 60% 0);
            }}
            30% {{ 
                transform: translate(-1px, 0);
                filter: hue-rotate(90deg);
                clip-path: inset(0 0 40% 0);
            }}
            40% {{ 
                transform: translate(1px, 0);
                filter: hue-rotate(120deg);
                clip-path: inset(0 0 20% 0);
            }}
            50% {{ 
                transform: translate(0);
                filter: hue-rotate(180deg);
                clip-path: inset(0 0 0 0);
            }}
            60% {{ 
                transform: translate(-2px, 0);
                filter: hue-rotate(210deg);
                clip-path: inset(20% 0 0 0);
            }}
            70% {{ 
                transform: translate(2px, 0);
                filter: hue-rotate(240deg);
                clip-path: inset(40% 0 0 0);
            }}
            80% {{ 
                transform: translate(-1px, 0);
                filter: hue-rotate(270deg);
                clip-path: inset(60% 0 0 0);
            }}
            90% {{ 
                transform: translate(1px, 0);
                filter: hue-rotate(300deg);
                clip-path: inset(80% 0 0 0);
            }}
        }}
        ''',
        
        'corrupt': f'''
        .svg-text .char {{
            animation: corrupt {total_duration}ms steps(5) {repeat_count};
            animation-delay: calc(var(--char-index) * 30ms);
        }}
        
        @keyframes corrupt {{
            0%, 100% {{ 
                transform: translate(0) rotate(0deg) scale(1);
                opacity: 1;
            }}
            20% {{ 
                transform: translate(-{glitch_intensity}px, {glitch_intensity}px) rotate(-15deg) scale(0.8);
                opacity: 0.7;
            }}
            40% {{ 
                transform: translate({glitch_intensity}px, -{glitch_intensity}px) rotate(15deg) scale(1.2);
                opacity: 0.5;
            }}
            60% {{ 
                transform: translate(-{glitch_intensity//2}px, -{glitch_intensity//2}px) rotate(-30deg) scale(0.9);
                opacity: 0.8;
            }}
            80% {{ 
                transform: translate({glitch_intensity//2}px, {glitch_intensity//2}px) rotate(20deg) scale(1.1);
                opacity: 0.6;
            }}
        }}
        ''',
        
        'static': f'''
        .svg-text {{
            animation: staticNoise {total_duration}ms steps(20) {repeat_count};
        }}
        
        @keyframes staticNoise {{
            0%, 100% {{ 
                transform: translate(0);
                filter: contrast(1);
                opacity: 1;
            }}
            5% {{ 
                transform: translate(-1px, 1px);
                filter: contrast(1.5) brightness(0.8);
                opacity: 0.9;
            }}
            10% {{ 
                transform: translate(1px, -1px);
                filter: contrast(0.8) brightness(1.2);
                opacity: 0.95;
            }}
            15% {{ 
                transform: translate(-2px, 0);
                filter: contrast(1.3) brightness(0.9);
                opacity: 0.85;
            }}
            20% {{ 
                transform: translate(2px, 1px);
                filter: contrast(0.9) brightness(1.1);
                opacity: 0.9;
            }}
            25% {{ 
                transform: translate(0, -2px);
                filter: contrast(1.4) brightness(0.85);
                opacity: 0.88;
            }}
            30% {{ 
                transform: translate(-1px, -1px);
                filter: contrast(1.1) brightness(1);
                opacity: 0.92;
            }}
        }}
        ''',
        
        'shake': f'''
        .svg-text {{
            animation: shake {total_duration}ms ease-in-out {repeat_count};
        }}
        
        @keyframes shake {{
            0%, 100% {{ transform: translate(0, 0) rotate(0deg); }}
            10% {{ transform: translate(-2px, -1px) rotate(-1deg); }}
            20% {{ transform: translate(2px, 1px) rotate(1deg); }}
            30% {{ transform: translate(-2px, 1px) rotate(-1deg); }}
            40% {{ transform: translate(2px, -1px) rotate(1deg); }}
            50% {{ transform: translate(-2px, -1px) rotate(-1deg); }}
            60% {{ transform: translate(2px, 1px) rotate(1deg); }}
            70% {{ transform: translate(-2px, 1px) rotate(-1deg); }}
            80% {{ transform: translate(2px, -1px) rotate(1deg); }}
            90% {{ transform: translate(-1px, 0) rotate(-0.5deg); }}
        }}
        ''',
        
        'neon': f'''
        .svg-text {{
            animation: neon {total_duration}ms ease-in-out {repeat_count};
            filter: drop-shadow(0 0 5px currentColor) drop-shadow(0 0 10px currentColor);
        }}
        
        @keyframes neon {{
            0%, 100% {{ 
                filter: drop-shadow(0 0 5px currentColor) drop-shadow(0 0 10px currentColor);
                opacity: 1;
            }}
            10% {{ 
                filter: drop-shadow(0 0 2px currentColor) drop-shadow(0 0 5px currentColor);
                opacity: 0.8;
            }}
            15% {{ 
                filter: drop-shadow(0 0 15px currentColor) drop-shadow(0 0 25px currentColor);
                opacity: 1;
            }}
            20% {{ 
                filter: drop-shadow(0 0 3px currentColor) drop-shadow(0 0 8px currentColor);
                opacity: 0.85;
            }}
            25% {{ 
                filter: drop-shadow(0 0 20px currentColor) drop-shadow(0 0 35px currentColor);
                opacity: 1;
            }}
            50% {{ 
                filter: drop-shadow(0 0 10px currentColor) drop-shadow(0 0 20px currentColor);
                opacity: 1;
            }}
            75% {{ 
                filter: drop-shadow(0 0 5px currentColor) drop-shadow(0 0 12px currentColor);
                opacity: 0.9;
            }}
        }}
        ''',
        
        'rainbow': f'''
        .svg-text {{
            animation: rainbow {total_duration}ms linear {repeat_count};
        }}
        
        @keyframes rainbow {{
            0% {{ filter: hue-rotate(0deg) drop-shadow(0 0 8px currentColor); }}
            14% {{ filter: hue-rotate(51deg) drop-shadow(0 0 10px currentColor); }}
            28% {{ filter: hue-rotate(102deg) drop-shadow(0 0 8px currentColor); }}
            42% {{ filter: hue-rotate(153deg) drop-shadow(0 0 10px currentColor); }}
            57% {{ filter: hue-rotate(204deg) drop-shadow(0 0 8px currentColor); }}
            71% {{ filter: hue-rotate(255deg) drop-shadow(0 0 10px currentColor); }}
            85% {{ filter: hue-rotate(306deg) drop-shadow(0 0 8px currentColor); }}
            100% {{ filter: hue-rotate(360deg) drop-shadow(0 0 10px currentColor); }}
        }}
        ''',
        
        'sparkle': f'''
        .svg-text .char {{
            animation: sparkle {total_duration}ms ease-in-out {repeat_count};
            animation-delay: calc(var(--char-index) * {stagger_delay}ms);
        }}
        
        @keyframes sparkle {{
            0%, 100% {{ 
                filter: brightness(1) drop-shadow(0 0 0 currentColor);
                transform: scale(1);
            }}
            25% {{ 
                filter: brightness(1.5) drop-shadow(0 0 8px currentColor);
                transform: scale(1.1);
            }}
            50% {{ 
                filter: brightness(2) drop-shadow(0 0 15px currentColor);
                transform: scale(1.15);
            }}
            75% {{ 
                filter: brightness(1.3) drop-shadow(0 0 6px currentColor);
                transform: scale(1.05);
            }}
        }}
        ''',
        
        'fire': f'''
        .svg-text .char {{
            animation: fire {total_duration}ms ease-in-out {repeat_count}, fireFlicker 150ms ease-in-out {flicker_iterations};
            animation-delay: calc(var(--char-index) * {stagger_delay//2}ms), calc(var(--char-index) * 30ms);
            filter: drop-shadow(0 0 20px rgba(255,100,0,0.9)) drop-shadow(0 0 40px rgba(255,60,0,0.6)) drop-shadow(0 0 60px rgba(255,140,0,0.4));
            transform-origin: center bottom;
        }}
        
        @keyframes fire {{
            0% {{ 
                transform: translateY(0) scale(1, 1) rotate(0deg);
                filter: drop-shadow(0 0 20px rgba(255,100,0,0.9)) drop-shadow(0 0 40px rgba(255,60,0,0.6)) drop-shadow(0 0 60px rgba(255,140,0,0.4)) brightness(1.2);
                fill: #FF4500;
                opacity: 1;
            }}
            10% {{ 
                transform: translateY(-4px) scale(1.03, 1.08) rotate(-2deg);
                filter: drop-shadow(0 0 25px rgba(255,120,0,1)) drop-shadow(0 0 50px rgba(255,80,0,0.7)) drop-shadow(0 0 70px rgba(255,160,0,0.5)) brightness(1.4);
                fill: #FF5500;
                opacity: 0.98;
            }}
            20% {{ 
                transform: translateY(-8px) scale(1.05, 1.15) rotate(1deg);
                filter: drop-shadow(0 0 30px rgba(255,150,0,1)) drop-shadow(0 0 60px rgba(255,100,0,0.8)) drop-shadow(0 0 80px rgba(255,180,0,0.6)) brightness(1.6);
                fill: #FF6600;
                opacity: 0.95;
            }}
            30% {{ 
                transform: translateY(-12px) scale(1.04, 1.2) rotate(-1deg);
                filter: drop-shadow(0 0 35px rgba(255,180,0,1)) drop-shadow(0 0 70px rgba(255,120,0,0.8)) drop-shadow(0 0 90px rgba(255,200,0,0.6)) brightness(1.8);
                fill: #FF7700;
                opacity: 0.93;
            }}
            40% {{ 
                transform: translateY(-15px) scale(1.02, 1.25) rotate(2deg);
                filter: drop-shadow(0 0 40px rgba(255,200,0,1)) drop-shadow(0 0 80px rgba(255,150,0,0.9)) drop-shadow(0 0 100px rgba(255,220,0,0.7)) brightness(2);
                fill: #FF8800;
                opacity: 0.9;
            }}
            50% {{ 
                transform: translateY(-18px) scale(1, 1.3) rotate(0deg);
                filter: drop-shadow(0 0 45px rgba(255,220,100,1)) drop-shadow(0 0 90px rgba(255,180,0,1)) drop-shadow(0 0 110px rgba(255,240,100,0.8)) brightness(2.2);
                fill: #FFAA00;
                opacity: 0.85;
            }}
            60% {{ 
                transform: translateY(-15px) scale(1.02, 1.25) rotate(-2deg);
                filter: drop-shadow(0 0 40px rgba(255,200,0,1)) drop-shadow(0 0 80px rgba(255,150,0,0.9)) drop-shadow(0 0 100px rgba(255,220,0,0.7)) brightness(2);
                fill: #FF9900;
                opacity: 0.88;
            }}
            70% {{ 
                transform: translateY(-11px) scale(1.04, 1.18) rotate(1deg);
                filter: drop-shadow(0 0 35px rgba(255,170,0,1)) drop-shadow(0 0 70px rgba(255,130,0,0.8)) drop-shadow(0 0 90px rgba(255,200,0,0.6)) brightness(1.7);
                fill: #FF7700;
                opacity: 0.92;
            }}
            80% {{ 
                transform: translateY(-7px) scale(1.05, 1.12) rotate(-1deg);
                filter: drop-shadow(0 0 30px rgba(255,140,0,1)) drop-shadow(0 0 60px rgba(255,100,0,0.8)) drop-shadow(0 0 80px rgba(255,180,0,0.6)) brightness(1.5);
                fill: #FF6600;
                opacity: 0.95;
            }}
            90% {{ 
                transform: translateY(-3px) scale(1.02, 1.06) rotate(1deg);
                filter: drop-shadow(0 0 25px rgba(255,110,0,0.9)) drop-shadow(0 0 50px rgba(255,70,0,0.7)) drop-shadow(0 0 70px rgba(255,150,0,0.5)) brightness(1.3);
                fill: #FF5500;
                opacity: 0.97;
            }}
            100% {{ 
                transform: translateY(0) scale(1, 1) rotate(0deg);
                filter: drop-shadow(0 0 20px rgba(255,100,0,0.9)) drop-shadow(0 0 40px rgba(255,60,0,0.6)) drop-shadow(0 0 60px rgba(255,140,0,0.4)) brightness(1.2);
                fill: #FF4500;
                opacity: 1;
            }}
        }}
        
        @keyframes fireFlicker {{
            0%, 100% {{ 
                opacity: 1;
            }}
            25% {{ 
                opacity: 0.95;
            }}
            50% {{ 
                opacity: 0.92;
            }}
            75% {{ 
                opacity: 0.97;
            }}
        }}
        ''',
        
        'rotate3d': f'''
        .svg-text {{
            animation: rotate3d {total_duration}ms ease-in-out {repeat_count};
            transform-origin: center;
            transform-style: preserve-3d;
        }}
        
        @keyframes rotate3d {{
            0% {{ 
                transform: rotate3d(1, 1, 0, 0deg);
            }}
            25% {{ 
                transform: rotate3d(1, 1, 0, 90deg);
            }}
            50% {{ 
                transform: rotate3d(1, 1, 0, 180deg);
            }}
            75% {{ 
                transform: rotate3d(1, 1, 0, 270deg);
            }}
            100% {{ 
                transform: rotate3d(1, 1, 0, 360deg);
            }}
        }}
        ''',
        
        'gradient-shift': f'''
        .svg-text {{
            animation: gradientShift {total_duration}ms linear {repeat_count};
        }}
        
        @keyframes gradientShift {{
            0% {{ 
                filter: hue-rotate(0deg) saturate(1);
            }}
            20% {{ 
                filter: hue-rotate(72deg) saturate(1.3);
            }}
            40% {{ 
                filter: hue-rotate(144deg) saturate(1.5);
            }}
            60% {{ 
                filter: hue-rotate(216deg) saturate(1.3);
            }}
            80% {{ 
                filter: hue-rotate(288deg) saturate(1.1);
            }}
            100% {{ 
                filter: hue-rotate(360deg) saturate(1);
            }}
        }}
        ''',
        
        'blur-focus': f'''
        .svg-text {{
            animation: blurFocus {total_duration}ms ease-in-out {repeat_count};
        }}
        
        @keyframes blurFocus {{
            0% {{ 
                filter: blur(8px);
                opacity: 0.3;
            }}
            {active_percent}% {{ 
                filter: blur(0px);
                opacity: 1;
            }}
            100% {{ 
                filter: blur(0px);
                opacity: 1;
            }}
        }}
        ''',
        
    }
    
    # Parse the CSS block to extract properties and keyframes
    css_block = animations.get(animation, animations['typing'])
    
    # Split into properties and keyframes
    import re
    
    # Extract all @keyframes
    keyframes_list = re.findall(r'@keyframes[^{]+\{(?:[^{}]|\{[^}]*\})*\}', css_block, re.DOTALL)
    
    # Extract all CSS class selectors (like .cursor, .typing-cursor, etc.) that are not .svg-text
    # This preserves important helper classes
    other_classes = re.findall(r'\.[a-zA-Z][a-zA-Z0-9_-]*(?:\s+\.[a-zA-Z][a-zA-Z0-9_-]*)*\s*\{[^}]+\}', css_block, re.DOTALL)
    # Filter out .svg-text and .svg-text .char since we handle those separately
    other_classes = [cls for cls in other_classes if not cls.strip().startswith('.svg-text')]
    
    # Check if this is a character-level animation
    char_match = re.search(r'\.svg-text\s+\.char\s*\{([^}]+)\}', css_block, re.DOTALL)
    svg_text_match = re.search(r'\.svg-text\s*\{([^}]+)\}', css_block, re.DOTALL)
    
    # Build the keyframes section with all components
    all_keyframes_parts = []
    
    # Add other CSS classes first (like .cursor, .typing-cursor, etc.)
    if other_classes:
        all_keyframes_parts.extend(other_classes)
    
    # Add @keyframes
    if keyframes_list:
        all_keyframes_parts.extend(keyframes_list)
    
    # Get animation properties
    if char_match:
        # For character-level animations, add the .char selector to keyframes
        animation_props = ''
        char_styles = f'''.svg-text .char {{
            {char_match.group(1).strip()}
        }}'''
        all_keyframes_parts.insert(0, char_styles)
    elif svg_text_match:
        animation_props = svg_text_match.group(1).strip()
    else:
        animation_props = ''
    
    keyframes = '\n\n'.join(all_keyframes_parts)
    
    return (animation_props, keyframes)

def generate_typing_svg_elements(lines, fill_color, font, size, center, width, height, duration, pause, repeat, vCenter=False, letter_spacing=0, animation_type='typing'):
    """Generate SVG elements using textPath animation like readme-typing-svg."""
    elements = []
    last_line_index = len(lines) - 1
    
    for i, line in enumerate(lines):
        escaped_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        # Terminal: Use CSS character animation instead of SMIL
        if animation_type == 'terminal':
            # Skip SMIL animation for terminal, will use CSS instead
            path_element = ''
            cursor_element = ''
        else:
            # Typing animation: type and delete
            # Calculate animation timing
            if i == 0:
                begin = "0s" if not repeat else f"0s;d{last_line_index}.end"
            else:
                begin = f"d{i-1}.end"
            
            # Don't delete text after typing the last line if repeat is false
            freeze = not repeat and i == last_line_index
            
            # Path coordinates
            y_offset = height / 2
            empty_line = f"m0,{y_offset} h0"
            full_line = f"m0,{y_offset} h{width}"
            
            # Animation values: empty -> full (typing) -> hold (pause) -> empty (delete)
            values = [empty_line, full_line, full_line, full_line if freeze else empty_line]
            
            # KeyTimes: 0% -> 80% type -> 80-100% pause/delete
            total_dur = duration + pause
            key_times = [
                0,
                (0.8 * duration) / total_dur,
                (0.8 * duration + pause) / total_dur,
                1
            ]
            key_times_str = ';'.join([str(k) for k in key_times])
            values_str = ' ; '.join(values)
            
            # Create path with animate element
            path_element = f'''<path id="path{i}">
        <animate id="d{i}" attributeName="d" begin="{begin}"
            dur="{total_dur}ms" fill="{'freeze' if freeze else 'remove'}"
            values="{values_str}" keyTimes="{key_times_str}" />
    </path>'''
            cursor_element = ''
        
        # Create text element with textPath
        text_x = "50%" if center else "0%"
        text_anchor = "middle" if center else "start"
        dominant_baseline = "middle" if vCenter else "auto"
        
        text_element = f'''<text font-family="'{font}', monospace" fill="{fill_color}" font-size="{size}"
        dominant-baseline="{dominant_baseline}"
        x="{text_x}" text-anchor="{text_anchor}"
        letter-spacing="{letter_spacing}px">
        <textPath xlink:href="#path{i}">
            {escaped_line}
        </textPath>
    </text>'''
        
        elements.append(path_element)
        elements.append(text_element)
        if cursor_element:
            elements.append(cursor_element)
    
    return '\n    '.join(elements)

def generate_text_elements(lines, animation, fill_color, font, size, center, multiline, line_height, width, height, letter_spacing, stagger_delay, typing_mode='sequential', duration=3000, vCenter=False, pause=1000, repeat=True):
    """Generate SVG text elements."""
    
    # Use SMIL animation for typing only
    if animation in ['typing']:
        return generate_typing_svg_elements(lines, fill_color, font, size, center, width, height, duration, pause, repeat, vCenter, letter_spacing, animation)
    
    # All other animations use CSS
    text_elements = []
    
    for idx, line in enumerate(lines):
        # Better positioning logic
        if multiline:
            # Calculate vertical centering for multiple lines
            total_text_height = len(lines) * line_height
            start_y = (height - total_text_height) / 2 + line_height
            y_pos = start_y + (idx * line_height)
        else:
            y_pos = (height / 2) + (size / 3)
        
        # For character-level animations, we need numeric positions
        x_pos_numeric = width / 2 if center else 20
        # For simple text elements, use percentage-based positioning to work properly in GitHub embeds
        x_pos = "50%" if center else "20"
        text_anchor = 'middle' if center else 'start'
        
        # Escape special XML characters in text
        escaped_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        # Check if line has inline obfuscation syntax ?(text)
        has_inline_obf = '?(' in line
        
        # For animations that need character-level control
        if animation in ['wave', 'fade', 'matrix', 'terminal', 'obfuscated', 'corrupt', 'sparkle', 'fire']:
            if animation == 'obfuscated' and not has_inline_obf:
                # Full line obfuscation - Generate obfuscated effect using stacked text elements
                char_width = size * 0.6  # Approximate monospace character width
                
                # Calculate starting x position
                if center:
                    total_width = len(line) * char_width
                    start_x = x_pos_numeric - (total_width / 2)
                else:
                    start_x = x_pos_numeric
                
                # Create a group for stacked text layers
                obf_groups = []
                for char_idx, char in enumerate(line):
                    char_x = start_x + (char_idx * char_width)
                    frames = generate_obfuscated_frames(char, 10)
                    
                    # Create stacked text elements for each frame
                    frame_texts = []
                    for f_idx, f_char in enumerate(frames):
                        escaped_char = f_char.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                        frame_texts.append(
                            f'<text x="{char_x}" y="{y_pos}" class="obf-frame obf-frame-{f_idx}" font-family="{font}, monospace" font-size="{size}" fill="{fill_color}">{escaped_char}</text>'
                        )
                    
                    # Wrap in a group with svg-text class for animations
                    obf_groups.append(f'<g class="obf-char svg-text">{"".join(frame_texts)}</g>')
                
                text_elements.append('\n    '.join(obf_groups))
            elif has_inline_obf:
                # Mixed normal and obfuscated text with ?(text) syntax
                segments = parse_obfuscated_text(line)
                char_width = size * 0.6
                
                # Calculate starting position
                if center:
                    total_width = len(line.replace('?(', '').replace(')', '')) * char_width
                    start_x = x_pos_numeric - (total_width / 2)
                else:
                    start_x = x_pos_numeric
                
                mixed_elements = []
                char_position = 0
                
                for segment_text, is_obfuscated in segments:
                    for char in segment_text:
                        char_x = start_x + (char_position * char_width)
                        
                        if is_obfuscated:
                            # Generate obfuscated frames for this character
                            frames = generate_obfuscated_frames(char, 10)
                            frame_texts = []
                            for f_idx, f_char in enumerate(frames):
                                escaped_char = f_char.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                                frame_texts.append(
                                    f'<text x="{char_x}" y="{y_pos}" class="obf-frame obf-frame-{f_idx}" font-family="{font}, monospace" font-size="{size}" fill="{fill_color}">{escaped_char}</text>'
                                )
                            mixed_elements.append(f'<g class="obf-char svg-text">{"".join(frame_texts)}</g>')
                        else:
                            # Normal static character
                            escaped_char = char.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                            mixed_elements.append(
                                f'<text x="{char_x}" y="{y_pos}" font-family="{font}, monospace" font-size="{size}" fill="{fill_color}">{escaped_char}</text>'
                            )
                        
                        char_position += 1
                
                text_elements.append('\n    '.join(mixed_elements))
            else:
                # Normal character-level animation
                chars_html = ''.join([
                    f'<tspan class="char" style="--char-index: {i}">{char.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")}</tspan>'
                    for i, char in enumerate(line)
                ])
                
                # Add cursor for terminal animation
                cursor_html = ''
                if animation == 'terminal' and idx == len(lines) - 1:
                    cursor_html = '<tspan class="cursor">|</tspan>'
                text_elements.append(
                    f'<text x="{x_pos}" y="{y_pos}" class="svg-text line-{idx}" text-anchor="{text_anchor}">{chars_html}{cursor_html}</text>'
                )
        else:
            # For simple animations, check for inline obfuscation
            if has_inline_obf:
                segments = parse_obfuscated_text(line)
                char_width = size * 0.6
                
                if center:
                    total_width = len(line.replace('?(', '').replace(')', '')) * char_width
                    start_x = x_pos_numeric - (total_width / 2)
                else:
                    start_x = x_pos_numeric
                
                mixed_elements = []
                char_position = 0
                
                for segment_text, is_obfuscated in segments:
                    for char in segment_text:
                        char_x = start_x + (char_position * char_width)
                        
                        if is_obfuscated:
                            frames = generate_obfuscated_frames(char, 10)
                            frame_texts = []
                            for f_idx, f_char in enumerate(frames):
                                escaped_char = f_char.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                                frame_texts.append(
                                    f'<text x="{char_x}" y="{y_pos}" class="obf-frame obf-frame-{f_idx}" font-family="{font}, monospace" font-size="{size}" fill="{fill_color}">{escaped_char}</text>'
                                )
                            mixed_elements.append(f'<g class="obf-char svg-text">{"".join(frame_texts)}</g>')
                        else:
                            escaped_char = char.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                            mixed_elements.append(
                                f'<text x="{char_x}" y="{y_pos}" class="svg-text" font-family="{font}, monospace" font-size="{size}" fill="{fill_color}">{escaped_char}</text>'
                            )
                        
                        char_position += 1
                
                text_elements.append('\n    '.join(mixed_elements))
            else:
                text_elements.append(
                    f'<text x="{x_pos}" y="{y_pos}" class="svg-text line-{idx}" text-anchor="{text_anchor}">{escaped_line}</text>'
                )
    
    return '\n    '.join(text_elements)

@app.route('/generate')
def generate():
    """SVG generation endpoint."""
    # Get text lines (semicolon separated)
    lines_param = get_param('lines', 'Hello;World!')
    lines = [line.strip() for line in lines_param.split(';') if line.strip()]
    
    if not lines:
        lines = ['Add text with ?lines=Your+Text']
    
    # Get all customization parameters
    params = {
        'animation': get_param('animation', 'typing'),
        'font': get_param('font', 'Fira Code'),
        'size': get_param('size', '20'),
        'color': get_param('color', '409EFF'),
        'bg_color': get_param('bg_color', 'transparent'),
        'width': get_param('width', '600'),
        'height': get_param('height', '100'),
        'duration': get_param('duration', '5000'),
        'pause': get_param('pause', '1000'),
        'repeat': get_param('repeat', 'true'),
        'center': get_param('center', 'true'),
        'multiline': get_param('multiline', 'auto'),
        'glitch_intensity': get_param('glitch_intensity', '5'),
        'glitch_speed': get_param('glitch_speed', '0.1'),
        'gradient_angle': get_param('gradient_angle', '45'),
        'letter_spacing': get_param('letter_spacing', '0'),
        'stagger_delay': get_param('stagger_delay', '50'),
        'typing_mode': get_param('typing_mode', 'sequential'),
        'terminal_color_mode': get_param('terminal_color_mode', 'rainbow'),
        'terminal_colors': get_param('terminal_colors', 'FF0080,FF8000,FFFF00,00FF00,00FFFF,0080FF,8000FF'),
        'border_width': get_param('border_width', '0'),
        'border_color': get_param('border_color', '000000'),
        'border_radius': get_param('border_radius', '0'),
        'padding': get_param('padding', '0'),
    }
    
    svg = generate_svg(lines, **params)
    
    return Response(svg, mimetype='image/svg+xml', headers={
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
    })

@app.route('/fonts/<path:filename>')
def serve_font(filename):
    """Serve local font files."""
    import os
    font_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'fonts')
    return send_from_directory(font_dir, filename)

@app.route('/favicon.svg')
def favicon():
    """Serve animated favicon."""
    favicon_svg = '''<svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
    <style>
        @keyframes glowPulse {
            0%, 100% { 
                filter: drop-shadow(0 0 3px #6366f1) drop-shadow(0 0 6px #8b5cf6);
            }
            50% { 
                filter: drop-shadow(0 0 8px #6366f1) drop-shadow(0 0 15px #8b5cf6);
            }
        }
        @keyframes floatT {
            0%, 100% { 
                transform: translateY(0) rotate(0deg);
            }
            25% { 
                transform: translateY(-1px) rotate(-2deg);
            }
            75% { 
                transform: translateY(1px) rotate(2deg);
            }
        }
        @keyframes cursorSlide {
            0% { 
                transform: translateX(0);
                opacity: 0;
            }
            10% {
                opacity: 1;
            }
            90% {
                opacity: 1;
            }
            100% { 
                transform: translateX(8px);
                opacity: 0;
            }
        }
        @keyframes cursorBlink {
            0%, 49% { opacity: 1; }
            50%, 100% { opacity: 0; }
        }
        .logo-t {
            animation: glowPulse 2s ease-in-out infinite, floatT 3s ease-in-out infinite;
            transform-origin: center center;
        }
        .cursor {
            animation: cursorSlide 2s ease-in-out infinite, cursorBlink 0.7s step-end infinite;
        }
    </style>
    <rect width="32" height="32" fill="#0a0e27" rx="6"/>
    <defs>
        <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#6366f1;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#8b5cf6;stop-opacity:1" />
        </linearGradient>
    </defs>
    <g class="logo-t">
        <path d="M 8 9 L 24 9 L 24 12 L 18 12 L 18 24 L 14 24 L 14 12 L 8 12 Z" fill="url(#grad)"/>
    </g>
    <rect class="cursor" x="19" y="17" width="2" height="7" fill="#a5b4fc" rx="0.5"/>
</svg>'''
    
    return Response(favicon_svg, mimetype='image/svg+xml', headers={
        'Cache-Control': 'public, max-age=31536000'
    })

@app.route('/')
def home():
    demo_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TypeFlow - Animated SVG Generator</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        * { 
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body { 
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', sans-serif;
            color: #e2e8f0;
        }
        .glass-card {
            background: rgba(15, 23, 42, 0.7);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(148, 163, 184, 0.1);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .glass-card:hover {
            border-color: rgba(99, 102, 241, 0.3);
            transform: translateY(-2px);
        }
        .preview-container { 
            min-height: 300px;
            background: rgba(10, 14, 26, 0.8);
            border: 1px solid rgba(99, 102, 241, 0.2);
            box-shadow: 0 0 40px rgba(99, 102, 241, 0.1);
        }
        .btn-primary {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            box-shadow: 0 4px 20px rgba(99, 102, 241, 0.4);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .btn-primary:hover {
            box-shadow: 0 8px 30px rgba(99, 102, 241, 0.6);
            transform: translateY(-2px);
        }
        .input-field {
            background: rgba(15, 23, 42, 0.5);
            border: 1px solid rgba(148, 163, 184, 0.2);
            color: #e2e8f0;
            transition: all 200ms;
        }
        .input-field:focus {
            outline: none;
            border-color: #6366f1;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
        }
        .custom-select {
            position: relative;
            cursor: pointer;
        }
        .custom-select select {
            display: none;
        }
        .custom-dropdown {
            position: relative;
            width: 100%;
        }
        .dropdown-selected {
            background: rgba(15, 23, 42, 0.5);
            border: 1px solid rgba(148, 163, 184, 0.2);
            color: #e2e8f0;
            padding: 0.5rem 2.5rem 0.5rem 0.75rem;
            border-radius: 0.5rem;
            cursor: pointer;
            transition: all 0.2s;
            user-select: none;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .dropdown-selected:hover {
            border-color: rgba(99, 102, 241, 0.4);
            background: rgba(15, 23, 42, 0.7);
        }
        .dropdown-selected.active {
            border-color: #6366f1;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
        }
        .dropdown-arrow {
            color: #6366f1;
            font-size: 0.7rem;
            transition: transform 0.3s ease;
            margin-left: auto;
        }
        .dropdown-selected.active .dropdown-arrow {
            transform: rotate(180deg);
        }
        .dropdown-options {
            position: absolute;
            top: calc(100% + 0.25rem);
            left: 0;
            right: 0;
            background: rgba(15, 23, 42, 0.98);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 0.5rem;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5), 0 0 20px rgba(99, 102, 241, 0.2);
            max-height: 300px;
            overflow-y: auto;
            z-index: 1000;
            opacity: 0;
            transform: translateY(-10px);
            pointer-events: none;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            backdrop-filter: blur(20px);
        }
        .dropdown-options.show {
            opacity: 1;
            transform: translateY(0);
            pointer-events: all;
        }
        .dropdown-option {
            padding: 0.625rem 0.75rem;
            cursor: pointer;
            transition: all 0.15s;
            color: #cbd5e1;
            font-size: 0.875rem;
        }
        .dropdown-option:hover {
            background: rgba(99, 102, 241, 0.15);
            color: #e2e8f0;
        }
        .dropdown-option.selected {
            background: rgba(99, 102, 241, 0.2);
            color: #a5b4fc;
            font-weight: 500;
        }
        .dropdown-options::-webkit-scrollbar {
            width: 8px;
        }
        .dropdown-options::-webkit-scrollbar-track {
            background: rgba(15, 23, 42, 0.5);
            border-radius: 4px;
        }
        .dropdown-options::-webkit-scrollbar-thumb {
            background: rgba(99, 102, 241, 0.4);
            border-radius: 4px;
        }
        .dropdown-options::-webkit-scrollbar-thumb:hover {
            background: rgba(99, 102, 241, 0.6);
        }
        .tab-button {
            padding: 0.75rem 1.5rem;
            border-radius: 0.5rem;
            font-weight: 500;
            transition: all 0.3s;
            cursor: pointer;
            background: transparent;
            color: #94a3b8;
        }
        .tab-button.active {
            background: rgba(99, 102, 241, 0.15);
            color: #6366f1;
        }
        .tab-button:hover {
            background: rgba(99, 102, 241, 0.1);
            color: #818cf8;
        }
        .accordion-content {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .accordion-content.active {
            max-height: 2000px;
        }
        .accordion-header {
            cursor: pointer;
            user-select: none;
            transition: all 0.2s;
        }
        .accordion-header:hover {
            background: rgba(99, 102, 241, 0.08);
        }
        .badge {
            display: inline-block;
            padding: 3px 10px;
            border-radius: 9999px;
            font-size: 11px;
            font-weight: 600;
            background: rgba(99, 102, 241, 0.2);
            color: #a5b4fc;
        }
        .example-card {
            background: rgba(15, 23, 42, 0.5);
            border: 1px solid rgba(148, 163, 184, 0.1);
            border-radius: 0.75rem;
            padding: 1rem;
            transition: all 0.3s;
            cursor: pointer;
        }
        .example-card:hover {
            border-color: rgba(99, 102, 241, 0.4);
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(99, 102, 241, 0.2);
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .fade-in {
            animation: fadeIn 0.5s ease-out;
        }
        .content-wrapper {
            max-width: 1400px;
            margin: 0 auto;
        }
        @media (min-width: 1024px) {
            .content-wrapper {
                max-width: 1200px;
            }
        }
    </style>
    <link rel="icon" type="image/svg+xml" href="/favicon.svg">
</head>
<body class="min-h-screen p-4 md:p-8">
    <div class="content-wrapper">
        <div class="text-center mb-6 fade-in">
            <h1 class="text-5xl md:text-6xl font-bold bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent mb-3">TypeFlow</h1>
            <p class="text-slate-400 text-base">Animated SVG text for your projects</p>
        </div>
        
        <div class="flex justify-center gap-4 mb-8">
            <button onclick="switchTab('generator')" id="tab-generator" class="tab-button active">Generator</button>
            <button onclick="switchTab('examples')" id="tab-examples" class="tab-button">Examples</button>
        </div>

        <div id="generator-tab" class="grid grid-cols-1 lg:grid-cols-2 gap-6 fade-in">
            <div class="glass-card rounded-xl shadow-lg p-6 space-y-6">
                <!-- Core Settings -->
                <div class="space-y-5">
                    <!-- Text Lines -->
                    <div>
                        <div class="flex justify-between items-center mb-3">
                            <label class="block text-sm font-semibold text-slate-200">Text Lines</label>
                            <button onclick="addNewLine()" type="button" class="px-3 py-1.5 btn-primary text-white rounded-lg text-xs font-medium">
                                + Add Line
                            </button>
                        </div>
                        <div id="lines-container" class="space-y-2">
                            <div class="line-input-group flex gap-2">
                                <input type="text" class="line-input flex-1 input-field rounded-lg px-3 py-2 text-sm" value="Hello, World!" placeholder="Enter text...">
                                <button onclick="removeLine(this)" type="button" class="px-3 py-1.5 bg-slate-700 hover:bg-red-600 text-slate-200 hover:text-white rounded-lg text-xs font-medium transition-all">×</button>
                            </div>
                        </div>
                    </div>
                    
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-semibold text-slate-200 mb-2">Animation</label>
                            <div class="custom-select">
                                <select id="animation" class="w-full">
                                    <option value="typing">Typing</option>
                                    <option value="typewriter">Typewriter</option>
                                    <option value="fade">Fade In</option>
                                    <option value="slide">Slide In</option>
                                    <option value="wave">Wave</option>
                                    <option value="zoom">Zoom</option>
                                    <option value="pulse">Pulse</option>
                                    <option value="flip">Flip</option>
                                    <option value="bounce">Bounce</option>
                                    <option value="glitch">Glitch</option>
                                    <option value="glitch-heavy">Glitch Heavy</option>
                                    <option value="glitch-scan">Glitch Scan</option>
                                    <option value="corrupt">Corrupt</option>
                                    <option value="static">Static</option>
                                    <option value="shake">Shake</option>
                                    <option value="neon">Neon</option>
                                    <option value="rainbow">Rainbow</option>
                                    <option value="sparkle">Sparkle</option>
                                    <option value="fire">Fire</option>
                                    <option value="stroke">Stroke</option>
                                    <option value="rotate3d">Rotate 3D</option>
                                    <option value="gradient-shift">Gradient Shift</option>
                                    <option value="blur-focus">Blur Focus</option>
                                    <option value="obfuscated">Obfuscated</option>
                                    <option value="terminal">Terminal</option>
                                    <option value="matrix">Matrix</option>
                                </select>
                                <div class="custom-dropdown">
                                    <div class="dropdown-selected" data-target="animation">
                                        <span class="dropdown-text">Typing</span>
                                        <span class="dropdown-arrow">▼</span>
                                    </div>
                                    <div class="dropdown-options"></div>
                                </div>
                            </div>
                        </div>
                        
                        <div>
                            <label class="block text-sm font-semibold text-slate-200 mb-2">Font</label>
                            <div class="custom-select">
                                <select id="font" class="w-full">
                                    <option value="Fira Code">Fira Code</option>
                                    <option value="Inter">Inter</option>
                                    <option value="JetBrains Mono">JetBrains Mono</option>
                                    <option value="Roboto">Roboto</option>
                                    <option value="Poppins">Poppins</option>
                                    <option value="Montserrat">Montserrat</option>
                                    <option value="Oswald">Oswald</option>
                                </select>
                                <div class="custom-dropdown">
                                    <div class="dropdown-selected" data-target="font">
                                        <span class="dropdown-text">Fira Code</span>
                                        <span class="dropdown-arrow">▼</span>
                                    </div>
                                    <div class="dropdown-options"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="grid grid-cols-3 gap-4">
                        <div>
                            <label class="block text-sm font-semibold text-slate-200 mb-2">Size: <span id="size_value" class="text-indigo-400">24</span>px</label>
                            <input type="range" id="size_slider" min="10" max="100" value="24" class="w-full accent-indigo-500">
                            <input type="number" id="size" value="24" class="w-full input-field rounded-lg px-2 py-1.5 text-xs mt-1">
                        </div>
                        <div>
                            <label class="block text-sm font-semibold text-slate-200 mb-2">Width: <span id="width_value" class="text-indigo-400">600</span>px</label>
                            <input type="range" id="width_slider" min="200" max="1200" value="600" class="w-full accent-indigo-500">
                            <input type="number" id="width" value="600" class="w-full input-field rounded-lg px-2 py-1.5 text-xs mt-1">
                        </div>
                        <div>
                            <label class="block text-sm font-semibold text-slate-200 mb-2">Height: <span id="height_value" class="text-indigo-400">100</span>px</label>
                            <input type="range" id="height_slider" min="50" max="500" value="100" class="w-full accent-indigo-500">
                            <input type="number" id="height" value="100" class="w-full input-field rounded-lg px-2 py-1.5 text-xs mt-1">
                        </div>
                    </div>
                    
                    <div class="flex gap-4">
                        <label class="flex items-center text-sm text-slate-300">
                            <input type="checkbox" id="center" checked class="mr-2 accent-indigo-500">
                            Center
                        </label>
                        <label class="flex items-center text-sm text-slate-300">
                            <input type="checkbox" id="multiline" class="mr-2 accent-indigo-500">
                            Multiline
                        </label>
                        <label class="flex items-center text-sm text-slate-200">
                            <input type="checkbox" id="repeat" checked class="mr-2 accent-indigo-500">
                            Repeat
                        </label>
                    </div>
                </div>
                
                <!-- Collapsible: Colors & Background -->
                <div class="border-t border-slate-700 pt-5">
                    <div class="accordion-header rounded-lg p-3 flex justify-between items-center" onclick="toggleSection('colors')">
                        <span class="text-sm font-semibold text-slate-200">Colors & Background</span>
                        <span id="colors-icon" class="text-lg text-gray-500">+</span>
                    </div>
                    <div id="colors-section" class="accordion-content mt-3">
                        <div class="space-y-4">
                            <div>
                                <label class="block text-xs font-semibold text-slate-300 mb-2">Text Color</label>
                                <div class="flex gap-2">
                                    <input type="color" id="color_picker" value="#409EFF" class="h-10 w-14 border rounded-lg cursor-pointer">
                                    <input type="text" id="color" value="409EFF" placeholder="409EFF" class="flex-1 input-field rounded-lg px-3 py-2 font-mono text-xs">
                                </div>
                                <p class="text-xs text-slate-400 mt-1">Comma-separated for gradient</p>
                            </div>
                            
                            <div>
                                <label class="block text-xs font-semibold text-slate-300 mb-2">Background</label>
                                <div class="flex gap-2">
                                    <input type="color" id="bg_color_picker" value="#000000" class="h-10 w-14 border rounded-lg cursor-pointer">
                                    <input type="text" id="bg_color" value="transparent" placeholder="transparent" class="flex-1 input-field rounded-lg px-3 py-2 font-mono text-xs">
                                </div>
                                <p class="text-xs text-slate-400 mt-1">Use "transparent" or hex</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Collapsible: Animation Timing -->
                <div class="border-t border-slate-700 pt-5">
                    <div class="accordion-header rounded-lg p-3 flex justify-between items-center" onclick="toggleSection('timing')">
                        <span class="text-sm font-semibold text-slate-200">Animation Timing</span>
                        <span id="timing-icon" class="text-lg text-gray-500">+</span>
                    </div>
                    <div id="timing-section" class="accordion-content mt-3">
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-xs font-semibold text-slate-300 mb-2">Duration: <span id="duration_value" class="text-indigo-400">3000</span>ms</label>
                                <input type="range" id="duration_slider" min="500" max="10000" step="100" value="3000" class="w-full accent-indigo-500">
                                <input type="number" id="duration" value="3000" class="w-full input-field rounded-lg px-2 py-1.5 text-xs mt-1">
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-slate-300 mb-2">Letter Spacing: <span id="letter_spacing_value" class="text-indigo-400">0</span>px</label>
                                <input type="range" id="letter_spacing_slider" min="-5" max="20" value="0" class="w-full accent-indigo-500">
                                <input type="number" id="letter_spacing" value="0" class="w-full input-field rounded-lg px-2 py-1.5 text-xs mt-1">
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Collapsible: Text Effects -->
                <div class="border-t border-slate-700 pt-5">
                    <div class="accordion-header rounded-lg p-3 flex justify-between items-center" onclick="toggleSection('effects')">
                        <span class="text-sm font-semibold text-slate-200">Text Effects</span>
                        <span id="effects-icon" class="text-lg text-gray-500">+</span>
                    </div>
                    <div id="effects-section" class="accordion-content mt-3">
                        <div class="space-y-4">
                            <div class="grid grid-cols-2 gap-4">
                                <div>
                                    <label class="block text-xs font-semibold text-slate-300 mb-2">Glitch: <span id="glitch_intensity_value" class="text-indigo-400">5</span></label>
                                    <input type="range" id="glitch_intensity_slider" min="1" max="20" value="5" class="w-full accent-indigo-500">
                                    <input type="number" id="glitch_intensity" value="5" min="1" max="20" class="w-full input-field rounded-lg px-2 py-1.5 text-xs mt-1">
                                </div>
                                <div>
                                    <label class="block text-xs font-semibold text-slate-300 mb-2">Stagger: <span id="stagger_delay_value" class="text-indigo-400">50</span>ms</label>
                                    <input type="range" id="stagger_delay_slider" min="0" max="200" step="10" value="50" class="w-full accent-indigo-500">
                                    <input type="number" id="stagger_delay" value="50" class="w-full input-field rounded-lg px-2 py-1.5 text-xs mt-1">
                                </div>
                            </div>
                            
                            <div>
                                <label class="block text-xs font-semibold text-slate-300 mb-2">Typing Mode</label>
                                <div class="custom-select">
                                    <select id="typing_mode" class="w-full">
                                        <option value="sequential">Sequential</option>
                                        <option value="all">All at once</option>
                                    </select>
                                    <div class="custom-dropdown">
                                        <div class="dropdown-selected" data-target="typing_mode">
                                            <span class="dropdown-text">Sequential</span>
                                            <span class="dropdown-arrow">▼</span>
                                        </div>
                                        <div class="dropdown-options"></div>
                                    </div>
                                </div>
                            </div>
                            
                            <div>
                                <label class="block text-xs font-semibold text-slate-300 mb-2">Terminal Color Mode</label>
                                <div class="custom-select">
                                    <select id="terminal_color_mode" class="w-full">
                                        <option value="rainbow">Rainbow</option>
                                        <option value="static">Static</option>
                                        <option value="custom">Custom</option>
                                    </select>
                                    <div class="custom-dropdown">
                                        <div class="dropdown-selected" data-target="terminal_color_mode">
                                            <span class="dropdown-text">Rainbow</span>
                                            <span class="dropdown-arrow">▼</span>
                                        </div>
                                        <div class="dropdown-options"></div>
                                    </div>
                                </div>
                            </div>
                            
                            <div>
                                <label class="block text-xs font-semibold text-slate-300 mb-2">Custom Terminal Colors</label>
                                <div class="flex gap-2 mb-2">
                                    <input type="color" id="terminal_color_picker" value="#FF0080" class="h-10 w-14 border rounded-lg cursor-pointer">
                                    <button onclick="addTerminalColor()" type="button" class="px-3 py-1.5 btn-primary text-white rounded-lg text-xs font-medium">Add</button>
                                    <button onclick="clearTerminalColors()" type="button" class="px-3 py-1.5 bg-gray-200 hover:bg-red-100 text-slate-200 hover:text-red-600 rounded-lg text-xs font-medium">Clear</button>
                                </div>
                                <input type="text" id="terminal_colors" value="FF0080,FF8000,FFFF00,00FF00,00FFFF,0080FF,8000FF" class="w-full input-field rounded-lg px-3 py-2 font-mono text-xs">
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Collapsible: Border & Container -->
                <div class="border-t border-slate-700 pt-5">
                    <div class="accordion-header rounded-lg p-3 flex justify-between items-center" onclick="toggleSection('border')">
                        <span class="text-sm font-semibold text-slate-200">Border & Container</span>
                        <span id="border-icon" class="text-lg text-gray-500">+</span>
                    </div>
                    <div id="border-section" class="accordion-content mt-3">
                        <div class="grid grid-cols-2 gap-4">
                            <div>
                                <label class="block text-xs font-semibold text-slate-300 mb-2">Width: <span id="border_width_value" class="text-indigo-400">0</span>px</label>
                                <input type="range" id="border_width_slider" min="0" max="20" value="0" class="w-full accent-indigo-500">
                                <input type="number" id="border_width" value="0" min="0" max="20" class="w-full input-field rounded-lg px-2 py-1.5 text-xs mt-1">
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-slate-300 mb-2">Color</label>
                                <div class="flex gap-2">
                                    <input type="color" id="border_color_picker" value="#000000" class="h-10 w-14 border rounded-lg cursor-pointer">
                                    <input type="text" id="border_color" value="000000" class="flex-1 input-field rounded-lg px-3 py-2 font-mono text-xs">
                                </div>
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-slate-300 mb-2">Radius: <span id="border_radius_value" class="text-indigo-400">0</span>px</label>
                                <input type="range" id="border_radius_slider" min="0" max="100" value="0" class="w-full accent-indigo-500">
                                <input type="number" id="border_radius" value="0" min="0" max="100" class="w-full input-field rounded-lg px-2 py-1.5 text-xs mt-1">
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-slate-300 mb-2">Padding: <span id="padding_value" class="text-indigo-400">0</span>px</label>
                                <input type="range" id="padding_slider" min="0" max="100" value="0" class="w-full accent-indigo-500">
                                <input type="number" id="padding" value="0" min="0" max="100" class="w-full input-field rounded-lg px-2 py-1.5 text-xs mt-1">
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Update Button -->
                <button onclick="updatePreview()" class="w-full btn-primary text-white font-semibold py-3 px-4 rounded-lg mt-6">
                    Generate
                </button>
                </div>
            </div>
            
            <!-- Preview -->
            <div class="space-y-6">
                <!-- Live Preview -->
                <div class="preview-container rounded-xl p-8 flex items-center justify-center sticky top-6">
                    <img id="preview" src="/generate?lines=Hello,+World!&animation=typing&size=24" alt="SVG Preview" class="max-w-full rounded-lg">
                </div>
                
                <!-- Embed Code -->
                <div class="glass-card rounded-xl shadow-lg p-6">
                    <h3 class="text-sm font-semibold text-slate-200 mb-3">Embed Code</h3>
                    <textarea id="embed-code" readonly class="w-full rounded-lg p-3 font-mono text-xs h-24 resize-none bg-black text-white border border-slate-700"></textarea>
                    <button onclick="copyToClipboard()" class="mt-3 w-full btn-primary text-white font-semibold py-2.5 px-4 rounded-lg text-sm">
                        Copy to Clipboard
                    </button>
                </div>
            </div>
        </div>

        <div id="examples-tab" class="hidden fade-in">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div class="example-card" onclick="loadExample('typing', 'Hello TypeFlow', 'typing')">
                    <div class="mb-3"><img src="/generate?lines=Hello+TypeFlow&animation=typing&size=28&width=400&height=100" class="w-full rounded" alt="Typing"></div>
                    <h4 class="font-semibold text-slate-100 mb-1">Typing</h4>
                    <p class="text-xs text-slate-400">Classic typewriter effect</p>
                </div>
                <div class="example-card" onclick="loadExample('fade', 'Fade+In', 'fade')">
                    <div class="mb-3"><img src="/generate?lines=Fade+In&animation=fade&size=28&width=400&height=100" class="w-full rounded" alt="Fade"></div>
                    <h4 class="font-semibold text-slate-100 mb-1">Fade</h4>
                    <p class="text-xs text-slate-400">Smooth fade in animation</p>
                </div>
                <div class="example-card" onclick="loadExample('wave', 'Wave+Motion', 'wave')">
                    <div class="mb-3"><img src="/generate?lines=Wave+Motion&animation=wave&size=28&width=400&height=100" class="w-full rounded" alt="Wave"></div>
                    <h4 class="font-semibold text-slate-100 mb-1">Wave</h4>
                    <p class="text-xs text-slate-400">Flowing wave motion</p>
                </div>
                <div class="example-card" onclick="loadExample('flip', 'Flip+Effect', 'flip')">
                    <div class="mb-3"><img src="/generate?lines=Flip+Effect&animation=flip&size=28&width=400&height=100" class="w-full rounded" alt="Flip"></div>
                    <h4 class="font-semibold text-slate-100 mb-1">Flip</h4>
                    <p class="text-xs text-slate-400">3D flip rotation</p>
                </div>
                <div class="example-card" onclick="loadExample('bounce', 'Bounce!', 'bounce')">
                    <div class="mb-3"><img src="/generate?lines=Bounce!&animation=bounce&size=28&width=400&height=100" class="w-full rounded" alt="Bounce"></div>
                    <h4 class="font-semibold text-slate-100 mb-1">Bounce</h4>
                    <p class="text-xs text-slate-400">Elastic bounce effect</p>
                </div>
                <div class="example-card" onclick="loadExample('glitch', 'GLITCH', 'glitch')">
                    <div class="mb-3"><img src="/generate?lines=GLITCH&animation=glitch&size=28&width=400&height=100" class="w-full rounded" alt="Glitch"></div>
                    <h4 class="font-semibold text-slate-100 mb-1">Glitch</h4>
                    <p class="text-xs text-slate-400">Digital glitch effect</p>
                </div>
                <div class="example-card" onclick="loadExample('fire', 'FIRE', 'fire')">
                    <div class="mb-3"><img src="/generate?lines=FIRE&animation=fire&size=28&width=400&height=100&color=FF4500" class="w-full rounded" alt="Fire"></div>
                    <h4 class="font-semibold text-slate-100 mb-1">Fire</h4>
                    <p class="text-xs text-slate-400">Realistic flame animation</p>
                </div>
                <div class="example-card" onclick="loadExample('matrix', 'Matrix+Rain', 'matrix')">
                    <div class="mb-3"><img src="/generate?lines=Matrix+Rain&animation=matrix&size=28&width=400&height=100&color=00FF00" class="w-full rounded" alt="Matrix"></div>
                    <h4 class="font-semibold text-slate-100 mb-1">Matrix</h4>
                    <p class="text-xs text-slate-400">Matrix cascade effect</p>
                </div>
                <div class="example-card" onclick="loadExample('obfuscated', 'Hello+?(Secret)', 'obfuscated')">
                    <div class="mb-3"><img src="/generate?lines=Hello+?(Secret)&animation=obfuscated&size=28&width=400&height=100" class="w-full rounded" alt="Obfuscated"></div>
                    <h4 class="font-semibold text-slate-100 mb-1">Obfuscated <span class="badge">?(text)</span></h4>
                    <p class="text-xs text-slate-400">Minecraft-style scramble. Use ?(text) to scramble specific words</p>
                </div>
                <div class="example-card" onclick="loadExample('neon', 'NEON+GLOW', 'neon')">
                    <div class="mb-3"><img src="/generate?lines=NEON+GLOW&animation=neon&size=28&width=400&height=100&color=00FFFF" class="w-full rounded" alt="Neon"></div>
                    <h4 class="font-semibold text-slate-100 mb-1">Neon</h4>
                    <p class="text-xs text-slate-400">Glowing neon sign effect</p>
                </div>
                <div class="example-card" onclick="loadExample('rainbow', 'Rainbow+Colors', 'rainbow')">
                    <div class="mb-3"><img src="/generate?lines=Rainbow+Colors&animation=rainbow&size=28&width=400&height=100" class="w-full rounded" alt="Rainbow"></div>
                    <h4 class="font-semibold text-slate-100 mb-1">Rainbow</h4>
                    <p class="text-xs text-slate-400">Shifting rainbow hues</p>
                </div>
                <div class="example-card" onclick="loadExample('sparkle', 'Sparkle✨', 'sparkle')">
                    <div class="mb-3"><img src="/generate?lines=Sparkle✨&animation=sparkle&size=28&width=400&height=100&color=FFD700" class="w-full rounded" alt="Sparkle"></div>
                    <h4 class="font-semibold text-slate-100 mb-1">Sparkle</h4>
                    <p class="text-xs text-slate-400">Shimmering sparkle effect</p>
                </div>
                <div class="example-card" onclick="loadExample('rotate3d', 'Rotate+3D', 'rotate3d')">
                    <div class="mb-3"><img src="/generate?lines=Rotate+3D&animation=rotate3d&size=28&width=400&height=100" class="w-full rounded" alt="Rotate 3D"></div>
                    <h4 class="font-semibold text-slate-100 mb-1">Rotate 3D</h4>
                    <p class="text-xs text-slate-400">3D rotation effect</p>
                </div>
                <div class="example-card" onclick="loadExample('pulse', 'Pulse', 'pulse')">
                    <div class="mb-3"><img src="/generate?lines=Pulse&animation=pulse&size=28&width=400&height=100&color=FF1493" class="w-full rounded" alt="Pulse"></div>
                    <h4 class="font-semibold text-slate-100 mb-1">Pulse</h4>
                    <p class="text-xs text-slate-400">Heartbeat pulsing effect</p>
                </div>
                <div class="example-card" onclick="loadExample('zoom', 'Zoom+In!', 'zoom')">
                    <div class="mb-3"><img src="/generate?lines=Zoom+In!&animation=zoom&size=28&width=400&height=100" class="w-full rounded" alt="Zoom"></div>
                    <h4 class="font-semibold text-slate-100 mb-1">Zoom</h4>
                    <p class="text-xs text-slate-400">Dramatic zoom entrance</p>
                </div>
                <div class="example-card" onclick="loadExample('shake', 'Shake!', 'shake')">
                    <div class="mb-3"><img src="/generate?lines=Shake!&animation=shake&size=28&width=400&height=100&color=FF0000" class="w-full rounded" alt="Shake"></div>
                    <h4 class="font-semibold text-slate-100 mb-1">Shake</h4>
                    <p class="text-xs text-slate-400">Intense shaking motion</p>
                </div>
                <div class="example-card" onclick="loadExample('gradient-shift', 'Gradient+Flow', 'gradient-shift')">
                    <div class="mb-3"><img src="/generate?lines=Gradient+Flow&animation=gradient-shift&size=28&width=400&height=100&color=FF00FF,00FFFF,FFFF00" class="w-full rounded" alt="Gradient Shift"></div>
                    <h4 class="font-semibold text-slate-100 mb-1">Gradient Shift</h4>
                    <p class="text-xs text-slate-400">Flowing gradient colors</p>
                </div>
                <div class="example-card" onclick="loadExample('stroke', 'Stroke+Draw', 'stroke')">
                    <div class="mb-3"><img src="/generate?lines=Stroke+Draw&animation=stroke&size=28&width=400&height=100&color=6366F1" class="w-full rounded" alt="Stroke"></div>
                    <h4 class="font-semibold text-slate-100 mb-1">Stroke</h4>
                    <p class="text-xs text-slate-400">Drawing stroke animation</p>
                </div>
                <div class="example-card" onclick="loadExample('typewriter', 'Typewriter+Click', 'typewriter')">
                    <div class="mb-3"><img src="/generate?lines=Typewriter+Click&animation=typewriter&size=28&width=400&height=100" class="w-full rounded" alt="Typewriter"></div>
                    <h4 class="font-semibold text-slate-100 mb-1">Typewriter</h4>
                    <p class="text-xs text-slate-400">Classic typewriter with cursor</p>
                </div>
                <div class="example-card" onclick="loadExample('terminal', 'user@terminal:~$', 'terminal')">
                    <div class="mb-3"><img src="/generate?lines=user@terminal:~$&animation=terminal&size=28&width=400&height=100&color=00FF00" class="w-full rounded" alt="Terminal"></div>
                    <h4 class="font-semibold text-slate-100 mb-1">Terminal</h4>
                    <p class="text-xs text-slate-400">Terminal-style typing</p>
                </div>
            </div>
            <div class="mt-8 glass-card rounded-xl p-6">
                <h3 class="text-lg font-bold text-slate-100 mb-3">💡 Using ?(text) Syntax</h3>
                <p class="text-slate-300 text-sm mb-4">Wrap any text in <code class="bg-slate-700 px-2 py-1 rounded text-indigo-300">?(text)</code> to make it obfuscated while keeping the rest normal. Works with most animations!</p>
                <div class="space-y-2 text-sm">
                    <div class="bg-slate-800 p-3 rounded"><code class="text-indigo-300">?lines=Hello+?(World)&animation=flip</code></div>
                    <p class="text-slate-400 text-xs">Note: Obfuscated text works best with: flip, bounce, zoom, rotate3d, pulse, slide. Some complex effects like typing or terminal may not support ?(text) syntax.</p>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function switchTab(tab) {
            const generatorTab = document.getElementById('generator-tab');
            const examplesTab = document.getElementById('examples-tab');
            const genButton = document.getElementById('tab-generator');
            const exButton = document.getElementById('tab-examples');
            
            if (tab === 'generator') {
                generatorTab.classList.remove('hidden');
                examplesTab.classList.add('hidden');
                genButton.classList.add('active');
                exButton.classList.remove('active');
            } else {
                generatorTab.classList.add('hidden');
                examplesTab.classList.remove('hidden');
                genButton.classList.remove('active');
                exButton.classList.add('active');
            }
        }
        
        function loadExample(name, text, animation) {
            switchTab('generator');
            const lines = text.split('+');
            const container = document.getElementById('lines-container');
            container.innerHTML = '';
            lines.forEach(line => {
                const newLineDiv = document.createElement('div');
                newLineDiv.className = 'line-input-group flex gap-2';
                newLineDiv.innerHTML = `
                    <input type="text" class="line-input flex-1 input-field rounded-lg px-3 py-2 text-sm" value="${line.replace(/\+/g, ' ')}" placeholder="Enter text...">
                    <button onclick="removeLine(this)" type="button" class="px-3 py-1.5 bg-slate-700 hover:bg-red-600 text-slate-200 hover:text-white rounded-lg text-xs font-medium transition-all">×</button>
                `;
                container.appendChild(newLineDiv);
            });
            document.getElementById('animation').value = animation;
            updatePreview();
        }
        
        function toggleSection(name) {
            const section = document.getElementById(`${name}-section`);
            const icon = document.getElementById(`${name}-icon`);
            
            section.classList.toggle('active');
            icon.textContent = section.classList.contains('active') ? '−' : '+';
        }
        
        function getAllLines() {
            const lineInputs = document.querySelectorAll('.line-input');
            const lines = Array.from(lineInputs)
                .map(input => input.value.trim())
                .filter(line => line.length > 0);
            return lines.join(';');
        }
        
        function addNewLine() {
            const container = document.getElementById('lines-container');
            const newLineDiv = document.createElement('div');
            newLineDiv.className = 'line-input-group flex gap-2';
            newLineDiv.innerHTML = `
                <input type="text" class="line-input flex-1 input-field rounded-lg px-3 py-2 text-sm" value="" placeholder="Enter text...">
                <button onclick="removeLine(this)" type="button" class="px-3 py-1.5 bg-slate-700 hover:bg-red-600 text-slate-200 hover:text-white rounded-lg text-xs font-medium transition-all">×</button>
            `;
            container.appendChild(newLineDiv);
        }
        
        function removeLine(button) {
            const container = document.getElementById('lines-container');
            const lineGroups = container.querySelectorAll('.line-input-group');
            if (lineGroups.length > 1) {
                button.parentElement.remove();
            } else {
                alert('You must have at least one line!');
            }
        }
        
        function buildURL() {
            const params = new URLSearchParams();
            params.append('lines', getAllLines());
            params.append('animation', document.getElementById('animation').value);
            params.append('font', document.getElementById('font').value);
            params.append('color', document.getElementById('color').value);
            params.append('bg_color', document.getElementById('bg_color').value);
            params.append('size', document.getElementById('size').value);
            params.append('width', document.getElementById('width').value);
            params.append('height', document.getElementById('height').value);
            params.append('duration', document.getElementById('duration').value);
            params.append('center', document.getElementById('center').checked);
            params.append('repeat', document.getElementById('repeat').checked);
            params.append('letter_spacing', document.getElementById('letter_spacing').value);
            params.append('glitch_intensity', document.getElementById('glitch_intensity').value);
            params.append('stagger_delay', document.getElementById('stagger_delay').value);
            params.append('typing_mode', document.getElementById('typing_mode').value);
            params.append('terminal_color_mode', document.getElementById('terminal_color_mode').value);
            params.append('terminal_colors', document.getElementById('terminal_colors').value);
            params.append('border_width', document.getElementById('border_width').value);
            params.append('border_color', document.getElementById('border_color').value);
            params.append('border_radius', document.getElementById('border_radius').value);
            params.append('padding', document.getElementById('padding').value);
            
            return '/generate?' + params.toString();
        }
        
        function updatePreview() {
            const url = buildURL();
            document.getElementById('preview').src = url + '&_t=' + Date.now();
            
            const embedURL = window.location.origin + url;
            const isCentered = document.getElementById('center').checked;
            
            // Always provide HTML format, with centering div if center is enabled
            if (isCentered) {
                document.getElementById('embed-code').value = `<div align="center">\n  <img src="${embedURL}" alt="Animated SVG">\n</div>`;
            } else {
                document.getElementById('embed-code').value = `<img src="${embedURL}" alt="Animated SVG">`;
            }
        }
        
        function copyToClipboard() {
            const textarea = document.getElementById('embed-code');
            textarea.select();
            textarea.setSelectionRange(0, 99999); // For mobile
            
            navigator.clipboard.writeText(textarea.value).then(() => {
                const btn = event.target;
                const originalText = btn.textContent;
                btn.textContent = '✓ Copied!';
                btn.style.background = 'linear-gradient(135deg, #10b981 0%, #059669 100%)';
                setTimeout(() => {
                    btn.textContent = originalText;
                    btn.style.background = '';
                }, 2000);
            }).catch(() => {
                // Fallback
                document.execCommand('copy');
                alert('Copied to clipboard!');
            });
        }
        
        // Color picker sync functions
        function syncColorPicker() {
            const colorInput = document.getElementById('color');
            const colorPicker = document.getElementById('color_picker');
            if (!colorInput.value.includes(',')) {
                const hex = colorInput.value.replace('#', '');
                colorPicker.value = '#' + hex;
            }
        }
        
        function syncBgColorPicker() {
            const bgInput = document.getElementById('bg_color');
            const bgPicker = document.getElementById('bg_color_picker');
            if (bgInput.value !== 'transparent' && !bgInput.value.includes(',')) {
                const hex = bgInput.value.replace('#', '');
                bgPicker.value = '#' + hex;
            }
        }
        
        // Sync text input when color picker changes
        document.getElementById('color_picker').addEventListener('input', function() {
            document.getElementById('color').value = this.value.replace('#', '');
            updatePreview();
        });
        
        document.getElementById('bg_color_picker').addEventListener('input', function() {
            document.getElementById('bg_color').value = this.value.replace('#', '');
            updatePreview();
        });
        
        // Sync picker when text input changes
        document.getElementById('color').addEventListener('input', syncColorPicker);
        document.getElementById('bg_color').addEventListener('input', syncBgColorPicker);
        
        // Border color picker sync
        document.getElementById('border_color_picker').addEventListener('input', function() {
            document.getElementById('border_color').value = this.value.replace('#', '');
            updatePreview();
        });
        
        document.getElementById('border_color').addEventListener('input', function() {
            const hex = this.value.replace('#', '');
            document.getElementById('border_color_picker').value = '#' + hex;
        });
        
        // Slider sync functions
        function syncSlider(sliderId, inputId, valueId) {
            const slider = document.getElementById(sliderId);
            const input = document.getElementById(inputId);
            const valueDisplay = document.getElementById(valueId);
            
            // Sync slider -> input & display
            slider.addEventListener('input', function() {
                input.value = this.value;
                valueDisplay.textContent = this.value;
                updatePreview();
            });
            
            // Sync input -> slider & display
            input.addEventListener('input', function() {
                slider.value = this.value;
                valueDisplay.textContent = this.value;
            });
        }
        
        // Initialize all slider syncs
        syncSlider('size_slider', 'size', 'size_value');
        syncSlider('width_slider', 'width', 'width_value');
        syncSlider('height_slider', 'height', 'height_value');
        syncSlider('duration_slider', 'duration', 'duration_value');
        syncSlider('letter_spacing_slider', 'letter_spacing', 'letter_spacing_value');
        syncSlider('glitch_intensity_slider', 'glitch_intensity', 'glitch_intensity_value');
        syncSlider('stagger_delay_slider', 'stagger_delay', 'stagger_delay_value');
        syncSlider('border_width_slider', 'border_width', 'border_width_value');
        syncSlider('border_radius_slider', 'border_radius', 'border_radius_value');
        syncSlider('padding_slider', 'padding', 'padding_value');
        
        // Terminal color functions
        function addTerminalColor() {
            const picker = document.getElementById('terminal_color_picker');
            const input = document.getElementById('terminal_colors');
            const newColor = picker.value.replace('#', '');
            
            if (input.value.trim() === '') {
                input.value = newColor;
            } else {
                input.value += ',' + newColor;
            }
            updatePreview();
        }
        
        function clearTerminalColors() {
            document.getElementById('terminal_colors').value = '';
            updatePreview();
        }
        
        // Custom Dropdown Functionality
        function initCustomDropdowns() {
            document.querySelectorAll('.custom-select').forEach(selectWrapper => {
                const select = selectWrapper.querySelector('select');
                const dropdown = selectWrapper.querySelector('.custom-dropdown');
                if (!select || !dropdown) return;
                
                const selected = dropdown.querySelector('.dropdown-selected');
                const optionsContainer = dropdown.querySelector('.dropdown-options');
                const selectId = select.id;
                
                // Populate dropdown options
                const options = Array.from(select.options);
                optionsContainer.innerHTML = options.map(option => `
                    <div class="dropdown-option ${option.selected ? 'selected' : ''}" data-value="${option.value}">
                        ${option.text}
                    </div>
                `).join('');
                
                // Toggle dropdown
                selected.addEventListener('click', (e) => {
                    e.stopPropagation();
                    const isActive = selected.classList.contains('active');
                    
                    // Close all other dropdowns
                    document.querySelectorAll('.dropdown-selected.active').forEach(other => {
                        if (other !== selected) {
                            other.classList.remove('active');
                            other.parentElement.querySelector('.dropdown-options').classList.remove('show');
                        }
                    });
                    
                    // Toggle current dropdown
                    selected.classList.toggle('active');
                    optionsContainer.classList.toggle('show');
                });
                
                // Handle option selection
                optionsContainer.addEventListener('click', (e) => {
                    const option = e.target.closest('.dropdown-option');
                    if (!option) return;
                    
                    const value = option.dataset.value;
                    const text = option.textContent.trim();
                    
                    // Update visual selection
                    optionsContainer.querySelectorAll('.dropdown-option').forEach(opt => {
                        opt.classList.remove('selected');
                    });
                    option.classList.add('selected');
                    
                    // Update display text
                    selected.querySelector('.dropdown-text').textContent = text;
                    
                    // Update hidden select
                    select.value = value;
                    
                    // Trigger change event
                    select.dispatchEvent(new Event('change'));
                    
                    // Close dropdown
                    selected.classList.remove('active');
                    optionsContainer.classList.remove('show');
                    
                    updatePreview();
                });
            });
            
            // Close dropdowns when clicking outside
            document.addEventListener('click', () => {
                document.querySelectorAll('.dropdown-selected.active').forEach(selected => {
                    selected.classList.remove('active');
                    selected.parentElement.querySelector('.dropdown-options').classList.remove('show');
                });
            });
        }
        
        // Initialize custom dropdowns
        initCustomDropdowns();
        
        // Auto-update on input
        document.querySelectorAll('input, select, textarea').forEach(elem => {
            elem.addEventListener('change', updatePreview);
        });
        
        // Initial sync and update
        syncColorPicker();
        syncBgColorPicker();
        updatePreview();
    </script>
</body>
</html>'''
    return demo_html

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

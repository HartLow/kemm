import re

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

idx = read_file('index.html')
kn = read_file('khai-niem.html')
lh = read_file('lien-he.html')
vm = read_file('vi-moi.html')
vtt = read_file('vi-truyen-thong.html')

# Extract CSS
def extract_css(html):
    m = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
    return m.group(1) if m else ""

idx_css = extract_css(idx)
kn_css = extract_css(kn)
lh_css = extract_css(lh)
vm_css = extract_css(vm)
vtt_css = extract_css(vtt)

combined_css = idx_css + "\n" + kn_css + "\n" + lh_css + "\n" + vm_css + "\n" + vtt_css

# Clean up CSS (remove basic duplicates)
combined_css = re.sub(r':root\s*\{[^}]*\}', '', combined_css)
combined_css = re.sub(r'\*,\s*\*\s*::before,\s*\*\s*::after\s*\{[^}]*\}', '', combined_css)
combined_css = re.sub(r'body\s*\{[^}]*\}', '', combined_css)
combined_css = re.sub(r'body\.page-in\s*\{[^}]*\}', '', combined_css)
combined_css = re.sub(r'body\.page-out\s*\{[^}]*\}', '', combined_css)
combined_css = re.sub(r'#cursor-glow\s*\{[^}]*\}', '', combined_css)
combined_css = re.sub(r'\.blob\s*\{[^}]*\}', '', combined_css)
combined_css = re.sub(r'@keyframes f[abc]\s*\{[^}]*\}', '', combined_css)

base_css = """
    :root {
      --ease-bounce: cubic-bezier(.34,1.56,.64,1);
      --ease-smooth: cubic-bezier(.25,.8,.25,1);
      
      --theme-idx-1: rgba(255,140,200,0.75); --theme-idx-2: rgba(200,253,230,0.7); --theme-idx-3: rgba(255,200,232,0.75);
      --bg-idx: linear-gradient(145deg, #ffedf7 0%, #ffd5eb 50%, #e8fff6 100%);
    }
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: "Quicksand", sans-serif;
      min-height: 100vh;
      color: #3d1530;
      background:
        radial-gradient(ellipse 60% 40% at 8% 5%, var(--theme-idx-1), transparent),
        radial-gradient(ellipse 55% 45% at 92% 10%, var(--theme-idx-2), transparent),
        radial-gradient(ellipse 50% 50% at 55% 92%, var(--theme-idx-3), transparent),
        var(--bg-idx);
      overflow-x: hidden;
      opacity: 0;
      transform: translateY(14px);
      transition: opacity .4s var(--ease-smooth), transform .4s var(--ease-smooth), background 0.8s ease;
    }
    body.page-in  { opacity: 1; transform: translateY(0); }
    body.page-out { opacity: 0; transform: translateY(10px); }

    /* Theme overrides for pages */
    body[data-page="khai-niem"] { --theme-idx-1: rgba(255,180,220,.7); --theme-idx-2: rgba(190,250,225,.65); --theme-idx-3: rgba(0,0,0,0); --bg-idx: linear-gradient(155deg, #fcedf5 0%, #ffd6eb 55%, #edfff7 100%); }
    body[data-page="lien-he"] { --theme-idx-1: rgba(255,160,210,.72); --theme-idx-2: rgba(200,240,255,.65); --theme-idx-3: rgba(0,0,0,0); --bg-idx: linear-gradient(150deg, #fce0f0 0%, #f5b8d2 50%, #e8f4ff 100%); }
    body[data-page="vi-moi"] { --theme-idx-1: rgba(255,170,215,.75); --theme-idx-2: rgba(180,255,225,.7); --theme-idx-3: rgba(210,190,255,.45); --bg-idx: linear-gradient(145deg, #fceaf5 0%, #f0d4ea 50%, #eafff7 100%); }
    body[data-page="vi-truyen-thong"] { --theme-idx-1: rgba(255,140,185,.75); --theme-idx-2: rgba(255,220,150,.65); --theme-idx-3: rgba(0,0,0,0); --bg-idx: linear-gradient(150deg, #fcd5e8 0%, #f5a9c6 45%, #ffe8c0 100%); }

    #cursor-glow {
      position: fixed; pointer-events: none; z-index: 9999;
      width: 320px; height: 320px; top: 0; left: 0;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(255,150,210,0.18) 0%, transparent 70%);
      transform: translate(-50%, -50%);
      transition: transform .08s linear;
      will-change: transform;
      mix-blend-mode: multiply;
    }

    .blob {
      position: fixed; border-radius: 50%; z-index: -1;
      filter: blur(28px); opacity: .5;
      will-change: transform;
      transform: translateZ(0);
    }
    
    .page-section { display: none; }
    .page-section.active { display: block; animation: fadeIn .5s forwards; }
    @keyframes fadeIn { from { opacity:0; } to { opacity:1; } }
"""

combined_css = base_css + combined_css

# Extract body contents
def extract_body(html):
    m = re.search(r'<body>(.*?)<script>', html, re.DOTALL)
    if not m: return ""
    b = m.group(1)
    # Remove blobs and cursor glow from subpages
    b = re.sub(r'<div id="cursor-glow"></div>', '', b)
    b = re.sub(r'<div class="blob.*?</div>', '', b, flags=re.DOTALL)
    # Remove standalone nav topbars (we will replace their links and class to just topbar)
    # Wait, keeping topbar is good, just change the href
    b = re.sub(r'href="index\.html"', 'href="#" onclick="navTo(\'home\'); return false;"', b)
    return b.strip()

idx_body = extract_body(idx)
kn_body = extract_body(kn)
lh_body = extract_body(lh)
vm_body = extract_body(vm)
vtt_body_str = extract_body(vtt)

# Replace menu links in idx_body
idx_body = idx_body.replace('href="khai-niem.html"', 'href="#" onclick="navTo(\'khai-niem\'); return false;"')
idx_body = idx_body.replace('href="vi-truyen-thong.html"', 'href="#" onclick="navTo(\'vi-truyen-thong\'); return false;"')
idx_body = idx_body.replace('href="vi-moi.html"', 'href="#" onclick="navTo(\'vi-moi\'); return false;"')
idx_body = idx_body.replace('href="lien-he.html"', 'href="#" onclick="navTo(\'lien-he\'); return false;"')

# Create the final html
final_html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Tiệm Kem Sweety Ice – Trang Chủ</title>
  <meta name="description" content="Sweety Ice House – kem tươi ngọt mỗi ngày, vị kem truyền thống và sáng tạo tại Quảng Ngãi." />
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" />
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css" rel="stylesheet" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Lilita+One&family=Pacifico&family=Quicksand:wght@500;700&display=swap" rel="stylesheet" />
  <style>
{combined_css}
  </style>
</head>
<body data-page="home">
  <!-- Cursor glow -->
  <div id="cursor-glow"></div>

  <!-- Blobs -->
  <div class="blob blob-a"></div>
  <div class="blob blob-b"></div>
  <div class="blob blob-c"></div>

  <!-- Confetti -->
  <div class="confetti-wrap" id="confetti"></div>

  <!-- PAGES -->
  <div id="page-home" class="page-section active">
    {idx_body}
  </div>

  <div id="page-khai-niem" class="page-section">
    {kn_body}
  </div>

  <div id="page-vi-truyen-thong" class="page-section">
    {vtt_body_str}
  </div>

  <div id="page-vi-moi" class="page-section">
    {vm_body}
  </div>

  <div id="page-lien-he" class="page-section">
    {lh_body}
  </div>

  <script>
    requestAnimationFrame(() => {{ document.body.classList.add('page-in'); }});

    const glow = document.getElementById('cursor-glow');
    document.addEventListener('mousemove', e => {{
      glow.style.transform = `translate(calc(${{e.clientX}}px - 50%), calc(${{e.clientY}}px - 50%))`;
    }}, {{ passive: true }});

    // Confetti
    const wrap = document.getElementById('confetti');
    if (wrap) {{
      const colors = ['#ff9bd2','#ffcfe8','#b5fcdf','#ffc867','#c8d4ff','#ffe680'];
      const frag = document.createDocumentFragment();
      for (let i = 0; i < 28; i++) {{
        const d = document.createElement('div');
        const size = 5 + Math.random() * 8;
        d.className = 'dot';
        Object.assign(d.style, {{
          width: size+'px', height: size+'px',
          background: colors[Math.floor(Math.random()*colors.length)],
          left: (Math.random()*100)+'%',
          top: (Math.random()*100)+'%',
          animationDuration: (8 + Math.random()*12)+'s',
          animationDelay: (Math.random()*12)+'s',
        }});
        frag.appendChild(d);
      }}
      wrap.appendChild(frag);
    }}

    // Ripple
    document.querySelectorAll('.menu-card').forEach(card => {{
      card.addEventListener('click', function (e) {{
        const r = document.createElement('span');
        r.className = 'ripple';
        const rect = this.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        Object.assign(r.style, {{
          width: size+'px', height: size+'px',
          left: (e.clientX - rect.left - size/2)+'px',
          top:  (e.clientY - rect.top  - size/2)+'px',
        }});
        this.appendChild(r);
        setTimeout(() => r.remove(), 600);
      }});
    }});

    // Navigation
    function navTo(pageId) {{
      window.scrollTo(0, 0);
      document.body.classList.remove('page-in');
      document.body.classList.add('page-out');
      
      setTimeout(() => {{
        document.querySelectorAll('.page-section').forEach(el => el.classList.remove('active'));
        document.getElementById('page-' + pageId).classList.add('active');
        document.body.setAttribute('data-page', pageId);
        
        // Hide confetti on subpages
        if (pageId === 'home') {{
          if (document.getElementById('confetti')) document.getElementById('confetti').style.display = 'block';
        }} else {{
          if (document.getElementById('confetti')) document.getElementById('confetti').style.display = 'none';
        }}

        // Re-trigger reveal animations
        document.querySelectorAll('#page-' + pageId + ' .reveal').forEach(el => el.classList.remove('visible'));
        observeReveals();

        document.body.classList.remove('page-out');
        document.body.classList.add('page-in');
      }}, 320);
    }}

    // Reveal Logic
    let currentObserver = null;
    function observeReveals() {{
      if (currentObserver) currentObserver.disconnect();
      currentObserver = new IntersectionObserver(entries => {{
        entries.forEach(en => {{ 
          if(en.isIntersecting){{ 
            en.target.classList.add('visible'); 
            currentObserver.unobserve(en.target); 
          }} 
        }});
      }}, {{ threshold: 0.1 }});
      
      const activeReveals = document.querySelectorAll('.page-section.active .reveal');
      activeReveals.forEach((el,i) => {{
        el.style.transitionDelay = (i*0.08)+'s';
        currentObserver.observe(el);
      }});
    }}
    
    // Initial observations
    observeReveals();
    
    // Fallback Image
    const heroImage = document.getElementById('heroImage');
    if (heroImage) {{
      heroImage.addEventListener('error', () => {{
        heroImage.src = `data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='800'><defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'><stop offset='0%25' stop-color='%23ffd2ea'/><stop offset='100%25' stop-color='%23cffff0'/></linearGradient></defs><rect width='1200' height='800' fill='url(%23g)'/><text x='600' y='400' text-anchor='middle' font-size='96' font-family='Verdana' fill='%2370264f'>Sweety Ice</text></svg>`;
      }}, {{ once: true }});
    }}
  </script>
</body>
</html>
"""

write_file('index.html', final_html)
print("Merge complete")

import streamlit.components.v1 as components
import json

def render_js_hero_header():
    """
    Renders an aesthetic JavaScript-powered interactive cyber-header with animated particle canvas,
    glowing badges, and interactive UX elements.
    """
    hero_html = """
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&family=Inter:wght@400;500&display=swap" rel="stylesheet">
      <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
          background: transparent;
          font-family: 'Outfit', -apple-system, sans-serif;
          overflow: hidden;
        }
        .hero-container {
          position: relative;
          background: linear-gradient(135deg, rgba(15, 23, 42, 0.85) 0%, rgba(30, 27, 75, 0.85) 50%, rgba(15, 23, 42, 0.9) 100%);
          border: 1px solid rgba(139, 92, 246, 0.3);
          border-radius: 20px;
          padding: 22px 32px;
          box-shadow: 0 10px 30px -10px rgba(99, 102, 241, 0.3), inset 0 1px 1px rgba(255, 255, 255, 0.1);
          overflow: hidden;
          display: flex;
          align-items: center;
          justify-content: space-between;
        }
        #particle-canvas {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          z-index: 1;
          pointer-events: none;
        }
        .hero-content {
          position: relative;
          z-index: 2;
          max-width: 65%;
        }
        .badge {
          display: inline-flex;
          align-items: center;
          gap: 8px;
          background: rgba(99, 102, 241, 0.15);
          border: 1px solid rgba(129, 140, 248, 0.4);
          padding: 6px 14px;
          border-radius: 9999px;
          font-size: 13px;
          font-weight: 600;
          color: #a5b4fc;
          letter-spacing: 0.5px;
          margin-bottom: 14px;
        }
        .pulse-dot {
          width: 8px;
          height: 8px;
          background: #34d399;
          border-radius: 50%;
          box-shadow: 0 0 10px #34d399;
          animation: pulse 1.8s infinite;
        }
        @keyframes pulse {
          0% { transform: scale(0.95); opacity: 0.8; }
          50% { transform: scale(1.3); opacity: 1; }
          100% { transform: scale(0.95); opacity: 0.8; }
        }
        h1 {
          font-size: 32px;
          font-weight: 800;
          color: #ffffff;
          letter-spacing: -0.5px;
          line-height: 1.2;
          background: linear-gradient(to right, #ffffff, #c7d2fe, #f0abfc);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          margin-bottom: 8px;
        }
        p {
          font-family: 'Inter', sans-serif;
          font-size: 15px;
          color: #94a3b8;
          line-height: 1.5;
        }
        .hero-stats {
          position: relative;
          z-index: 2;
          display: flex;
          gap: 16px;
        }
        .stat-card {
          background: rgba(255, 255, 255, 0.04);
          backdrop-filter: blur(10px);
          border: 1px solid rgba(255, 255, 255, 0.08);
          padding: 14px 20px;
          border-radius: 14px;
          text-align: center;
          transition: transform 0.3s ease, border-color 0.3s ease;
          cursor: pointer;
        }
        .stat-card:hover {
          transform: translateY(-3px);
          border-color: rgba(139, 92, 246, 0.6);
          background: rgba(255, 255, 255, 0.08);
        }
        .stat-num {
          font-size: 22px;
          font-weight: 800;
          color: #f8fafc;
          margin-bottom: 2px;
        }
        .stat-label {
          font-size: 11px;
          color: #94a3b8;
          text-transform: uppercase;
          letter-spacing: 0.8px;
          font-weight: 600;
        }
        @media (max-width: 768px) {
          .hero-container { flex-direction: column; align-items: flex-start; padding: 20px; }
          .hero-content { max-width: 100%; margin-bottom: 16px; }
          .hero-stats { width: 100%; justify-content: space-between; }
          h1 { font-size: 24px; }
        }
      </style>
    </head>
    <body>
      <div class="hero-container">
        <canvas id="particle-canvas"></canvas>
        <div class="hero-content">
          <div class="badge">
            <span class="pulse-dot"></span>
            META LLAMA 3.3 70B POWERED
          </div>
          <h1>AI Interview Coach & Career Mentor</h1>
          <p>Master technical & behavioral interviews with dynamic STAR guidance, anti-repetition intelligence, and instant multi-metric feedback.</p>
        </div>
        <div class="hero-stats">
          <div class="stat-card" onclick="triggerGlow(this)">
            <div class="stat-num">50ms</div>
            <div class="stat-label">Groq Latency</div>
          </div>
          <div class="stat-card" onclick="triggerGlow(this)">
            <div class="stat-num">100%</div>
            <div class="stat-label">Tailored Prep</div>
          </div>
          <div class="stat-card" onclick="triggerGlow(this)">
            <div class="stat-num">STAR</div>
            <div class="stat-label">AI Mentor</div>
          </div>
        </div>
      </div>

      <script>
        // Interactive JavaScript Particle Canvas
        const canvas = document.getElementById('particle-canvas');
        const ctx = canvas.getContext('2d');
        let width = canvas.width = canvas.offsetWidth;
        let height = canvas.height = canvas.offsetHeight;

        window.addEventListener('resize', () => {
          width = canvas.width = canvas.offsetWidth;
          height = canvas.height = canvas.offsetHeight;
        });

        const particles = [];
        const numParticles = 30;

        for (let i = 0; i < numParticles; i++) {
          particles.push({
            x: Math.random() * width,
            y: Math.random() * height,
            vx: (Math.random() - 0.5) * 0.8,
            vy: (Math.random() - 0.5) * 0.8,
            radius: Math.random() * 2 + 1,
            alpha: Math.random() * 0.5 + 0.2
          });
        }

        function animate() {
          ctx.clearRect(0, 0, width, height);

          for (let i = 0; i < numParticles; i++) {
            let p = particles[i];
            p.x += p.vx;
            p.y += p.vy;

            if (p.x < 0 || p.x > width) p.vx *= -1;
            if (p.y < 0 || p.y > height) p.vy *= -1;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(165, 180, 252, ${p.alpha})`;
            ctx.fill();

            for (let j = i + 1; j < numParticles; j++) {
              let p2 = particles[j];
              let dist = Math.hypot(p.x - p2.x, p.y - p2.y);
              if (dist < 100) {
                ctx.beginPath();
                ctx.moveTo(p.x, p.y);
                ctx.lineTo(p2.x, p2.y);
                ctx.strokeStyle = `rgba(139, 92, 246, ${0.15 * (1 - dist / 100)})`;
                ctx.lineWidth = 1;
                ctx.stroke();
              }
            }
          }
          requestAnimationFrame(animate);
        }
        animate();

        function triggerGlow(card) {
          card.style.transform = 'scale(1.06)';
          card.style.borderColor = '#c084fc';
          setTimeout(() => {
            card.style.transform = '';
            card.style.borderColor = '';
          }, 300);
        }
      </script>
    </body>
    </html>
    """
    components.html(hero_html, height=190)


def render_js_interview_timer():
    """
    Renders an aesthetic interactive JavaScript Interview Pace Timer inside Step 2.
    Candidates can time their response against recommended 2-minute STAR target.
    """
    timer_html = """
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;700&display=swap" rel="stylesheet">
      <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
          background: transparent;
          font-family: 'Outfit', sans-serif;
        }
        .timer-box {
          background: linear-gradient(135deg, rgba(15, 23, 42, 0.7) 0%, rgba(30, 41, 59, 0.7) 100%);
          border: 1px solid rgba(255, 255, 255, 0.08);
          border-radius: 14px;
          padding: 12px 20px;
          display: flex;
          align-items: center;
          justify-content: space-between;
          color: #f8fafc;
        }
        .timer-left {
          display: flex;
          align-items: center;
          gap: 12px;
        }
        .timer-display {
          font-size: 24px;
          font-weight: 700;
          color: #38bdf8;
          font-variant-numeric: tabular-nums;
        }
        .timer-label {
          font-size: 12px;
          color: #94a3b8;
          line-height: 1.2;
        }
        .timer-controls {
          display: flex;
          gap: 8px;
        }
        .btn {
          background: rgba(255, 255, 255, 0.06);
          border: 1px solid rgba(255, 255, 255, 0.15);
          color: #e2e8f0;
          padding: 6px 14px;
          border-radius: 8px;
          font-size: 13px;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s ease;
        }
        .btn:hover {
          background: rgba(56, 189, 248, 0.2);
          border-color: #38bdf8;
          color: #ffffff;
        }
        .btn-primary {
          background: linear-gradient(135deg, #4f46e5, #7c3aed);
          border: none;
        }
        .btn-primary:hover {
          background: linear-gradient(135deg, #4338ca, #6d28d9);
        }
      </style>
    </head>
    <body>
      <div class="timer-box">
        <div class="timer-left">
          <div class="timer-display" id="display">02:00</div>
          <div class="timer-label">⏱️ STAR Target Pace<br>Recommended Response Time</div>
        </div>
        <div class="timer-controls">
          <button class="btn btn-primary" id="startBtn" onclick="toggleTimer()">Start Pace Timer</button>
          <button class="btn" onclick="resetTimer()">Reset</button>
        </div>
      </div>

      <script>
        let totalSeconds = 120;
        let currentSeconds = totalSeconds;
        let interval = null;
        let running = false;

        function updateDisplay() {
          const mins = Math.floor(currentSeconds / 60).toString().padStart(2, '0');
          const secs = (currentSeconds % 60).toString().padStart(2, '0');
          const disp = document.getElementById('display');
          disp.innerText = `${mins}:${secs}`;
          if (currentSeconds <= 30) {
            disp.style.color = '#f87171';
          } else {
            disp.style.color = '#38bdf8';
          }
        }

        function toggleTimer() {
          const btn = document.getElementById('startBtn');
          if (!running) {
            running = true;
            btn.innerText = 'Pause';
            interval = setInterval(() => {
              if (currentSeconds > 0) {
                currentSeconds--;
                updateDisplay();
              } else {
                clearInterval(interval);
                running = false;
                btn.innerText = 'Start Pace Timer';
              }
            }, 1000);
          } else {
            running = false;
            clearInterval(interval);
            btn.innerText = 'Resume';
          }
        }

        function resetTimer() {
          running = false;
          clearInterval(interval);
          currentSeconds = totalSeconds;
          document.getElementById('startBtn').innerText = 'Start Pace Timer';
          updateDisplay();
        }
      </script>
    </body>
    </html>
    """
    components.html(timer_html, height=75)


def render_js_radar_chart(evaluations):
    """
    Renders an aesthetic interactive JavaScript Chart.js visualizer for Step 5 final report scores.
    """
    if not evaluations:
        return
        
    # Calculate average scores across all answered questions
    avg_scores = {
        "Overall": 0.0,
        "Relevance": 0.0,
        "Structure": 0.0,
        "Depth": 0.0,
        "Communication": 0.0
    }
    
    count = len(evaluations)
    for idx, eval_data in evaluations.items():
        scores = eval_data.get("scores", {})
        for k in avg_scores.keys():
            avg_scores[k] += float(scores.get(k.lower(), 0))
            
    for k in avg_scores.keys():
        avg_scores[k] = round(avg_scores[k] / count, 1) if count > 0 else 0
        
    labels = list(avg_scores.keys())
    values = list(avg_scores.values())
    
    chart_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
      <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@600&display=swap" rel="stylesheet">
      <style>
        body {{
          background: transparent;
          font-family: 'Outfit', sans-serif;
          display: flex;
          justify-content: center;
          align-items: center;
          margin: 0;
          padding: 10px;
        }}
        .chart-card {{
          background: rgba(15, 23, 42, 0.7);
          border: 1px solid rgba(139, 92, 246, 0.3);
          border-radius: 16px;
          padding: 20px;
          width: 100%;
          max-width: 600px;
          box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        }}
      </style>
    </head>
    <body>
      <div class="chart-card">
        <canvas id="scoreChart" height="230"></canvas>
      </div>

      <script>
        const ctx = document.getElementById('scoreChart').getContext('2d');
        const gradient = ctx.createLinearGradient(0, 0, 0, 230);
        gradient.addColorStop(0, 'rgba(139, 92, 246, 0.85)');
        gradient.addColorStop(1, 'rgba(6, 182, 212, 0.4)');

        new Chart(ctx, {{
          type: 'bar',
          data: {{
            labels: {json.dumps(labels)},
            datasets: [{{
              label: 'Average Score (out of 10)',
              data: {json.dumps(values)},
              backgroundColor: gradient,
              borderColor: '#c084fc',
              borderWidth: 1.5,
              borderRadius: 8
            }}]
          }},
          options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
              legend: {{
                labels: {{ color: '#e2e8f0', font: {{ family: 'Outfit', size: 13 }} }}
              }}
            }},
            scales: {{
              y: {{
                min: 0,
                max: 10,
                grid: {{ color: 'rgba(255, 255, 255, 0.08)' }},
                ticks: {{ color: '#94a3b8', font: {{ family: 'Outfit' }} }}
              }},
              x: {{
                grid: {{ display: false }},
                ticks: {{ color: '#f8fafc', font: {{ family: 'Outfit', size: 12, weight: '600' }} }}
              }}
            }}
          }}
        }});
      </script>
    </body>
    </html>
    """
    components.html(chart_html, height=290)

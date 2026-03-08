import json
import os

HTML_DIR = "/Users/ketanpillai/Documents/Major_Project_3rd_review.html"
ASSETS_DIR = os.path.join(HTML_DIR, "assets")
HEADER_JSON = os.path.join(ASSETS_DIR, "header.json")

with open(HEADER_JSON, "r") as f:
    header = json.load(f)

slide_list = header["slideList"]

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Major Project Presentation</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
        
        body {
            font-family: 'Inter', sans-serif;
            background-color: #050505;
            color: #fff;
            overflow-x: hidden;
            margin: 0;
            padding: 0;
            /* Smooth scrolling */
            scroll-behavior: smooth;
        }

        .slide-container {
            position: relative;
            width: 100vw;
            height: 100vh;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .slide-layer {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
            object-position: center;
            will-change: transform, opacity;
        }

        .layer-0 {
            /* Background layer defaults */
            z-index: 10;
        }

        .layer-1 {
            /* Foreground layer defaults */
            z-index: 20;
        }

        /* Modern UI Elements */
        #progress-bar {
            position: fixed;
            top: 0;
            left: 0;
            height: 4px;
            background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899);
            width: 0%;
            z-index: 100;
            box-shadow: 0 0 10px rgba(236, 72, 153, 0.5);
        }

        .slide-indicator {
            position: fixed;
            right: 20px;
            top: 50%;
            transform: translateY(-50%);
            display: flex;
            flex-direction: column;
            gap: 10px;
            z-index: 50;
        }

        .indicator-dot {
            width: 8px;
            height: 8px;
            background-color: rgba(255, 255, 255, 0.2);
            border-radius: 50%;
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .indicator-dot.active {
            background-color: #ec4899;
            box-shadow: 0 0 10px #ec4899;
            transform: scale(1.5);
        }

        /* Ambient glowing background */
        .ambient-glow {
            position: absolute;
            width: 60vw;
            height: 60vh;
            background: radial-gradient(circle, rgba(139, 92, 246, 0.15) 0%, rgba(5, 5, 5, 0) 70%);
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 1;
            pointer-events: none;
        }
    </style>
</head>
<body>

    <div id="progress-bar"></div>
    <div class="slide-indicator" id="indicator-container"></div>

    <main id="presentation-main">
"""

for i, slide_id in enumerate(slide_list):
    slide_dir = os.path.join("assets", slide_id, "assets")
    layer_0 = os.path.join(slide_dir, "layer_0.png")
    layer_1 = os.path.join(slide_dir, "layer_1.png")
    
    html_content += f"""
        <section class="slide-container" id="slide-{i}">
            <div class="ambient-glow"></div>
            <!-- Background Layer -->
    """
    
    if os.path.exists(os.path.join(HTML_DIR, layer_0)):
        html_content += f'<img src="{layer_0}" class="slide-layer layer-0" data-depth="0.2" alt="Slide {i+1} Background">\n'
        
    if os.path.exists(os.path.join(HTML_DIR, layer_1)):
        html_content += f'            <!-- Content Layer -->\n'
        html_content += f'            <img src="{layer_1}" class="slide-layer layer-1" data-depth="0.8" alt="Slide {i+1} Content">\n'
        
    html_content += """
        </section>
    """

html_content += """
    </main>

    <!-- GSAP & ScrollTrigger -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
    
    <script>
        gsap.registerPlugin(ScrollTrigger);

        // Progress bar animation
        gsap.to("#progress-bar", {
            width: "100%",
            ease: "none",
            scrollTrigger: {
                trigger: "body",
                start: "top top",
                end: "bottom bottom",
                scrub: 0.3
            }
        });

        const slides = gsap.utils.toArray('.slide-container');
        const indicatorContainer = document.getElementById('indicator-container');

        slides.forEach((slide, i) => {
            // Create indicator dot
            const dot = document.createElement('div');
            dot.className = 'indicator-dot';
            dot.addEventListener('click', () => {
                window.scrollTo({
                    top: slide.offsetTop,
                    behavior: 'smooth'
                });
            });
            indicatorContainer.appendChild(dot);

            // Set active dot on scroll
            ScrollTrigger.create({
                trigger: slide,
                start: "top center",
                end: "bottom center",
                onToggle: self => {
                    if (self.isActive) {
                        document.querySelectorAll('.indicator-dot').forEach((d, index) => {
                            if (index === i) d.classList.add('active');
                            else d.classList.remove('active');
                        });
                    }
                }
            });

            // --- ANIMATIONS ---

            const bgLayer = slide.querySelector('.layer-0');
            const contentLayer = slide.querySelector('.layer-1');
            const glow = slide.querySelector('.ambient-glow');

            // 1. Initial State for entrance animations
            if (bgLayer) gsap.set(bgLayer, { scale: 1.1, opacity: 0 });
            if (contentLayer) gsap.set(contentLayer, { y: 100, opacity: 0, scale: 0.95 });
            if (glow) gsap.set(glow, { scale: 0.8, opacity: 0 });

            // 2. Entrance Animation Timeline using ScrollTrigger
            const tl = gsap.timeline({
                scrollTrigger: {
                    trigger: slide,
                    start: "top 80%", // trigger when slide reaches 80% of viewport
                    end: "top 20%",
                    scrub: false,
                    toggleActions: "play reverse play reverse"
                }
            });

            if (bgLayer) {
                tl.to(bgLayer, {
                    scale: 1,
                    opacity: 1,
                    duration: 1.2,
                    ease: "power2.out"
                }, 0);
            }

            if (glow) {
                tl.to(glow, {
                    scale: 1,
                    opacity: 1,
                    duration: 1.5,
                    ease: "power1.inOut"
                }, 0.2);
            }

            if (contentLayer) {
                tl.to(contentLayer, {
                    y: 0,
                    opacity: 1,
                    scale: 1,
                    duration: 1,
                    ease: "back.out(1.2)"
                }, 0.4);
            }
            
            // 3. Parallax effect during scroll using Scrub
            if (bgLayer) {
                gsap.to(bgLayer, {
                    y: "20%",
                    ease: "none",
                    scrollTrigger: {
                        trigger: slide,
                        start: "top bottom",
                        end: "bottom top",
                        scrub: true
                    }
                });
            }

            if (contentLayer) {
                gsap.to(contentLayer, {
                    y: "-15%",
                    ease: "none",
                    scrollTrigger: {
                        trigger: slide,
                        start: "top bottom",
                        end: "bottom top",
                        scrub: true
                    }
                });
            }
        });
        
        // Initialize first dot as active
        if(indicatorContainer.firstChild) {
            indicatorContainer.firstChild.classList.add('active');
        }
    </script>
</body>
</html>
"""

with open(os.path.join(HTML_DIR, "index.html"), "w") as f:
    f.write(html_content)

print("Generated index.html successfully.")

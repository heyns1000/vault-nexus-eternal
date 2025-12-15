# 3D AtomMode Dashboard Guide

## Overview

The AtomMode Integrated Dashboard provides real-time 3D visualization of the Vault Nexus Eternal ecosystem using Three.js.

## Features

### 1. 40D Hypercube Wireframe

Rotating 3D projection of the 40-dimensional hypercube:

```javascript
// Five nested cubes represent dimension projections
sizes = [60, 50, 40, 30, 20]
colors = [#4fc3f7, #64b5f6, #90caf9, #bbdefb, #e3f2fd]

// Each cube rotates at slightly different rates
cube[i].rotation.x += i * 0.002
```

### 2. Brand Particle Cloud

13,713 particles representing individual brands:

```javascript
// Spherical distribution
radius = 100 + random() * 50
theta = random() * π * 2
phi = acos(random() * 2 - 1)

// Blue color gradient
hsl(0.55 + random() * 0.1, 0.8, 0.5 + random() * 0.3)
```

### 3. Real-Time Metrics

Six metric cards displaying live stats:

- **40D Hypercube**: Total brands stored
- **CARE-15 Pool**: Accumulated redistribution funds
- **Memories**: ELEPHANT_MEMORY count
- **Query Latency**: Average response time
- **Breath Cycles**: Number of complete cycles
- **Free Capacity**: Available storage space

### 4. Breath Timer

Circular countdown displaying:
- Current phase (PULSE/GLOW/TRADE/FLOW/RESET)
- Seconds remaining in 9s cycle
- Visual pulse animation

### 5. Rossouw Node Widget

Embedded iframe showing:
- Ghost Gap calculation
- Collapse Lock protocol
- Signal ping counter
- Phase progress

### 6. Interactive Controls

Four control buttons:
- **Auto-Rotate**: Toggle automatic rotation
- **Particles**: Show/hide brand cloud
- **Wireframe**: Show/hide hypercube
- **Reset View**: Return camera to origin

## Usage

### Opening the Dashboard

```bash
# Method 1: Direct file
open atommode-integrated-dashboard.html

# Method 2: Serve via HTTP (recommended)
python -m http.server 8080
# Then open: http://localhost:8080/atommode-integrated-dashboard.html
```

### WebSocket Connection

Dashboard automatically connects to:
```
ws://localhost:8000/ws/realtime
```

Ensure API server is running:
```bash
python main.py
```

### Camera Controls

**Mouse:**
- Click + Drag: Manual rotation (disables auto-rotate)
- Scroll: Zoom in/out

**Keyboard:**
- Arrow keys: Pan view
- R: Reset view
- Space: Toggle auto-rotate

### Toggling Rossouw Widget

Click the **−** button to minimize/restore the widget.

## Customization

### Colors

```javascript
// Edit color scheme in <style> section
--primary-color: #4fc3f7;
--secondary-color: #64b5f6;
--background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 50%, #0a0e27 100%);
```

### Particle Count

```javascript
// Edit in createParticles()
const particleCount = 13713;  // Increase for denser cloud
```

### Rotation Speed

```javascript
// Edit in animate()
hypercube.rotation.x += 0.002;  // Slower: decrease value
hypercube.rotation.y += 0.003;
```

### Metric Update Frequency

```javascript
// Edit in fetchStats()
setTimeout(fetchStats, 3000);  // Update every 3s
```

## Performance

### Recommended Specs

- Modern browser (Chrome 90+, Firefox 88+, Safari 14+)
- WebGL support required
- 4GB RAM minimum
- GPU acceleration recommended

### FPS Optimization

```javascript
// Reduce particle count for low-end devices
if (navigator.hardwareConcurrency < 4) {
    const particleCount = 5000;  // Reduced
}

// Lower rendering quality
renderer.setPixelRatio(1);  // Instead of window.devicePixelRatio
```

### Mobile Support

Dashboard is responsive but best experienced on desktop. Mobile optimizations:

```css
@media (max-width: 768px) {
    .metrics-grid {
        grid-template-columns: 1fr;  /* Stack vertically */
    }
    .rossouw-widget {
        display: none;  /* Hide on mobile */
    }
}
```

## Troubleshooting

### WebSocket Not Connecting

```javascript
// Check console for errors
// Fallback to polling if WebSocket fails
if (ws.readyState !== WebSocket.OPEN) {
    setInterval(() => {
        fetch('http://localhost:8000/api/v1/stats')
            .then(res => res.json())
            .then(updateMetrics);
    }, 3000);
}
```

### Three.js Not Loading

```html
<!-- Use local copy instead of CDN -->
<script src="lib/three.min.js"></script>
```

### CORS Issues

```bash
# Serve dashboard from same origin as API
python -m http.server 8000 --directory ./
```

## Extensions

### Add New Metric Card

```html
<div class="metric-card">
    <div class="metric-label">Your Metric</div>
    <div class="metric-value">
        <span id="your-metric">0</span>
        <span class="metric-unit">units</span>
    </div>
</div>
```

```javascript
// Update in updateMetrics()
document.getElementById('your-metric').textContent = data.yourValue;
```

### Custom Visualization

```javascript
// Add to scene
const geometry = new THREE.TorusGeometry(40, 10, 16, 100);
const material = new THREE.MeshBasicMaterial({ color: 0x4fc3f7 });
const torus = new THREE.Mesh(geometry, material);
scene.add(torus);
```

---

**Technology**: Three.js + WebSocket  
**Features**: 3D visualization + Real-time metrics  
**Status**: FULLY OPERATIONAL  
**URL**: atommode-integrated-dashboard.html

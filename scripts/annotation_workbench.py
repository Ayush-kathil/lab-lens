import os
import glob
import json
from flask import Flask, render_template_string, request, jsonify, send_from_directory

app = Flask(__name__)
DATASET_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Dataset", "SpatialComplianceReal"))
IMAGES_DIR = os.path.join(DATASET_DIR, "images")
ANNOTATIONS_DIR = os.path.join(DATASET_DIR, "annotations")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Real-World Annotation Workbench</title>
    <style>
        body { font-family: sans-serif; display: flex; margin: 0; padding: 20px; }
        #sidebar { width: 300px; padding-right: 20px; border-right: 1px solid #ccc; max-height: 90vh; overflow-y: auto;}
        #main { flex-grow: 1; padding-left: 20px; }
        .sample-item { cursor: pointer; padding: 5px; border: 1px solid transparent; }
        .sample-item:hover { background: #eee; }
        .sample-item.active { border-color: #999; background: #e0e0e0; }
        .status-NEEDS_REVIEW { color: red; }
        .status-HUMAN_VERIFIED { color: green; }
        canvas { border: 1px solid #333; cursor: crosshair; }
        .form-group { margin-bottom: 10px; }
        label { display: block; font-weight: bold; }
        input, select, textarea { width: 100%; padding: 5px; }
        button { padding: 10px; margin-top: 10px; cursor: pointer; }
        .box-list-item { display: flex; justify-content: space-between; margin-bottom: 5px; border: 1px solid #ddd; padding: 5px;}
    </style>
</head>
<body>
    <div id="sidebar">
        <h3>Samples</h3>
        <div id="sample-list"></div>
    </div>
    <div id="main">
        <h2 id="current-sample">Select a sample</h2>
        <div style="display: flex;">
            <div>
                <canvas id="image-canvas" width="600" height="600"></canvas>
            </div>
            <div style="margin-left: 20px; width: 400px; max-height: 90vh; overflow-y: auto;">
                <div class="form-group">
                    <label>Annotation Status</label>
                    <select id="annotation-status">
                        <option value="NEEDS_REVIEW">NEEDS_REVIEW</option>
                        <option value="HUMAN_VERIFIED">HUMAN_VERIFIED</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Compliant (Ground Truth)</label>
                    <select id="ground-truth-compliant">
                        <option value="null">Unreviewed (null)</option>
                        <option value="true">True</option>
                        <option value="false">False</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Setup Name</label>
                    <input type="text" id="setup-name" />
                </div>
                
                <hr />
                <h3>Objects</h3>
                <div class="form-group">
                    <label>New Object Class (Draw box to add)</label>
                    <input type="text" id="new-class-name" placeholder="e.g. beaker, flask..." />
                </div>
                <div id="objects-list"></div>

                <button onclick="saveAnnotation()">Save Annotation</button>
            </div>
        </div>
    </div>

    <script>
        let samples = [];
        let currentSampleId = null;
        let currentData = null;
        let imgObj = null;
        let isDrawing = false;
        let startX, startY;

        const canvas = document.getElementById('image-canvas');
        const ctx = canvas.getContext('2d');

        // Fetch samples
        fetch('/api/samples')
            .then(r => r.json())
            .then(data => {
                samples = data;
                renderSampleList();
            });

        function renderSampleList() {
            const list = document.getElementById('sample-list');
            list.innerHTML = '';
            samples.forEach(s => {
                const div = document.createElement('div');
                div.className = `sample-item ${s.id === currentSampleId ? 'active' : ''}`;
                div.innerHTML = `<strong>${s.id}</strong> <span class="status-${s.status}">[${s.status}]</span>`;
                div.onclick = () => loadSample(s.id);
                list.appendChild(div);
            });
        }

        function loadSample(sampleId) {
            currentSampleId = sampleId;
            renderSampleList();
            document.getElementById('current-sample').innerText = sampleId;

            fetch(`/api/samples/${sampleId}`)
                .then(r => r.json())
                .then(data => {
                    currentData = data;
                    document.getElementById('annotation-status').value = data.annotation_status;
                    document.getElementById('ground-truth-compliant').value = data.ground_truth.compliant === null ? 'null' : data.ground_truth.compliant.toString();
                    document.getElementById('setup-name').value = data.setup_specification.setup_name || '';

                    imgObj = new Image();
                    imgObj.src = `/images/${data.image_metadata.filename}`;
                    imgObj.onload = () => {
                        // resize canvas to fit image while maintaining aspect ratio
                        const maxW = 600, maxH = 600;
                        let w = imgObj.width, h = imgObj.height;
                        if (w > maxW) { h = (h * maxW) / w; w = maxW; }
                        if (h > maxH) { w = (w * maxH) / h; h = maxH; }
                        canvas.width = w;
                        canvas.height = h;
                        draw();
                    };
                    renderObjects();
                });
        }

        function renderObjects() {
            const list = document.getElementById('objects-list');
            list.innerHTML = '';
            if (currentData && currentData.objects) {
                currentData.objects.forEach((obj, idx) => {
                    const div = document.createElement('div');
                    div.className = 'box-list-item';
                    div.innerHTML = `
                        <div>
                            <strong>${obj.class_name}</strong> (ID: ${obj.object_id})<br/>
                            <small>[${obj.bbox.map(n => n.toFixed(2)).join(', ')}]</small>
                        </div>
                        <button onclick="removeObject(${idx})">X</button>
                    `;
                    list.appendChild(div);
                });
            }
        }

        function removeObject(idx) {
            currentData.objects.splice(idx, 1);
            renderObjects();
            draw();
        }

        function draw() {
            if (!imgObj) return;
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(imgObj, 0, 0, canvas.width, canvas.height);
            
            if (currentData && currentData.objects) {
                currentData.objects.forEach(obj => {
                    const [x1, y1, x2, y2] = obj.bbox;
                    ctx.strokeStyle = 'red';
                    ctx.lineWidth = 2;
                    ctx.strokeRect(x1 * canvas.width, y1 * canvas.height, (x2 - x1) * canvas.width, (y2 - y1) * canvas.height);
                    ctx.fillStyle = 'red';
                    ctx.fillText(obj.class_name, x1 * canvas.width, y1 * canvas.height > 10 ? y1 * canvas.height - 5 : 10);
                });
            }
        }

        canvas.onmousedown = (e) => {
            isDrawing = true;
            const rect = canvas.getBoundingClientRect();
            startX = e.clientX - rect.left;
            startY = e.clientY - rect.top;
        };

        canvas.onmousemove = (e) => {
            if (!isDrawing) return;
            draw();
            const rect = canvas.getBoundingClientRect();
            const currentX = e.clientX - rect.left;
            const currentY = e.clientY - rect.top;
            ctx.strokeStyle = 'blue';
            ctx.lineWidth = 2;
            ctx.strokeRect(startX, startY, currentX - startX, currentY - startY);
        };

        canvas.onmouseup = (e) => {
            if (!isDrawing) return;
            isDrawing = false;
            const rect = canvas.getBoundingClientRect();
            const endX = e.clientX - rect.left;
            const endY = e.clientY - rect.top;
            
            const x1 = Math.min(startX, endX) / canvas.width;
            const y1 = Math.min(startY, endY) / canvas.height;
            const x2 = Math.max(startX, endX) / canvas.width;
            const y2 = Math.max(startY, endY) / canvas.height;
            
            // Only add if it's a real box
            if (x2 - x1 > 0.01 && y2 - y1 > 0.01) {
                let cls = document.getElementById('new-class-name').value || 'object';
                if (!currentData.objects) currentData.objects = [];
                currentData.objects.push({
                    object_id: cls + '_' + Date.now(),
                    class_name: cls,
                    bbox: [x1, y1, x2, y2]
                });
                renderObjects();
            }
            draw();
        };

        function saveAnnotation() {
            if (!currentData) return;
            currentData.annotation_status = document.getElementById('annotation-status').value;
            const compVal = document.getElementById('ground-truth-compliant').value;
            currentData.ground_truth.compliant = compVal === 'null' ? null : (compVal === 'true');
            currentData.setup_specification.setup_name = document.getElementById('setup-name').value;

            fetch(`/api/samples/${currentSampleId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(currentData)
            })
            .then(r => r.json())
            .then(res => {
                if (res.success) {
                    alert('Saved!');
                    // Update sample list status
                    const s = samples.find(x => x.id === currentSampleId);
                    if(s) s.status = currentData.annotation_status;
                    renderSampleList();
                } else {
                    alert('Error saving');
                }
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(IMAGES_DIR, filename)

@app.route('/api/samples')
def list_samples():
    files = glob.glob(os.path.join(ANNOTATIONS_DIR, '*.json'))
    samples = []
    for f in sorted(files):
        with open(f, 'r', encoding='utf-8') as file:
            data = json.load(file)
            samples.append({
                'id': data['sample_id'],
                'status': data['annotation_status']
            })
    return jsonify(samples)

@app.route('/api/samples/<sample_id>')
def get_sample(sample_id):
    path = os.path.join(ANNOTATIONS_DIR, f"{sample_id}.json")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify({"error": "not found"}), 404

@app.route('/api/samples/<sample_id>', methods=['POST'])
def save_sample(sample_id):
    data = request.json
    path = os.path.join(ANNOTATIONS_DIR, f"{sample_id}.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    return jsonify({"success": True})

if __name__ == '__main__':
    print("Starting Annotation Workbench on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)

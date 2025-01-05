// Initialize Three.js scene
let scene, camera, renderer, controls;
let environment = null;

function initViewer() {
    // Create scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0xf0f0f0);

    // Create camera
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 5;

    // Create renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(document.getElementById('viewer').clientWidth, document.getElementById('viewer').clientHeight);
    document.getElementById('viewer').appendChild(renderer.domElement);

    // Add controls
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;

    // Add ambient light
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);

    // Add directional light
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
    directionalLight.position.set(0, 1, 0);
    scene.add(directionalLight);

    // Animation loop
    function animate() {
        requestAnimationFrame(animate);
        controls.update();
        renderer.render(scene, camera);
    }
    animate();

    // Handle window resize
    window.addEventListener('resize', onWindowResize, false);
}

function onWindowResize() {
    const container = document.getElementById('viewer');
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
}

// Handle file input
document.getElementById('imageInput').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('preview').src = e.target.result;
            document.getElementById('imagePreview').classList.remove('hidden');
            document.getElementById('generateBtn').disabled = false;
        };
        reader.readAsDataURL(file);
    }
});

// Handle generate button
document.getElementById('generateBtn').addEventListener('click', async function() {
    const file = document.getElementById('imageInput').files[0];
    if (!file) return;

    updateStatus('Generating environment...');
    const formData = new FormData();
    formData.append('image', file);

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) throw new Error('Generation failed');
        
        const data = await response.json();
        environment = data.environment;
        
        // Update 3D viewer with generated environment
        updateEnvironmentView(environment);
        
        document.getElementById('exploreBtn').disabled = false;
        updateStatus('Environment generated successfully!');
    } catch (error) {
        updateStatus('Error: ' + error.message);
    }
});

// Handle explore button
document.getElementById('exploreBtn').addEventListener('click', async function() {
    if (!environment) return;

    updateStatus('Starting exploration...');
    try {
        const response = await fetch('/explore', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                environment_id: environment.id
            })
        });
        
        if (!response.ok) throw new Error('Exploration failed');
        
        const data = await response.json();
        
        // Update 3D viewer with exploration results
        updateExplorationView(data.trajectory);
        
        document.getElementById('mapBtn').disabled = false;
        updateStatus('Exploration completed successfully!');
    } catch (error) {
        updateStatus('Error: ' + error.message);
    }
});

// Handle map button
document.getElementById('mapBtn').addEventListener('click', async function() {
    if (!environment) return;

    updateStatus('Generating map...');
    try {
        const response = await fetch('/map', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                environment_id: environment.id,
                exploration_data: environment.exploration_data
            })
        });
        
        if (!response.ok) throw new Error('Map generation failed');
        
        const data = await response.json();
        
        // Update 3D viewer with map
        updateMapView(data.map);
        
        updateStatus('Map generated successfully!');
    } catch (error) {
        updateStatus('Error: ' + error.message);
    }
});

function updateStatus(message) {
    document.getElementById('status').textContent = message;
}

function updateEnvironmentView(environment) {
    // TODO: Implement environment visualization
    console.log('Updating environment view:', environment);
}

function updateExplorationView(trajectory) {
    // TODO: Implement trajectory visualization
    console.log('Updating exploration view:', trajectory);
}

function updateMapView(map) {
    // TODO: Implement map visualization
    console.log('Updating map view:', map);
}

// Initialize viewer on page load
initViewer();

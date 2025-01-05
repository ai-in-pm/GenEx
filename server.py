from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn
from pathlib import Path
import numpy as np
from PIL import Image
import io
import json
from typing import Dict, Optional

from core.environment.environment_generator import EnvironmentGenerator
from agents.exploration.exploration_agent import ExplorationAgent
from tasks.mapping_task import MappingTask

app = FastAPI(title="GenEx - Generative Environment Explorer")

# Load configuration
config = {
    "model_paths": {
        "panorama_generator": "models/panorama_generator.pt",
        "depth_estimator": "models/depth_estimator.pt",
        "policy_network": "models/policy_network.pt"
    },
    "device": "cuda" if torch.cuda.is_available() else "cpu"
}

# Initialize components
env_generator = EnvironmentGenerator(config)
exploration_agent = ExplorationAgent(config)
mapping_task = MappingTask(config)

@app.post("/generate")
async def generate_environment(image: UploadFile = File(...)):
    """Generate a 3D environment from an input image."""
    try:
        contents = await image.read()
        pil_image = Image.open(io.BytesIO(contents))
        input_array = np.array(pil_image)
        
        # Generate environment
        environment = env_generator.generate_environment(input_array)
        
        return JSONResponse(content={"status": "success", "environment": environment})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/explore")
async def explore_environment(environment_id: str, goal: Optional[Dict] = None):
    """Explore a generated environment."""
    try:
        # Load environment
        environment = env_generator.load_environment(Path(f"environments/{environment_id}"))
        
        # Start exploration
        trajectory = exploration_agent.explore(environment, goal)
        
        return JSONResponse(content={"status": "success", "trajectory": trajectory})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/map")
async def create_map(environment_id: str, exploration_data: List[Dict]):
    """Create a 3D map from exploration data."""
    try:
        # Generate map
        map_data = mapping_task.create_map(exploration_data)
        
        return JSONResponse(content={"status": "success", "map": map_data})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files for web interface
app.mount("/", StaticFiles(directory="ui", html=True), name="ui")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

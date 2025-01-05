import pytest
import numpy as np
from pathlib import Path
from core.environment.environment_generator import EnvironmentGenerator

@pytest.fixture
def config():
    return {
        "model_paths": {
            "panorama_generator": "models/panorama_generator.pt",
            "depth_estimator": "models/depth_estimator.pt"
        },
        "device": "cpu"
    }

@pytest.fixture
def generator(config):
    return EnvironmentGenerator(config)

@pytest.fixture
def sample_image():
    # Create a simple test image
    return np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)

def test_environment_generator_initialization(generator):
    assert generator is not None
    assert generator.config is not None
    assert generator.device is not None

def test_generate_environment(generator, sample_image):
    # Test environment generation
    environment = generator.generate_environment(sample_image)
    
    # Check that all required components are present
    assert "panorama" in environment
    assert "depth_map" in environment
    assert "physics_data" in environment
    assert "navigation_map" in environment
    
    # Check data shapes and types
    assert isinstance(environment["panorama"], np.ndarray)
    assert isinstance(environment["depth_map"], np.ndarray)
    assert isinstance(environment["physics_data"], dict)
    assert isinstance(environment["navigation_map"], dict)

def test_save_and_load_environment(generator, sample_image, tmp_path):
    # Generate and save environment
    environment = generator.generate_environment(sample_image)
    save_path = tmp_path / "test_environment"
    generator.save_environment(save_path)
    
    # Load environment and verify
    loaded_environment = generator.load_environment(save_path)
    assert np.array_equal(environment["panorama"], loaded_environment["panorama"])
    assert np.array_equal(environment["depth_map"], loaded_environment["depth_map"])
    assert environment["physics_data"] == loaded_environment["physics_data"]
    assert environment["navigation_map"] == loaded_environment["navigation_map"]

def test_environment_update(generator, sample_image):
    # Generate initial environment
    environment = generator.generate_environment(sample_image)
    
    # Create a test action
    action = {
        "type": "move",
        "direction": np.array([1.0, 0.0, 0.0]),
        "magnitude": 1.0
    }
    
    # Update environment
    updated_environment = generator.update_environment(environment, action)
    
    # Verify update effects
    assert not np.array_equal(environment["panorama"], updated_environment["panorama"])
    assert not np.array_equal(environment["depth_map"], updated_environment["depth_map"])

def test_invalid_input(generator):
    # Test with invalid image shape
    with pytest.raises(ValueError):
        invalid_image = np.random.randint(0, 255, (100, 100), dtype=np.uint8)  # Missing color channel
        generator.generate_environment(invalid_image)
    
    # Test with invalid image type
    with pytest.raises(TypeError):
        invalid_image = "not an image"
        generator.generate_environment(invalid_image)

def test_physics_constraints(generator, sample_image):
    environment = generator.generate_environment(sample_image)
    physics_data = environment["physics_data"]
    
    # Verify physics data contains required components
    assert "collision_map" in physics_data
    assert "material_properties" in physics_data
    assert "gravity" in physics_data
    
    # Verify physics properties are within reasonable bounds
    assert physics_data["gravity"] == pytest.approx(-9.81, rel=1e-2)
    assert all(0 <= prop <= 1 for prop in physics_data["material_properties"].values())

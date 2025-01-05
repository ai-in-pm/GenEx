# GenEx: Generative 3D Environment Exploration System

A system for generative exploration of imaginative 3D environments from minimal input data, integrating Generative AI with embodied agents.

The development of this GitHub Repository was inspired by the "GenEx: Generating an Explorable World" Paper. To read the entire paper, visit https://arxiv.org/pdf/2412.09624v1

## Features

- Single RGB image to 3D environment conversion
- Physics-based environment generation using Unreal Engine
- Interactive and GPT-assisted exploration modes
- Multi-agent coordination and spatial reasoning
- Imagination-augmented policy for decision making
- Spherical consistency for seamless 360° navigation

## Prerequisites

- Python 3.9 or higher
- CUDA-capable GPU (recommended for optimal performance)
- Unreal Engine 5.1 or higher
- OpenAI API key (for GPT integration)
- Anthropic API key (for Claude integration)
- Mistral API key
- Groq API key
- Gemini API key
- At least 16GB RAM
- 50GB free disk space
- Windows 10/11 or Linux (Ubuntu 20.04 or higher)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/GenEx.git
cd GenEx
```

2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and configure your environment variables:
```bash
cp .env.example .env
```

## Project Structure

```
GenEx/
├── core/               # Core system components
│   ├── environment/    # Environment generation and physics
│   ├── perception/     # Image processing and 3D reconstruction
│   └── utils/         # Utility functions
├── agents/            # Agent implementations
│   ├── exploration/   # Exploration policies
│   └── reasoning/     # Spatial reasoning modules
├── tasks/             # Task-specific implementations
├── benchmarks/        # Performance evaluation
├── tests/             # Unit and integration tests
├── docs/              # Documentation
└── ui/                # User interface
```

## Usage

1. Start the server:
```bash
python -m genex.server
```

2. Access the web interface at `http://localhost:8000`

## Contributing

1. Fork the repository
2. Create your feature branch
3. Submit a pull request

## License

MIT License

## Citation

If you use this code in your research, please cite:
```
@software{genex2025,
  title={GenEx: Generative 3D Environment Exploration System},
  year={2025},
  url={https://github.com/yourusername/GenEx}
}
```

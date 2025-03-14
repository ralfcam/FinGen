# FinGen

A financial data visualization and analysis application built with Plotly Dash.

## Features

- Interactive financial data visualization
- Real-time data processing
- Responsive design with Bootstrap components
- Client-side optimizations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/FinGen.git
cd FinGen
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the development server:
```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:8050`

## Project Structure

```
├── assets/
│   └── clientside.js    # Client-side callback functions
├── pages/
│   ├── __init__.py
│   ├── tests/          # Test suite
│   ├── utils.py        # Utility functions
│   └── callbacks.py    # Dash callback handlers
├── layout.py           # UI layout components
└── callback_functions.py  # Core callback implementations
```

## Testing

Run the test suite:
```bash
pytest pages/tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
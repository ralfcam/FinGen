# FinGen - Financial Dashboard

A modern financial dashboard application built with Dash, using the Dash Pages feature for multi-page routing.

## Features

- Dashboard overview with key financial metrics
- Natural language query interface for data analysis
- Advanced financial analysis tools
- Interactive data visualizations
- Customizable report generation

## Project Structure

The application follows the multi-page structure pattern from the Dash documentation:

```
- app.py                 # Main entry point that initializes the app
- pages/                 # Directory containing all pages
  ├── __init__.py        # Package initialization
  ├── home.py            # Dashboard home page
  ├── query.py           # Query interface page
  ├── analysis.py        # Financial analysis page
  ├── visualizations.py  # Data visualization page
  ├── reports.py         # Report generation page
  └── utils.py           # Utility functions
```

## Setup and Installation

1. Clone this repository
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   python app.py
   ```
5. Open your browser and navigate to http://127.0.0.1:8050/

## Using Dash Pages

This application uses Dash Pages for routing, which simplifies managing multi-page applications. Each page registers itself with:

```python
dash.register_page(__name__, path='/page-path')
```

The main app.py file includes the pages container:

```python
app.layout = html.Div([
    # ...
    dash.page_container
    # ...
])
```

## Dash Mantine Components

This application uses the Dash Mantine Components library for its UI components. Important notes:

- For layout, use `dmc.Grid` and `dmc.GridCol` (not Row/Col which don't exist in dmc)
- Set column width using the `span` prop (e.g., `span=6` for half-width, `span=12` for full-width)
- Cards are created with `dmc.Card` and content goes directly inside (there is no CardBody component)
- Add padding to cards with `p="md"` instead of using a separate CardBody component

### Property Changes in dash-mantine-components 1.0.0

Many props have been shortened in version 1.0.0:
- Use `fw` instead of `weight` for font weight
- Use `c` instead of `color` for text color
- Use `ta` instead of `align` for text alignment
- Use `fz` instead of `size` for font size (though `size` still works in some components)

## Requirements

- Python 3.8+
- Dash 2.5.0+ (for Pages support)
- Other dependencies listed in requirements.txt 
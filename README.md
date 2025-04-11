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

This application uses the Dash Mantine Components library (v1.0.0) for its UI components. Important notes:

- For layout, use `dmc.SimpleGrid` instead of Grid/GridCol combinations
- Set column width using `style={"gridColumn": "span X"}` (where X is 1-12, e.g., `span 6` for half-width)
- Use `justify="space-between"` in `dmc.Group` (not `position="apart"`)
- Use `leftSection` for Button icons (not `leftIcon`)
- Cards are created with `dmc.Paper` with `withBorder=True`
- Add padding to components with `p="md"`

### Property Changes in dash-mantine-components 1.0.0

Many props have been shortened in version 1.0.0:
- Use `fw` instead of `weight` for font weight
- Use `c` instead of `color` for text color
- Use `ta` instead of `align` for text alignment
- Use `fz` instead of `size` for font size (though `size` still works in some components)

## Requirements

- Python 3.8+
- Dash 2.5.0+ (for Pages support)
- dash-mantine-components 1.0.0
- Other dependencies listed in requirements.txt 
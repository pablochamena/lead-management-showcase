import os
import sys

# Insert the parent directory of this file to sys.path to resolve 'app' imports correctly
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

from nicegui import ui
from app.components.kpi_cards import kpi_cards

@ui.page('/')
async def index_page() -> None:
    """
    Main SPA Dashboard page.
    Lays out the header and analytic metrics.
    """
    # Apply modern slate background color to index body
    ui.query('body').style('background-color: #f8fafc;')
    
    # 1. Dashboard Header Navigation
    with ui.header().classes('bg-slate-900 text-white p-4 items-center shadow-md justify-between w-full'):
        with ui.row().classes('items-center gap-3'):
            ui.icon('assignment', size='md').classes('text-blue-400')
            ui.label('Lead Management CRM').classes('text-lg font-bold tracking-tight')
        with ui.row().classes('items-center gap-2'):
            ui.button('Refrescar', icon='refresh', on_click=kpi_cards.refresh).props('flat color=white')
            
    # 2. Main Content Container
    with ui.column().classes('w-full max-w-7xl mx-auto p-6 gap-6'):
        
        # Section Title and Subtitle
        with ui.row().classes('justify-between items-center w-full'):
            with ui.column().classes('gap-1'):
                ui.label('Dashboard Comercial').classes('text-2xl font-extrabold text-slate-800')
                ui.label('Métricas analíticas del embudo de ventas en tiempo real.').classes('text-sm text-slate-500')
                
        # 3. Embed analytic KPI Cards
        await kpi_cards()

# Run NiceGUI bound to 0.0.0.0 and port 8080 (as expected by Docker Compose)
ui.run(
    host='0.0.0.0',
    port=8080,
    title='CRM Dashboard',
    show=False,
    reload=True
)

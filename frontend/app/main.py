import os
import sys

# Insert the parent directory of this file to sys.path to resolve 'app' imports correctly
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

from nicegui import ui
from app.components.kpi_cards import kpi_cards
from app.components.lead_table import lead_table
from app.components.lead_form import lead_form
from app.components.lead_detail import lead_detail, detail_state

@ui.page('/')
async def index_page() -> None:
    """
    Main SPA Dashboard entry point.
    Coordinates table actions, modal triggers, details display, and reactive updates.
    """
    # Apply modern slate background color to index body
    ui.query('body').style('background-color: #f8fafc;')
    
    # Callback to refresh all reactive components in the dashboard
    def refresh_all():
        kpi_cards.refresh()
        lead_table.refresh()
        if detail_state["selected_id"]:
            lead_detail.refresh(detail_state["selected_id"])
            
    # Callback when a lead row detail button is clicked in the table
    def select_lead(lead_id: int):
        detail_state["selected_id"] = lead_id
        lead_detail.refresh(lead_id)
        
    # Instantiate the lead registration dialog form
    creation_dialog = lead_form(on_success=refresh_all)
    
    # 1. Header Navigation Bar
    with ui.header().classes('bg-slate-900 text-white p-4 items-center shadow-md justify-between w-full no-wrap'):
        with ui.row().classes('items-center gap-3 no-wrap'):
            ui.icon('assignment', size='md').classes('text-blue-400')
            ui.label('Lead Management CRM').classes('text-lg font-bold tracking-tight')
            
        with ui.row().classes('items-center gap-3 no-wrap'):
            ui.button(
                'Registrar Lead',
                icon='add',
                on_click=creation_dialog.open
            ).props('dense').classes('bg-blue-600 hover:bg-blue-700 text-white font-bold px-3 py-1.5 rounded-lg text-sm')
            ui.button(icon='refresh', on_click=refresh_all).props('flat color=white dense')
            
    # 2. Main Layout Container
    with ui.column().classes('w-full max-w-7xl mx-auto p-6 gap-6'):
        
        # Section Header
        with ui.row().classes('justify-between items-center w-full'):
            with ui.column().classes('gap-1'):
                ui.label('Dashboard Comercial').classes('text-2xl font-extrabold text-slate-800')
                ui.label('Gestión integral de prospectos comerciales y registro histórico de interacciones.').classes('text-sm text-slate-500')
                
        # 3. Embed Sales Funnel Metrics
        await kpi_cards()
        
        # 4. Split Layout Section (Leads Table & Ficha Detail)
        # 12-column responsive layout grid: 7/12 for table, 5/12 for details
        with ui.grid(columns='1-col lg-12-col').classes('w-full gap-6 items-start mt-2'):
            
            # Left Column: Leads list table
            with ui.column().classes('lg:col-span-7 w-full gap-2'):
                ui.label('Clientes Potenciales').classes('text-xs font-bold text-slate-400 uppercase tracking-wider')
                await lead_table(on_select_lead=select_lead)
                
            # Right Column: Lead detail & Activity timeline
            with ui.column().classes('lg:col-span-5 w-full gap-2'):
                ui.label('Ficha de Seguimiento').classes('text-xs font-bold text-slate-400 uppercase tracking-wider')
                await lead_detail(detail_state["selected_id"], on_update=refresh_all)

# Run NiceGUI bound to 0.0.0.0 and port 8080 (as expected by Docker Compose)
ui.run(
    host='0.0.0.0',
    port=8080,
    title='CRM Dashboard',
    show=False,
    reload=True
)

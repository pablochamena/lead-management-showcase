from nicegui import ui
from app.client import api_request

@ui.refreshable
async def kpi_cards() -> None:
    """
    Renders 4 Sales Funnel KPI Cards using metrics retrieved from the backend.
    Refreshes dynamically when kpi_cards.refresh() is called.
    """
    # Request metrics from backend
    data = await api_request("GET", "/metrics")
    
    # Handle connection failures gracefully
    metrics = data if data else {"new": 0, "contacted": 0, "qualified": 0, "lost": 0}
    
    # 4-column responsive grid layout
    with ui.grid(columns='1-col sm-2-col md-4-col').classes('w-full gap-4'):
        
        # 1. NEW Leads (Blue Theme)
        with ui.card().classes('bg-blue-50 border-l-4 border-blue-500 shadow-sm p-4 rounded-lg'):
            with ui.row().classes('justify-between items-center w-full no-wrap'):
                ui.label('Nuevos').classes('text-blue-800 text-xs font-bold uppercase tracking-wider')
                ui.icon('fiber_new', size='sm').classes('text-blue-500')
            ui.label(str(metrics.get("new", 0))).classes('text-3xl font-extrabold text-blue-900 mt-2')
            ui.label('Prospectos sin contacto').classes('text-blue-600 text-xs mt-1')

        # 2. CONTACTED Leads (Amber/Yellow Theme)
        with ui.card().classes('bg-amber-50 border-l-4 border-amber-500 shadow-sm p-4 rounded-lg'):
            with ui.row().classes('justify-between items-center w-full no-wrap'):
                ui.label('Contactados').classes('text-amber-800 text-xs font-bold uppercase tracking-wider')
                ui.icon('chat_bubble_outline', size='sm').classes('text-amber-500')
            ui.label(str(metrics.get("contacted", 0))).classes('text-3xl font-extrabold text-amber-900 mt-2')
            ui.label('En comunicación activa').classes('text-amber-600 text-xs mt-1')

        # 3. QUALIFIED Leads (Green Theme)
        with ui.card().classes('bg-green-50 border-l-4 border-green-500 shadow-sm p-4 rounded-lg'):
            with ui.row().classes('justify-between items-center w-full no-wrap'):
                ui.label('Calificados').classes('text-green-800 text-xs font-bold uppercase tracking-wider')
                ui.icon('check_circle_outline', size='sm').classes('text-green-500')
            ui.label(str(metrics.get("qualified", 0))).classes('text-3xl font-extrabold text-green-900 mt-2')
            ui.label('Cumplen perfil de venta').classes('text-green-600 text-xs mt-1')

        # 4. LOST Leads (Red Theme)
        with ui.card().classes('bg-red-50 border-l-4 border-red-500 shadow-sm p-4 rounded-lg'):
            with ui.row().classes('justify-between items-center w-full no-wrap'):
                ui.label('Perdidos').classes('text-red-800 text-xs font-bold uppercase tracking-wider')
                ui.icon('highlight_off', size='sm').classes('text-red-500')
            ui.label(str(metrics.get("lost", 0))).classes('text-3xl font-extrabold text-red-900 mt-2')
            ui.label('Proceso finalizado').classes('text-red-600 text-xs mt-1')

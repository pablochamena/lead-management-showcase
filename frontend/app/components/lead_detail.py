from nicegui import ui, app as nicegui_app
from typing import Callable, Optional
from app.client import api_request
from app.models.enums import LeadStatus, ActivityType

def get_detail_state() -> dict:
    """
    Returns the current user's detail state from NiceGUI's per-session storage (A-01).
    Replaces the previous global mutable dict shared across all user connections.
    'selected_id' is stored per user to ensure multi-user isolation.
    """
    storage = nicegui_app.storage.user
    if "selected_id" not in storage:
        storage["selected_id"] = None
    return storage

@ui.refreshable
async def lead_detail(lead_id: Optional[int], on_update: Callable[[], None]) -> None:
    """
    Renders the detailed Lead profile card (Ficha Tecnica), status selection dropdown,
    activity logger form, and an immutable vertical activity history timeline.
    """
    if not lead_id:
        with ui.card().classes('w-full p-8 text-center items-center justify-center bg-white border rounded-xl shadow-sm'):
            ui.icon('assignment_ind', size='lg').classes('text-slate-300')
            ui.label('Seleccione un lead de la lista para ver su detalle e historial de actividades.').classes('text-slate-500 mt-2 text-sm font-medium')
        return

    # Fetch detailed info and activity timeline concurrently from the backend API
    lead = await api_request("GET", f"/leads/{lead_id}")
    activities = await api_request("GET", f"/leads/{lead_id}/activities")

    # Robust guard: verify lead is a valid dict with required keys before any subscript access.
    # This prevents 'NoneType' object errors under race conditions or malformed API responses (B-04).
    if not lead or not isinstance(lead, dict) or "name" not in lead:
        with ui.card().classes('w-full p-8 text-center items-center justify-center bg-white border rounded-xl shadow-sm'):
            ui.icon('error_outline', size='lg').classes('text-red-300')
            ui.label('No se pudo obtener la información de este lead.').classes('text-red-500 mt-2 text-sm font-medium')
        return
        
    activities = activities if activities else []

    with ui.column().classes('w-full gap-6'):
        
        # 1. FICHA TÉCNICA CARD
        with ui.card().classes('w-full p-6 bg-white border shadow-sm rounded-xl'):
            with ui.row().classes('justify-between items-center w-full gap-4'):
                with ui.column().classes('gap-0'):
                    ui.label(lead["name"]).classes('text-2xl font-bold text-slate-800')
                    ui.label(f"ID del lead: #{lead['id']}").classes('text-xs text-slate-400')
                    
                # Dynamic status dropdown transitioner
                status_select = ui.select(
                    options=[s.value for s in LeadStatus],
                    value=lead["status"]
                ).props('outlined dense').classes('w-44')
                
                async def update_status(captured_lead_id: int = lead_id):
                    """Update lead status. Captures lead_id as a default argument to prevent
                    stale closure bugs when the component is refreshed (B-04)."""
                    if status_select.value == lead["status"]:
                        return
                    res = await api_request("PUT", f"/leads/{captured_lead_id}", json={"status": status_select.value})
                    if res:
                        ui.notify(f"Estado del lead actualizado a {status_select.value}", type="positive", position="top-right")
                        on_update()  # Refresh metrics cards and main lead list table
                        lead_detail.refresh(captured_lead_id)  # Refresh lead profile values locally
                        
                status_select.on('update:model-value', update_status)

            # Details grid layout
            with ui.grid(columns='1-col sm-2-col').classes('w-full gap-4 mt-6 border-t pt-4'):
                with ui.row().classes('items-center gap-2 no-wrap'):
                    ui.icon('business', size='xs').classes('text-slate-400')
                    ui.label('Empresa:').classes('text-xs font-bold text-slate-400 uppercase tracking-wider')
                    ui.label(lead.get("company") or 'N/A').classes('text-sm text-slate-700 font-medium')
                    
                with ui.row().classes('items-center gap-2 no-wrap'):
                    ui.icon('email', size='xs').classes('text-slate-400')
                    ui.label('Correo:').classes('text-xs font-bold text-slate-400 uppercase tracking-wider')
                    ui.label(lead["email"]).classes('text-sm text-slate-700 font-medium')
                    
                with ui.row().classes('items-center gap-2 no-wrap'):
                    ui.icon('phone', size='xs').classes('text-slate-400')
                    ui.label('Teléfono:').classes('text-xs font-bold text-slate-400 uppercase tracking-wider')
                    ui.label(lead.get("phone") or 'N/A').classes('text-sm text-slate-700 font-medium')
                    
                with ui.row().classes('items-center gap-2 no-wrap'):
                    ui.icon('calendar_today', size='xs').classes('text-slate-400')
                    ui.label('Creado:').classes('text-xs font-bold text-slate-400 uppercase tracking-wider')
                    try:
                        date_str = lead["created_at"].split("T")[0]
                    except Exception:
                        date_str = lead["created_at"]
                    ui.label(date_str).classes('text-sm text-slate-700 font-medium')

        # 2. LOG NEW INTERACTION FORM CARD
        with ui.card().classes('w-full p-6 bg-white border shadow-sm rounded-xl'):
            ui.label('Registrar Interacción / Nota').classes('text-xs font-bold text-slate-400 uppercase tracking-wider')
            
            with ui.row().classes('w-full gap-4 items-start mt-4'):
                type_select = ui.select(
                    options=[t.value for t in ActivityType],
                    value=ActivityType.NOTE.value
                ).props('outlined dense').classes('w-44')
                
                notes_input = ui.textarea(
                    placeholder='Escriba los detalles de la interacción...'
                ).props('outlined dense required rows=2').classes('flex-1')
                
                async def add_activity(captured_lead_id: int = lead_id):
                    """Register a new activity. Captures lead_id as a default argument to prevent
                    stale closure bugs when the component is refreshed (B-04)."""
                    if not notes_input.value or not notes_input.value.strip():
                        ui.notify("Por favor ingrese las notas de la actividad.", type="warning", position="top-right")
                        return
                    
                    payload = {
                        "type": type_select.value,
                        "notes": notes_input.value.strip()
                    }
                    
                    # POST activity to API
                    res = await api_request("POST", f"/leads/{captured_lead_id}/activities", json=payload)
                    if res:
                        ui.notify("Interacción registrada correctamente.", type="positive", position="top-right")
                        notes_input.value = ""  # Clear input field
                        lead_detail.refresh(captured_lead_id)  # Refresh activity timeline locally
                        
                ui.button('Registrar', icon='send', on_click=add_activity).props('dense').classes('bg-blue-600 text-white px-4 py-2 rounded-lg text-xs font-bold self-end')

        # 3. CHRONOLOGICAL TIMELINE OF ACTIVITIES (IMMUTABLE)
        with ui.card().classes('w-full p-6 bg-white border shadow-sm rounded-xl'):
            ui.label('Historial de Seguimiento').classes('text-xs font-bold text-slate-400 uppercase tracking-wider')
            
            if not activities:
                with ui.column().classes('w-full p-8 text-center items-center justify-center bg-slate-50 rounded-lg mt-4'):
                    ui.icon('history', size='md').classes('text-slate-300')
                    ui.label('Sin actividades registradas para este lead.').classes('text-slate-400 mt-2 text-xs font-medium')
            else:
                # Renders activities in chronological desc order using NiceGUI's native timeline
                with ui.timeline(side='right').classes('w-full mt-6 px-2'):
                    for act in activities:
                        try:
                            # Clean timestamp formatting: "YYYY-MM-DD HH:MM"
                            date_part = act["created_at"].split("T")[0]
                            time_part = act["created_at"].split("T")[1][:5]
                            act_date = f"{date_part} {time_part}"
                        except Exception:
                            act_date = act["created_at"]
                            
                        # Pick icon and theme depending on activity type
                        act_type = act["type"]
                        act_icon = 'chat'
                        act_color = 'blue-500'
                        if act_type == 'CALL':
                            act_icon = 'phone'
                            act_color = 'amber-500'
                        elif act_type == 'EMAIL':
                            act_icon = 'email'
                            act_color = 'green-500'
                            
                        # Fully immutable timeline entries: no edit/delete buttons are provided
                        ui.timeline_entry(
                            body=act["notes"],
                            title=f"Interacción: {act_type}",
                            subtitle=act_date,
                            icon=act_icon,
                            color=act_color
                        )

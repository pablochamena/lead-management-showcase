from nicegui import ui
from typing import Callable, Optional
from app.client import api_request
from app.models.enums import LeadStatus

# Shared table filtering and pagination state
table_state = {
    "query": "",
    "status": None,
    "skip": 0,
    "limit": 10
}

@ui.refreshable
async def lead_table(on_select_lead: Callable[[int], None]) -> None:
    """
    Renders the interactive Leads table component.
    Allows searching, filtering by status, and pagination.
    """
    # Fetch paginated and filtered leads list from backend
    url = f"/leads?skip={table_state['skip']}&limit={table_state['limit']}"
    if table_state["status"]:
        url += f"&status={table_state['status']}"
    if table_state["query"]:
        url += f"&query={table_state['query']}"
        
    data = await api_request("GET", url)
    # Strict type guard: protects against None responses AND malformed non-dict payloads
    # (e.g. upstream proxy errors returning HTML or a plain string instead of JSON) (B-05).
    leads = data.get("leads", []) if isinstance(data, dict) else []
    
    # Define table columns for Quasar integration
    columns = [
        {'name': 'name', 'label': 'Nombre', 'field': 'name', 'required': True, 'align': 'left'},
        {'name': 'company', 'label': 'Empresa', 'field': 'company', 'align': 'left'},
        {'name': 'email', 'label': 'Email', 'field': 'email', 'align': 'left'},
        {'name': 'status', 'label': 'Estado', 'field': 'status', 'align': 'center'},
        {'name': 'created_at', 'label': 'Creado', 'field': 'created_at', 'align': 'center'},
        {'name': 'action', 'label': 'Detalle', 'field': 'id', 'align': 'center'}
    ]
    
    rows = []
    for l in leads:
        created_dt = l.get("created_at", "")
        try:
            created_dt = created_dt.split("T")[0]
        except Exception:
            pass
        rows.append({
            'id': l['id'],
            'name': l['name'],
            'company': l.get('company') or '-',
            'email': l['email'],
            'status': l['status'],
            'created_at': created_dt
        })
        
    # Filters Bar
    with ui.row().classes('w-full items-center justify-between gap-4 p-4 bg-white rounded-lg border shadow-sm'):
        with ui.row().classes('items-center gap-3 no-wrap'):
            # Text search input
            search_input = ui.input(placeholder='Buscar leads...').props('outlined dense').classes('w-64')
            search_input.value = table_state["query"]
            
            # Status dropdown
            status_select = ui.select(
                options=['Todos'] + [s.value for s in LeadStatus],
                value=table_state["status"] or 'Todos'
            ).props('outlined dense').classes('w-44')
            
            def apply_filters():
                table_state["query"] = search_input.value or ""
                table_state["status"] = None if status_select.value == 'Todos' else status_select.value
                table_state["skip"] = 0  # Reset to first page
                lead_table.refresh()
                
            ui.button('Filtrar', icon='search', on_click=apply_filters).props('dense').classes('bg-blue-600 text-white px-3 py-1 rounded')
            
        # Paginator controls
        with ui.row().classes('items-center gap-2'):
            ui.label(f"Pág. {(table_state['skip'] // table_state['limit']) + 1}").classes('text-sm text-slate-500 font-medium')
            
            def prev_page():
                if table_state["skip"] >= table_state["limit"]:
                    table_state["skip"] -= table_state["limit"]
                    lead_table.refresh()
                    
            def next_page():
                if len(leads) == table_state["limit"]:
                    table_state["skip"] += table_state["limit"]
                    lead_table.refresh()
                    
            ui.button(icon='chevron_left', on_click=prev_page).props('flat dense').enabled(table_state["skip"] > 0)
            ui.button(icon='chevron_right', on_click=next_page).props('flat dense').enabled(len(leads) == table_state["limit"])

    # NiceGUI / Quasar Table
    if not rows:
        with ui.card().classes('w-full p-8 text-center items-center justify-center bg-white border'):
            ui.icon('search_off', size='lg').classes('text-slate-300')
            ui.label('No se encontraron leads con los criterios seleccionados.').classes('text-slate-500 mt-2 text-sm')
    else:
        with ui.table(columns=columns, rows=rows, row_key='id').classes('w-full bg-white shadow-sm rounded-lg border') as table:
            # Custom slot for status column (colored badges)
            table.add_slot('body-cell-status', r'''
                <q-td :props="props">
                    <q-chip :color="props.value === 'NEW' ? 'blue-1' : props.value === 'CONTACTED' ? 'amber-1' : props.value === 'QUALIFIED' ? 'green-1' : 'red-1'" 
                            :text-color="props.value === 'NEW' ? 'blue-9' : props.value === 'CONTACTED' ? 'amber-9' : props.value === 'QUALIFIED' ? 'green-9' : 'red-9'"
                            dense class="text-weight-bold">
                        {{ props.value }}
                    </q-chip>
                </q-td>
            ''')
            # Custom slot for action column (detail button)
            table.add_slot('body-cell-action', '''
                <q-td :props="props" class="text-center">
                    <q-btn flat round dense color="primary" icon="visibility" @click="$parent.$emit('view_lead', props.value)" />
                </q-td>
            ''')
            
        # Bind table custom event to the Python selection callback
        table.on('view_lead', lambda msg: on_select_lead(msg.args))

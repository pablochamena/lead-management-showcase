from nicegui import ui
from typing import Callable
from app.client import api_request

def lead_form(on_success: Callable[[], None]) -> ui.dialog:
    """
    Renders a creation modal dialog for adding a new Lead.
    Triggers the on_success callback when the Lead is persisted.
    """
    with ui.dialog() as dialog, ui.card().classes('w-full max-w-md p-6 gap-4 rounded-xl'):
        # Modal Header
        ui.label('Registrar Cliente Potencial').classes('text-xl font-bold text-slate-800')
        ui.label('Complete la información de contacto inicial para el nuevo lead.').classes('text-xs text-slate-500 -mt-2')
        
        # Form Fields
        name_input = ui.input('Nombre completo *').props('outlined dense required').classes('w-full mt-2')
        company_input = ui.input('Empresa (Opcional)').props('outlined dense').classes('w-full')
        email_input = ui.input('Correo electrónico *').props('outlined dense required type=email').classes('w-full')
        phone_input = ui.input('Teléfono (Opcional)').props('outlined dense').classes('w-full')
        
        async def submit():
            # Validate required fields locally
            if not name_input.value or not name_input.value.strip():
                ui.notify("El nombre completo es obligatorio.", type="warning", position="top-right")
                return
            if not email_input.value or not email_input.value.strip():
                ui.notify("El correo electrónico es obligatorio.", type="warning", position="top-right")
                return
                
            payload = {
                "name": name_input.value.strip(),
                "email": email_input.value.strip(),
                "company": company_input.value.strip() if company_input.value else None,
                "phone": phone_input.value.strip() if phone_input.value else None
            }
            
            # Send post request via HTTP helper
            result = await api_request("POST", "/leads", json=payload)
            if result:
                # Success notification
                ui.notify(
                    f"Lead '{payload['name']}' registrado correctamente.",
                    type="positive",
                    position="top-right"
                )
                
                # Clear form fields
                name_input.value = ""
                company_input.value = ""
                email_input.value = ""
                phone_input.value = ""
                
                # Close modal and invoke dashboard refreshes
                dialog.close()
                on_success()
                
        # Dialog Action buttons
        with ui.row().classes('justify-end gap-2 w-full mt-4'):
            ui.button('Cancelar', on_click=dialog.close).props('flat color=grey').classes('text-xs font-semibold')
            ui.button('Guardar Lead', on_click=submit).props('dense').classes('bg-blue-600 text-white px-4 py-2 rounded-lg text-xs font-bold')
            
    return dialog

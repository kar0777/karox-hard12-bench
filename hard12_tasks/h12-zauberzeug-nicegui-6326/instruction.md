You are solving a software engineering issue in the supplied repository. Inspect the repository, implement the requested production-code change, and run appropriate tests. Do not stop at analysis when a code change is required. Do not search online, inspect repository remotes for the ready-made solution, or access issue/PR pages. Do not modify benchmark tests unless the task explicitly requires test changes. Do not commit, push, reset, or rewrite repository history. Leave the working tree containing your final solution.

Issue:

Sortable container elements do not work if created by a callback or inside dialog

### First Check

- [x] I added a very descriptive title here.
- [x] This is not a security issue (those should be reported via the [security advisory](https://github.com/zauberzeug/nicegui/security/advisories/new) instead).
- [x] This is not a Q&A. I am sure something is wrong with NiceGUI or its documentation.
- [x] I used the GitHub search to find a similar [issue](https://github.com/zauberzeug/nicegui/issues) and came up empty.

### Example Code

```python
from nicegui import ui


def card_ui(hidden:bool = True,container_type=ui.card,delete=False):
    """Example sortable container from Nicegui docs
    With the addition of making it hidden or not
    """
    if hidden:
        prop_args = {'add':'hidden=true'}
    else:
        prop_args = {'remove':'hidden=true'}
        
    with container_type().props(**prop_args) as card:
        for name in ['Larry','Curly','Moe']:
            with ui.row().classes('items-center gap-2'):
                ui.icon('drag_indicator') \
                    .classes('handle cursor-grab active:cursor-grabbing')
                ui.label(name)
        card.make_sortable(handle='.handle')
    
    if delete:
        card.delete()

def sortable_dialog(container_type=ui.card):
    """Makes the sortable UI in a dialog"""
    with ui.dialog() as dialog, ui.card():
        ui.label('Sort these guys out')
        card_ui(hidden=False,container_type=container_type)
        ui.button('Close', on_click=dialog.close)
    dialog.open()
  
@ui.page('/not-working')
async def not_working():
    ui.label('Click this button to open a sortable dialog that does not work')
    
    #Just in case the container type matters (it does not)
    ui.button('Open Dialog with card',on_click=sortable_dialog)
    ui.button('Open Dialog with column',on_click=lambda: sortable_dialog(container_type=ui.column))
    ui.button('Open Dialog with row',on_click=lambda: sortable_dialog(container_type=ui.row))
    
    ui.label("The make_sortable() method doesn't appear to work for any UI created on the fly in a callback.")
    ui.button('Create sortable UI below',on_click=lambda:card_ui(hidden=False))
    
    ui.link('Go Back',main)

@ui.page('/empty')
async def empty_page():
    ui.label("This page only makes the hidden sortable UI. You can't see it.")
    card_ui()
    
    ui.label("If you go back to the not-working page, it will work now.")
    ui.link('Go Back',main)
  
@ui.page('/working')
async def working():
    ui.label('Click this button to open a sortable dialog.')
    card_ui(hidden=True,delete=True) #this runs on page load
    ui.button('Open Dialog',on_click=sortable_dialog)    
    
    ui.label('This will work even if you came here first.')
    ui.link('back',main)

@ui.page('/')
def main():
    ui.link('Not Working Example',not_working)
    ui.link('Empty Page with hidden UI',empty_page)
    ui.link('Working Example',working)
ui.run()
```

### Description

Hello, I spent some time going in circles trying to troubleshoot and find a reproducible minimal example of this, and this is what I landed on.

I encountered the issue at first when trying to make a sortable container inside of a dialog, which is opened by a button `on_click` callback or similar (like in the examples in the docs). When I did so, the draggable elements just would not drag.

I ended up concluding that this will not work in any case. I tried a bunch of different stuff that google and LLMs suggested - only creating the UI on the dialog's `on_show` callback, clearing the dialog before creating the UI, waiting some time before making it sortable, and more, and nothing worked.

It seems to me that if the UI that is meant to be made sortable is created by an event callback (such as upon opening a dialog or clicking a button), then the sortable elements will not be draggable. My guess is that something is going on with the JS for the make_sortable() method where it tries to operate on elements that aren't drawn just yet - but I can only speculate. It's likely something more complicated, given the workaround below.

**The Workaround**  

It seems that if you make a sortable container once, any other sortable container will work afterwards, even if the contents are different, the structure is different, or the original sortable container is deleted. So if you make a sortable container that will run on page load, sortable containers created by event callbacks will work. This persists through navigation. The workaround is to make a function that creates a dummy hidden sortable UI and immediately deletes itself, and run this at the top of your app. My minimal working example demonstrates this.


### NiceGUI Version

3.16.0

### Python Version

3.13.3

### Browser

Chrome

### Operating System

Windows

### Additional Context

_No response_

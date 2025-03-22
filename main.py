from fasthtml.common import *
from monsterui.all import *
from datetime import datetime, timedelta


hdrs = Theme.red.headers()

# Initialize FastHTML app
app, rt = fast_app(hdrs=hdrs, live=True)

@rt('/')
def get():
    return Title('MadRed'), Main(
    DivCentered(
    	H3('MadRed'),
    	P('Calculate your periods easily')
    ),
    Grid(
        Div(
        	H4('Fill in the information'),
     		Form(
     		    LabelInput('Last Period Date', type='date', name='last_period', cls='input-field'),
     		    LabelInput('Average Cycle Length (in days)', type='number', name='cycle_length', min=20, max=40, placeholder='20', cls='input-field'),
     		    Button(UkIcon('rocket', cls='mr-2'),'Calculate', hx_post='/submit', hx_target='#result', hx_swap='innerHTML',hx_include='false', id='period-form',cls=(ButtonT.primary)), 
     		    
     	   
     		),
     		Div(
            	Button("Theme",data_uk_toggle="target: #my-modal" ),
            	Modal(ModalTitle("Set Your Theme"), 
              	ThemePicker(),
             	footer=ModalCloseButton("Close", cls=ButtonT.primary),id='my-modal')
            ),
     		cls =('space-y-4 space-x-4 mt-2') 
     	),		

        Div(
        	Card(
        		DivCentered(
        			P('Results will appear here. after calculating..'),
        		),
        		cls =('h-48'),
        		id='result' 
        	),
        	cls =('cols=2 gap-x-4',)
    		)	
        ),
    cls ='ml-4 mr-4'
    )

@rt('/submit')
def post(last_period: str, cycle_length: str):
    try:
        # Convert inputs to appropriate types
        last_period_date = datetime.strptime(last_period, '%Y-%m-%d')  # Parse date
        cycle_length_days = int(cycle_length)  # Convert to integer

        # Perform calculations
        next_red_day = last_period_date + timedelta(days=cycle_length_days)
        reminder_date = next_red_day - timedelta(days=5)

        #Days remaining
        today = datetime.today().date()
        next_red_day_date = next_red_day.date()
        days_remaining = (next_red_day_date - today).days

        # Format the results
        next_red_day_str = next_red_day.strftime('%Y-%m-%d')
        reminder_date_str = reminder_date.strftime('%Y-%m-%d')

        # Return the results as HTML
        return DivVStacked(
        	Div(
        		P(days_remaining,cls=('text-8xl')),
        		P('Days Remaining',cls =(TextT.warning))
        	),
            P(f"Next Flow Day is : {next_red_day_str}",cls=(TextT.success,'text-md')),
            
            cls="response-content"
        )

    except ValueError as e:
        # Handle invalid input
        return Div(P(f"Error: Please enter valid data. {str(e)}"), cls="error-message")
@rt('/theme')
def ex_theme_switcher():
    return ThemePicker()

serve()
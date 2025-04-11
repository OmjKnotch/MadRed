from fasthtml.common import *
from monsterui.all import *
from datetime import datetime, timedelta
import uuid

style =Style("""
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap');
body {
    font-family:Inter 
}
"""
)
hdrs = Theme.red.headers()

# Initialize FastHTML app
app, rt = fast_app(hdrs=(hdrs,style), live=True)

@rt('/')
def get(session):
    if 'session_id' not in session:session['session_id'] = str(uuid.uuid4())
    return Title('MadRed'), Main(
        DivCentered(
           
            Img(src='/public/madred-logo.png', alt='MadRed', cls='w-2/3 h-24 md:w-auto md:h-auto pb-4'),
            H1("Period Tracking, Fit for a Queen",
                    cls='text-center  text-5xl text-transparent bg-clip-text bg-gradient-to-r from-[#ED8B00] to-[#D01665]' 
            ),
                
            P('MadRed gives you absolute control over your flow. No more surprises, ever!', cls='text-2xl text-center text-neutral-800'),
            cls='py-4 space-y-4 '
         ),

    Grid(
        Div(
        	P('Give us some info',cls ='text-transparent bg-clip-text bg-gradient-to-r from-[#ED8B00] to-[#D01665] text-3xl'),
            Card(
     		Form(
     		    LabelInput('Last Period Date', type='date', name='last_period', cls='input-field'),
     		    LabelInput('Average Cycle Length (in days)', type='number', name='cycle_length', min=20, max=40, placeholder='20', cls='input-field'),
     		    Button(UkIcon('rocket', cls='mr-2'),'Calculate', hx_post='/submit', hx_target='#result', hx_swap='innerHTML',hx_include='false', id='period-form',cls=(ButtonT.primary,'rounded-lg')), 
     		    cls='bg-[#E5D9F2]'
     		),
            cls ='rounded-lg bg-[#E5D9F2]'
            ),
     		Div(
            	Button("Theme",data_uk_toggle="target: #my-modal" ),
            	Modal(ModalTitle("Set Your Theme"), 
              	ThemePicker(),
             	footer=ModalCloseButton("Close", cls=ButtonT.primary),id='my-modal')
            ),
     		cls =('space-y-4 space-x-4 pt-20 ') 
     	),		

        Div(
        	Card(
        		DivCentered(
                    DivVStacked(
                        P('Results will appear here after calculating',cls ='text-center text-2xl'),
                        Loading(cls ='loading-infinity lg bg-red-800'),
                        
                    ),
                    
        			
        		),
        		cls =(' h-80 bg-[#E5D9F2]'),
        		id='result' 
        	),
        	cls =('cols=2 gap-x-4 pt-10 rounded-lg ',)
    		)	
        ),

        Footer(
            DividerLine(),
                
                DivVStacked(
                    P(' MadRed is made with ❤️ for a Queen ',cls='text-neutral-700'),
                    A(Button(P("Request a feature,Give Feedback,Inquire or just curious - Let's Talk"),cls ='hover:bg-gradient-to-r from-[#ED8B00] to-[#D01665] py-8',), href="https://www.instagram.com/historical_client_12/"),
                ),
            
        cls ='mt-20 bg-neutral-100 w-100'
        ),
    cls ='h-screen w-screen pl-4 pr-4 bg-[#FBFBFB] pt-4'
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
        		P(days_remaining,cls=('text-8xl text-[#ED8B00]')),
        		P('Days Remaining',cls =('text-lg text-purple-500'))
        	),
            P(f"Next Period Starts on: ",cls=('text-xl text-[#89AC46] ')),
            Span(Time(next_red_day_str,cls='text-4xl')),
            
            cls="response-content bg-[#E5D9F2]"
        )

    except ValueError as e:
        # Handle invalid input
        return Div(P(f"Error: Please enter valid data. {str(e)}"), cls="error-message")
@rt('/theme')
def ex_theme_switcher():
    return ThemePicker()

serve()
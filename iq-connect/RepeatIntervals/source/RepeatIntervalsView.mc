using Toybox.WatchUi as Ui;
using Toybox.Graphics as Gfx;
using Toybox.Timer as Timer;
using Toybox.Attention as Attention;
using Toybox.Application as App;

var timer1;
var activeTimerState;
var count1;
var restTime;
var intervalTime;
var currentMode;
var nextMode;
var started;

class RepeatIntervalsView extends Ui.View {

    function onLayout(dc)
    {
    	currentMode = MODE_INTERVAL;
    	nextMode = MODE_REST;
    	restTime = new SetTime(0,10);
    	intervalTime = new SetTime(0,20);
    	count1 =0;
        timer1 = new Timer.Timer();
        activeTimerState = new TimerState(intervalTime.getMins(), intervalTime.getSecs());
 		started = false;   
 		
    }
    

    //! Update the view
    function onUpdate(dc) {
        // Call the parent onUpdate function to redraw the layout

 	    dc.setColor( Gfx.COLOR_BLACK, Gfx.COLOR_DK_BLUE );
        dc.clear();
        dc.setColor( Gfx.COLOR_WHITE, Gfx.COLOR_TRANSPARENT );
        var string;
        string  = "Rustyware ";
        dc.drawText( ( dc.getWidth() / 2 ), 10, Gfx.FONT_XTINY , string, Gfx.TEXT_JUSTIFY_CENTER );
      
      	if(currentMode == MODE_REST){
       		string  = "REST";
       	}
       	else if (currentMode == MODE_INTERVAL){
       		string = "INTERVAL";
       	}
       	
       	dc.drawText( ( dc.getWidth() / 2 ), 40, Gfx.FONT_MEDIUM , string, Gfx.TEXT_JUSTIFY_CENTER );
       
        string  = "Interval " + intervalTime.getMins() + ":" +  intervalTime.getSecs() ;
       	dc.drawText( 10, (dc.getHeight() / 2) -30 , Gfx.FONT_TINY , string, Gfx.TEXT_JUSTIFY_LEFT );
       
      	string  = "Rest " + restTime.getMins() + ":" + restTime.getSecs() ;
       	dc.drawText( dc.getWidth()-10 , (dc.getHeight() / 2) -30, Gfx.FONT_TINY , string, Gfx.TEXT_JUSTIFY_RIGHT );
        
       	string  = activeTimerState.getCurrentMins() + ":" +  activeTimerState.getCurrentSecs() ;
        dc.drawText( ( dc.getWidth() / 2 ), (dc.getHeight() / 2) -10, Gfx.FONT_NUMBER_HOT, string, Gfx.TEXT_JUSTIFY_CENTER );
       // View.onUpdate(dc);
    }

   
    function onHide() {
  
    }

}

class RepeatIntervalsDelegate extends Ui.BehaviorDelegate {


	

	function onKey(evt)
	{
		System.println("Key type : " + evt.getType() );
		System.println("Key event : " + evt.getKey() );
		
		if(evt.getKey() == Ui.KEY_LIGHT){
	    	intervalTime.increment();
	    }
	    else if(evt.getKey() == 8 ){
	    	intervalTime.decrement();
	    	
	    }
	   	else if(evt.getKey() == 4){
	    	restTime.increment();
	    }
	   	else if(evt.getKey() == 5 ){
	    	restTime.decrement();
	    	
	    }   
	    if(evt.getKey() == 7 ){
	    	activeTimerState.reset();
			System.println("stopping timer");
			timer1.stop();
			started = false;
				currentMode = MODE_INTERVAL;
    	nextMode = MODE_REST;
			
				activeTimerState.updateTimer(intervalTime.getMins(), intervalTime.getSecs());
		

			Ui.requestUpdate(); 
	    } 
	    else if(evt.getKey() == 13 ){
	    	
	    	if (started == true)
			{ 
				System.println("stopping timer");
				timer1.stop();
				started = false;
			}
			else
			{
				System.println("starting timeer");
				started = true;
       			timer1.start( method(:callback1), 1000, true );
			}

	    } 
	    Ui.requestUpdate();  
	}

	
	function callback1()
    {
        count1 += 1;
        if (activeTimerState.isExpired())
        {
 			Attention.vibrate( new Attention.VibeProfile( 100, 100  ));  
 			Attention.playTone( 7 );        	
        	if(currentMode == MODE_INTERVAL){
        		activeTimerState =  new TimerState(restTime.getMins(), restTime.getSecs());
        		currentMode = nextMode;
        		nextMode = MODE_INTERVAL;
        	}
        	else{
        	  	activeTimerState =  new TimerState(intervalTime.getMins(), intervalTime.getSecs());
        		currentMode = nextMode;
        		nextMode = MODE_REST;
			}
        }
        else{
        	activeTimerState.decrement();
        }	
        Ui.requestUpdate();
    }
	
}


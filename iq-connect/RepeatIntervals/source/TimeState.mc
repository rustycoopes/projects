
using Toybox.WatchUi as Ui;
using Toybox.Graphics as Gfx;
using Toybox.Application as App;
enum
{
     MODE_INTERVAL,
    MODE_REST
    
}


class TimerState{

	var mins = 2;
	var secs = 0;
	var originalMins;
	var originalSecs;
	
    function initialize(m,s)
    {
        mins = m;
        secs = s;
        originalMins = m;
        originalSecs = s;
    }
	
	function getCurrentMins()
	{
		return mins;
	}
	
	function getCurrentSecs()
	{
		return secs;
	}
	
	function getState()
	{
		return state;
	}
	
	function reset()
	{
		mins = originalMins;
		secs = originalSecs;
	}
	function updateTimer(m,s){
	
		if(m<mins){
			mins = m;
		}
		if(s<secs)
		{
			secs = s;
		}
		originalMins = m;
		originalSecs = s;
		
	}
	function isExpired(){
		return mins == 0 && secs == 0;
	}
	

	function decrement(){
		
	
		if ( mins == 0 && secs == 0)
		{
			return;
		}	
		if ( secs == 0 )
		{
			mins = mins - 1;
			secs = 59;
		}
		else
		{
			secs = secs -1;
		}	
	}

}



class SetTime{

	var mins = 2;
	var secs = 0;
	
    function initialize(m,s)
    {
        mins = m;
        secs = s;
    }
	
	function getMins()
	{
		return mins;
	}
	
	function getSecs()
	{
		return secs;
	}
	
	function increment(){
		if(secs == 59)
		{
			mins = mins +1;
			secs = 0;
		}
		else
		{
			secs = secs + 1;
		}
	}
	
	function decrement(){
		
		if(secs == 0 && mins == 0){
			return;
		}
		
		if(secs == 0)
		{
			mins = mins -1;
			secs = 59;
		}
		else
		{
			secs = secs - 1;
		}
	}
}






autowatch = 1; // JS Attribute

// inlets and outlets
inlets = 1;
outlets = 1;

function msg_int(input)
{
	var output;

	if (input >= 0 && input < 5000)
	{output = 0.4;
	}else if (input >= 5000 && input < 50000)
	{output = 0.6;
	}else if (input >= 50000 && input < 300000)
	{output = 0.8;
	}else if (input >= 300000 && input < 1000000)
	{output = 0.9;
	}else if (input >= 1000000)
	{output = 1.0;}
		
	outlet(0, output);
}
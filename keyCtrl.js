autowatch = 1; // JS Attribute

// inlets and outlets
inlets = 1;
outlets = 1;

function msg_float(input)
{
	var output;

	if (input >= 0. && input < 5000.0)
	{output = 96;
	}else if (input >= 5000.0 && input < 50000.0)
	{output = 84;
	}else if (input >= 50000.0 && input < 300000.0)
	{output = 72;
	}else if (input >= 300000.0 && input < 1000000.0)
	{output = 60;
	}else if (input >= 1000000.0)
	{output = 48;}
		
	outlet(0, output);
}
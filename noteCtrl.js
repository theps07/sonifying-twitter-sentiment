autowatch = 1; // JS Attribute

// inlets and outlets
inlets = 1;
outlets = 1;

function msg_float(input)
{
	var output;

	if (input >= -1.0 && input <= -0.5)
	{output = 84;
	}else if (input > -0.5 && input < 0)
	{output = 72;
	}else if (input == 0)
	{output = 96;
	}else if (input > 0 && input < 0.5)
	{output = 60;
	}else if (input >= 0.5 && input <= 1.0)
	{output = 48;}
		
	outlet(0, output);
}
function debugFunctionModifier()
{
	this.preLoadWindowArray = Object.keys(window);
	this.postLoadWindowArray = [];
	this.functionLevel = 0;
	this.debug = true;
	this.badFunctions = 0;
	
	this.globalName = "pageElements.debugController";
//	this.goThroughClass(specialOrderController);
}

debugFunctionModifier.prototype.postLoadRun = function()
{
	if (this.debug)
	{
		this.postLoadWindowArray = Object.keys(window);
		var diffArray = [];
		
		for (x in this.postLoadWindowArray)
		{
			if (this.preLoadWindowArray.indexOf(this.postLoadWindowArray[x]) == -1)
				diffArray.push(this.postLoadWindowArray[x]);
		}
		
		for (x in diffArray)
		{
			var thisVar = null;
			eval("thisVar = " + diffArray[x]);
			if (typeof(thisVar) == 'function')
			{
				this.goThroughClass(thisVar);
			}
			
		}
	}
//	console.log(this.badFunctions + " bad functions, with return in the middle");
}

debugFunctionModifier.prototype.goThroughClass = function(cl)
{
	var functionName = cl.name
	
	if (functionName == "debugFunctionCall" || functionName == "debugFunctionReturn" || functionName == "itemListAddItem")
		return;
	
	if (cl.prototype.length > 0)
		functionName += "::__Constructor()";
	else
		functionName += "()";
	
	var startFunction = "console.log('" + cl.name + "::__Constructor()', arguments);"
	
	fnString = cl.toString();
	fnString = fnString.replace(/{/, "{\n\t" + this.globalName + ".onFunctionStart('" + functionName + "', arguments)\n");
	
	if (fnString.match(/return[^\n]*\n}$/) !== null)
		fnString = fnString.replace(/(return)\s+([^\n\;]*);?[^\n]*\n}$/, this.globalName + ".onFunctionEnd($2)\;\n\t$1 $2\;\n}")
	else
		fnString = fnString.replace(/}$/, "\t" + this.globalName + ".onFunctionEnd()\n}");
	
	var newFn;
	eval("newFn = " + fnString);
	
	for (x in cl.prototype)
	{
//		break;
		this.injectIntoFunction(cl, x);
	}
	window[cl.name] = newFn;
	for (x in cl.prototype)
	{
		window[cl.name].prototype[x] = cl.prototype[x];
	}
}

debugFunctionModifier.prototype.injectIntoFunction = function(cl, fnName)
{
	var fn;
	eval("fn = cl.prototype." + fnName);
	
	var fnString = fn.toString();
	
	fnString = fnString.replace(/{/, "{\n\t" + this.globalName + ".onFunctionStart('" + cl.name + "::" + fnName + "()', arguments)\n");
	
//	if (fnString.match(/(return([ \t]+[a-zA-Z][^\s]*)?(;|\n))(\s*[^\s]+\s*)+\s*\}$/i))
//	{
//		// Print out any functions that have a return in the middle
//		console.log(fnString);
//		this.badFunctions++;
//	}
	
	if (fnString.match(/return[^\n]*\n}$/) !== null)
		fnString = fnString.replace(/(return)\s+([^\n\;]*);?[^\n]*\n}$/, "" + this.globalName + ".onFunctionEnd($2)\;\n\t$1 $2\;\n}")
	else
		fnString = fnString.replace(/}$/, "\t" + this.globalName + ".onFunctionEnd()\n}");
	
//	fnString = fnString.replace(/{/, "{\n\tconsole.log('" + cl.name + "::" + fnName + "()', arguments);\n");
	var newFn;
	
	eval("newFn = " + fnString);
	
	eval("cl.prototype." + fnName + " = newFn;");
}

debugFunctionModifier.prototype.onFunctionStart = function(name, arguments)
{

	var preceding = "";
	for (var i = 0; i < this.functionLevel; i++)
		preceding += "   ";
	console.log(preceding + name, arguments);
	this.functionLevel++;
}

debugFunctionModifier.prototype.onFunctionEnd = function(returnVal)
{
	this.functionLevel--;
//	console.log("Return: ", returnVal);
}
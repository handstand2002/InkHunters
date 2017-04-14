function errorDialog()
{
	this.div = document.getElementById("bottomError");
	
	this.alpha = 0;
	this.div.style.opacity = this.alpha/100;
}

errorDialog.prototype.setError = function(text)
{
	this.alpha = 100;
	this.div.style.opacity = this.alpha/100;
	while (this.div.childNodes.length > 0)
		this.div.removeChild(this.div.childNodes[0]);
	
	var newText = document.createTextNode(text);
	this.div.appendChild(newText);
//	console.log("Setting error '" + text + "'");
	window.setTimeout("pageElements.errorController.startFade()", 5000);
}

errorDialog.prototype.startFade = function()
{
	this.fadeOut();
}

errorDialog.prototype.fadeOut = function()
{
	this.alpha -= 2;
	this.div.style.opacity = this.alpha/100;
	if (this.alpha > 0)
		window.setTimeout("pageElements.errorController.fadeOut()", 10);
}
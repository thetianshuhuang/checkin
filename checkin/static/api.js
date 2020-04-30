
function deleteProgram(id, token) {
	fetch("http://" + SERVER + "/api/programs/delete/" + id + "?token=" + token)
	.then(res => res.json())
	.then(out => {console.log(out);})
	.catch(err => {throw err;});
}

function deleteToken(token) {
	fetch("http://" + SERVER + "/api/tokens/delete?token=" + token)
	.then(res => res.json())
	.then(out => {
		console.log(out);
		for(var sf of ['-token', '-controls']) {
			var div = document.getElementById(token + sf);
			div.parentNode.removeChild(div);
		}
	})
	.catch(err => {throw err;});
}


function addToken(target) {
	var desc = document.getElementById(target).value;
	fetch("http://" + SERVER + "/api/tokens/new?desc=" + desc)
	.then(res => res.json())
	.then(out => {
		console.log(out);
		var table = document.getElementById('user-token-table');

		var controls = document.createElement('div');
		controls.className = 'controls';
		controls.setAttribute('id', out.api_token + '-controls');
		table.appendChild(controls);

		var button = document.createElement('button');
		button.className = 'button-icon';
		button.innerHTML = BUTTONS.DELETE;
		button.addEventListener("click", function() {
			deleteToken(out.api_token);
		})
		controls.appendChild(button);
		console.log(out.desc);
		controls.appendChild(document.createTextNode(out.desc));

		var token = document.createElement('div');
		token.className = 'token';
		token.setAttribute('id', out.api_token + '-token');
		table.appendChild(token);
		token.appendChild(createDivText('API'));
		token.appendChild(createDivText(out.api_token));
	})
	.catch(err => {throw err;});
}

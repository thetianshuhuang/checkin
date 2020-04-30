
function deleteProgram(id, token) {
	fetch("http://" + SERVER + "/api/programs/delete/" + id + "?token=" + token)
	.then(res => res.json())
	.then(out => {
		console.log(out);
		destroy("program-table-" + id)
	})
	.catch(err => {throw err;});
}


function deleteToken(token) {
	fetch("http://" + SERVER + "/api/tokens/delete?token=" + token)
	.then(res => res.json())
	.then(out => {
		console.log(out);
		destroy("user-token-" + token);
	})
	.catch(err => {throw err;});
}


function createUserTokenRow(out) {
	var table = document.getElementById('user-token-table');

	var entry = document.createElement("div");
	entry.id = "user-token-" + out.api_token;
	table.appendChild(entry);

	// Title
	var title = document.createElement("div");
	title.className = "token-title";
	entry.appendChild(title);

	events = [
		["DELETE", function() { deleteToken(out.api_token); }],
		["TOGGLE", function() { toggle('user-tokens-' + out.api_token); }]
	];

	for(var s of events) {
		var btn = document.createElement("button");
		btn.addEventListener("click", s[1]);
		btn.innerHTML = BUTTONS[s[0]];
		btn.className = "button-icon";
		title.appendChild(btn);
	}

	var tokenDesc = document.createElement("span");
	tokenDesc.innerHTML = out.desc;
	tokenDesc.style = "padding-left: 8px";
	title.appendChild(tokenDesc);

	// Toggleable API keys
	var toggleTokens = document.createElement("div");
	toggleTokens.id = "user-tokens-" + out.api_token;
	toggleTokens.className = "token";
	toggleTokens.style = "display: none";
	entry.appendChild(toggleTokens);

	for(var t of ["API", out.api_token]) {
		var d = document.createElement("div");
		d.innerHTML = t;
		toggleTokens.appendChild(d);
	}
}


function getTokens() {
	fetch("http://" + SERVER + "/api/tokens/list")
	.then(res => res.json())
	.then(out => {
		console.log(out);
		for(var token of out.tokens) {
			createUserTokenRow(token);
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
		createUserTokenRow(out);
	})
	.catch(err => {throw err;});
}

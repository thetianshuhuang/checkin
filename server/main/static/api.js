
function deleteProgram(id, token) {
	fetch("http://localhost:8000/api/records/delete/" + id + "?token=" + token)
	.then(res => res.json())
	.then(out => {console.log(out);})
	.catch(err => {throw err;});
}

function deleteToken(token) {
	fetch("http://localhost:8000/api/tokens/delete?token=" + token)
	.then(res => res.json())
	.then(out => {console.log(out);})
	.catch(err => {throw err;});
}

function addToken(target) {
	var desc = document.getElementById(target).value;
	fetch("http://localhost:8000/api/tokens/new?desc=" + desc)
	.then(res => res.json())
	.then(out => {console.log(out);})
	.catch(err => {throw err;});
}

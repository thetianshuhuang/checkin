/**
 *
 *
 */



RECORDS = {};
RECOMPUTE_PROGRESS = false;





function update_elem(data, element) {
	if(element in data) {
		var tgt = document.getElementById(data.record_id + "-" + element);
		tgt.innerHTML = data[element];
	}
}


function update_icon(data, icon) {
	// In progress, not yet running
	if(!data.start) {
		icon.innerHTML = ICONS['WAITING'];
	} else if(!data.end) {
		icon.innerHTML = ICONS['RUNNING'];
	} else {
		icon.innerHTML = ICONS[data.type];
	}
}


function get_progress(data) {
	if(("progress" in data) && data.progress) {
		return Math.min(data.progress, 1) * 100;
	}
	else {
		var total = 0;
		var progress = 0;
		for(i of data.children) {
			if(i.type == 'TASK') {
				total += 1;
				var child = data.children[i];
				if(("progress" in child) && child.progress) {
					progress += child.progress;
				} else if("progress_computed" in child) {
					progress += progress_computed;
				}
			}
		}
		if(total > 0) {
			data.progress_computed = progress / total;
		} else {
			data.progress_computed = (data.end ? 1 : 0);
		}
		return Math.min(data.progress_computed, 1) * 100;
	}
}


function draw(parent, current) {

	var data = RECORDS[current];

	if(document.getElementById(current)) {

		update_elem(data, 'name');
		update_elem(data, 'progress');
		update_elem(data, 'desc');

		if(data.type == 'TASK') {
			var pbar = document.getElementById(data.record_id + "-progress-done");
			pbar.style.width = get_progress(data) + "%";
		}

		if(("start" in data) || ("end" in data)) {
			update_icon(
				data, document.getElementById(data.record_id + "-name-icon"));
		}
	}
	else {

		var c = new DOMConstructor(data.record_id);
		var parent = document.getElementById(parent + "-children");

		// Make container
		var container = c.makeDiv(parent, "container", "record");

		if(data.type != 'ROOT') {
			var button = c.makeDiv(container, "collapse", "button-collapse");
			button.appendChild(document.createTextNode("-"));
			button.addEventListener("click", function() {
				this.innerHTML = (this.innerHTML == "+" ? "-" : "+");
				toggle(data.record_id + "-children");
			});
		}

		// Content
		var content = c.makeDiv(container, "content", "content-block");

		// Metadata
		var metadata = c.makeDiv(content, "metadata", "metadata-block");

		// Name
		var name_ctr = c.makeDiv(metadata, "name-ctr", "metadata-name");
		
		// Icon
		var name_icon = c.makeDiv(name_ctr, "name-icon", "metadata-name-icon");
		update_icon(data, name_icon);

		// Actual name text
		var name = c.makeDiv(name_ctr, "name", "metadata-name-text");
		name.appendChild(document.createTextNode(data.name));

		// Progress bar (if task)
		if(data.type == 'TASK' || data.type == 'ROOT') {
			var progress = c.makeDiv(metadata, "progress", "progress");
			c.makeDiv(progress, "progress-done", "progress-done");
			pbar.style.width = get_progress(data) + "%";
		}

		// Children
		var children = c.makeDiv(content, "children", "children-block");

		// Desc
		var desc = c.makeDiv(children, "desc", "metadata-desc");
		desc.appendChild(document.createTextNode(data.desc));
	}

	if(data.children) {
		data.children.forEach(function(child) {
			draw(data.record_id, child);
		});
	}
}


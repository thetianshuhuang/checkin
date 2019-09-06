
ICONS = {
	"INFO": '<svg fill="var(--info)" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>',
	"ERR": '<svg fill="var(--error)" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/></svg>',
	"WARN": '<svg fill="var(--warning)" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/></svg>',
	"TASK": '<svg fill="var(--done)" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="none" d="M0 0h24v24H0z"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/></svg>',
	"TASK_PARENT": '<svg fill="var(--done)" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M0 0h24v24H0z" fill="none"/><path d="M18 7l-1.41-1.41-6.34 6.34 1.41 1.41L18 7zm4.24-1.41L11.66 16.17 7.48 12l-1.41 1.41L11.66 19l12-12-1.42-1.41zM.41 13.41L6 19l1.41-1.41L1.83 12 .41 13.41z"/></svg>',
	"WAITING": '<div class="waiting"></div>',
	"RUNNING": '<div class="loader"></div>',
}


class DOMConstructor {
	constructor(id_base) {
		this.id_base = id_base;
	}
	makeDiv(parent, type, classname) {
		var div = document.createElement("div");
		div.className = classname;
		div.setAttribute("id", this.id_base + "-" + type);
		parent.appendChild(div);

		return div;
	}
}

function toggle(id) {
	var elem = document.getElementById(id);
	elem.style.display = (elem.style.display === "none" ? "block" : "none");
}


class Program {
	constructor(container) {
		this.records = {};

		this.progress = {};
		this.totals = {};

		this.container = document.getElementById(container);
		this.recompute_progress = false;
	}

	/**
	 * Check for progress recompute
	 */
	checkProgress(data) {
		var is_progress_update = (
			(data.type == 'TASK') &&
			(("progress" in data) || ("end" in data)));
		if(is_progress_update) { this.recompute_progress = true; }
	}

	updateRecords(data) {
		for(var record of data) { this.updateRecord(record); }

		if(this.recompute_progress) {
			this.computeProgress();
			for(var x of Object.keys(this.records)) { this.drawUpdate(x); }
		}
	}

	/**
	 * Update Record
	 */
	updateRecord(data) {

		// Record already exists
		if(data.record_id in this.records) {
			for(var key of Object.keys(data)) {
				this.records[data.record_id][key] = data[key];
			}
		}
		// New record
		else {
			this.records[data.record_id] = data;
		}
		// Check if progress recompute is necessary
		this.checkProgress(data);
	}

	/**
	 * Compute progress
	 */
	computeProgress() {
		this.progress = {};
		this.totals = {};

		for(var id of Object.keys(this.records)) {
			var data = this.records[id];
			if(data.type == 'TASK') {
				var p = data.parent;

				if(!(p in this.totals)) { this.totals[p] = 0; }
				if(!(p in this.progress)) { this.progress[p] = 0; }

				if(data.end) { this.progress[p] += 1; }
				this.totals[p] += 1;
			}
		}
	}

	/**
	 * Check if container exists
	 */
	exists(id) {
		return document.getElementById(id + '-children');
	}

	/**
	 * Update element
	 */
	updateElem(id, key) {
		var tgt = document.getElementById(id + '-' + key);
		tgt.innerHTML = this.records[id][key];
	}

	/**
	 * Get progress
	 */
	getProgress(id) {
		// Has end time -> 1
		if(this.records[id].end) { return 1; }
		// Not computed -> 0
		else if(!(id in this.progress) || !(id in this.totals)) { return 0; }
		// No subtasks -> 0
		else if(this.totals[id] == 0) { return 0; }
		// Return progress -> progress / total
		else { return Math.min(1, this.progress[id] / this.totals[id]); }
	}

	/** 
	 * Update progress bar
	 */
	updateProgress(id) {
		var progress = this.getProgress(id) * 100 + "%"

		var pbar = document.getElementById(id + '-progress-done');
		pbar.style.width = progress;
		
		var ptext = document.getElementById(id + "-progress-text");
		var complete = (id in this.progress ? this.progress[id] : 0);
		var total = (id in this.totals ? this.totals[id] : 0);

		ptext.innerHTML = progress + " [" + complete + "/" + total + "]";
	}

	/**
	 * Update record icon
	 */
	updateIcon(id) {
		var data = this.records[id];

		var icon_name;
		if(!data.start) { icon_name = 'WAITING'; }
		else if(!data.end) { icon_name = 'RUNNING'; }
		else if(this.totals[id] > 0) { icon_name = 'TASK_PARENT'; }
		else { icon_name = data.type; }

		var icon = document.getElementById(id + '-name-icon');
		if(icon.innerHTML != ICONS[icon_name]) {
			icon.innerHTML = ICONS[icon_name]
		};
	}

	/**
	 * Update a single record (draw)
	 */
	drawUpdate(id) {

		var data = this.records[id];

		if(!this.exists(id)) {
			// Make sure parent exists
			if(!this.exists(data.parent)) { this.drawUpdate(data.parent); }

			// Draw
			var c = new DOMConstructor(data.record_id);
			var parent = document.getElementById(data.parent + "-children");

			var container = c.makeDiv(parent, "container", "record");

			// Collapse button
			var button = c.makeDiv(container, "collapse", "button-collapse");
			button.appendChild(document.createTextNode("-"));
			button.addEventListener("click", function() {
				this.innerHTML = (this.innerHTML == "+" ? "-" : "+");
				toggle(data.record_id + "-children");
			});

			var content = c.makeDiv(container, "content", "content-block");
			var metadata = c.makeDiv(content, "metadata", "metadata-block");
			var name_ctr = c.makeDiv(metadata, "name-ctr", "metadata-name");
			var name_icon = c.makeDiv(name_ctr, "name-icon", "metadata-icon");
			var name = c.makeDiv(name_ctr, "name", "metadata-name-text");
			var progress_percent = c.makeDiv(name_ctr, "progress-text", "progress-text");

			// Progress bar (if task)
			if(data.type == 'TASK') {
				var progress = c.makeDiv(metadata, "progress", "progress");
				var pbar = c.makeDiv(progress, "progress-done", "progress-done");
			}

			var children = c.makeDiv(content, "children", "children-block");
			var desc = c.makeDiv(children, "desc", "metadata-desc");

		}

		this.updateElem(id, 'name');
		this.updateElem(id, 'desc');

		this.updateIcon(id);

		if(data.type == 'TASK') {
			this.updateProgress(id);
		}
	}
}



class RecordConstructor {
	constructor(id_base) {
		this.id_base = id_base;
	}
	makeDiv(parent, type) {
		var div = document.createElement("div");
		div.className = "record-" + type;
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
	 * @typedef ProgramRecord
	 * @type {Object}
	 * @property {str} node_id - ID of originating compute node
	 * @property {str} record_id - ID of record
	 * @property {str} parent - ID of record parent
	 * @property {str} name - Record name
	 * @property {str} desc - Record description
	 * @property {str} type - Record type; TASK|ERR|WARN|INFO|META
	 * @property {number} start - Record start datetime; POSIX time
	 * @property {number} end - Record end datetime; POSIX time
	 * @property {Object} meta - metadata object
	 */

	/**
	 * Check for progress recompute
	 * @param {ProgramRecord} record - single record
	 */
	checkProgress(record) {
		var is_progress_update = (
			(record.type == 'TASK') &&
			(("progress" in record) || ("end" in record)));
		if(is_progress_update) { this.recompute_progress = true; }
	}

	/**
	 * Add a single new record
	 * @param {ProgramRecord} record - single record
	 */
	updateRecord(record) {
		// Record already exists
		if(record.record_id in this.records) {
			for(var key of Object.keys(record)) {
				this.records[record.record_id][key] = record[key];
			}
		}
		// New record
		else { this.records[record.record_id] = record; }

		// Check if progress recompute is necessary
		this.checkProgress(record);
	}

	/**
	 * Update records
	 * @param {ProgramRecord[]} records - list of records to update
	 */
	updateRecords(records) {
		for(var record of records) { this.updateRecord(record); }

		if(this.recompute_progress) {
			this.computeProgress();
			for(var x of Object.keys(this.records)) { this.drawUpdate(x); }
		}
	}

	/**
	 * Compute progress for all stored records
	 */
	computeProgress() {
		this.progress = {};
		this.totals = {};

		for(var id of Object.keys(this.records)) {
			var record = this.records[id];
			if(record.type == 'TASK') {
				var p = record.parent;

				if(!(p in this.totals)) { this.totals[p] = 0; }
				if(!(p in this.progress)) { this.progress[p] = 0; }

				if(record.end) { this.progress[p] += 1; }
				this.totals[p] += 1;
			}
		}
	}

	/**
	 * Check if container exists
	 * @param {str} id - record ID to check
	 * @return {Object} Fetched element. Check null the same way as a boolean.
	 */
	exists(id) {
		return document.getElementById(id + '-children');
	}

	/**
	 * Update element; only redraws if the values change (in case more complex
	 * HTML is involved such as animations)
	 * @param {str} id - record ID to check
	 * @param {str} key - ProgramRecord key to update
	 */
	updateElem(id, key) {
		var tgt = document.getElementById(id + '-' + key);
		var new_val = this.records[id][key];
		if(tgt.innerHTML != new_val) { tgt.innerHTML = new_val; }
	}

	/**
	 * Get progress
	 * @param {str} id - record ID to check
	 * @return {number} Progress, in [0, 1]
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
	 * @param {str} id - record ID to update progress for
	 */
	updateProgress(id) {
		var progress = this.getProgress(id) * 100 + "%"

		// Fetch progress bar; return immediately if does not exist
		var pbar = document.getElementById(id + '-progress-done');
		if(!pbar) { return; }
		pbar.style.width = progress;
		
		// Update progress text
		var ptext = document.getElementById(id + "-progress-text");
		var complete = (id in this.progress ? this.progress[id] : 0);
		var total = (id in this.totals ? this.totals[id] : 0);
		ptext.innerHTML = progress + " [" + complete + "/" + total + "]";
	}

	/**
	 * Update record icon
	 * @param {str} id - record to update icon for
	 */
	updateIcon(id) {
		var record = this.records[id];

		var icon_name;
		if(!record.start) { icon_name = 'WAITING'; }
		else if(!record.end) { icon_name = 'RUNNING'; }
		else if(this.totals[id] > 0) { icon_name = 'TASK_PARENT'; }
		else { icon_name = record.type; }

		var icon = document.getElementById(id + '-icon');
		if(icon.innerHTML != ICONS[icon_name]) {
			icon.innerHTML = ICONS[icon_name]
		};
	}

	/**
	 * Create new record
	 * @param {ProgramRecord} record - record to create
	 */
	createRecordDiv(record) {

		// Draw
		var c = new RecordConstructor(record.record_id);
		var parent = document.getElementById(record.parent + "-children");

		var container = c.makeDiv(parent, "container");
		var button = c.makeDiv(container, "collapse");
		var content = c.makeDiv(container, "content");
		var metadata = c.makeDiv(content, "metadata");
		var header = c.makeDiv(metadata, "header");
		c.makeDiv(header, "icon");
		c.makeDiv(header, "name");
		c.makeDiv(header, "progress-text");
		var children = c.makeDiv(content, "children");
		c.makeDiv(children, "desc");

		// Collapse button
		button.appendChild(document.createTextNode("-"));
		button.addEventListener("click", function() {
			this.innerHTML = (this.innerHTML == "+" ? "-" : "+");
			toggle(record.record_id + "-children");
		});

		// Progress bar (if task)
		if(record.type == 'TASK') {
			var progress = c.makeDiv(metadata, "progress");
			var pbar = c.makeDiv(progress, "progress-done");
		}
	}

	/**
	 * Update a single record (draw)
	 */
	drawUpdate(id) {

		var record = this.records[id];

		// Record isn't drawn -> create new
		if(!this.exists(id)) {
			// Make sure parent exists
			if(!this.exists(record.parent)) { this.drawUpdate(record.parent); }
			// Create record div
			this.createRecordDiv(record);
		}

		// Update elements
		this.updateElem(id, 'name');
		this.updateElem(id, 'desc');

		this.updateIcon(id);

		if(record.type == 'TASK') {
			this.updateProgress(id);
		}
	}
}

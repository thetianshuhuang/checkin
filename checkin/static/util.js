

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
    makeDivs(parent, types) {
        var res = [];
        for(var t of types) { res.push(this.makeDiv(parent, t)); }
        return res;
    }
}

function toggle(id) {
    var elem = document.getElementById(id);
    elem.style.display = (elem.style.display === "none" ? "block" : "none");
}

function destroy(id) {
    var elem = document.getElementById(id);
    element.parentNode.removeChild(element);
}

function createDivText(txt) {
    var div = document.createElement('div');
    var text = document.createTextNode(txt);
    div.appendChild(text);
    return div;
}

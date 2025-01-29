'use strict'
let type;

function change(m) {
	if (m.matches) {
		let t = document.getElementById("title");
		t.innerHTML = "<span translate='no' class='material-symbols-outlined ico-btn' onclick='showMenu()'>menu</span>";
		let a = document.getElementsByClassName("nav-btn");
		for (let i = 0; i < a.length; i++) {
			a[i].style = "display: none";
		}

		if (document.getElementById("table") != null) {
			let rotate = document.createElement("div");
			rotate.setAttribute("style", "display: flex; align-items: center; flex-direction: column");
			rotate.innerHTML = "<h1>Rotate your device&ensp;<span translate='no' class='material-symbols-outlined' style='font-size: larger'>screen_rotation</span></h1><h2 style='font-size: small'>If you have already rotated your device, or you are not using a mobile device, then the device is not compatible</h2>";
			document.getElementsByTagName("main")[0].appendChild(rotate);
		}
	} else {
		document.getElementById("title").innerHTML = "<h1>Fantastic MASs and where to find them</h1>"
		let a = document.getElementsByClassName("nav-btn");
		for (let i = 0; i < a.length; i++) {
			a[i].style = "";
		}

		if (document.getElementById("table") != null) {
			let main = document.getElementsByTagName("main")[0];
			main.removeChild(main.childNodes[main.childNodes.length - 1]);
		}
	}
}

function showMenu() {
	let a = document.getElementsByClassName("nav-btn");
	let t = document.getElementById("title");
	t.innerHTML = "<span translate='no' class='material-symbols-outlined ico-btn' onclick='hideMenu()'>close</span>";
	for (let i = 0; i < a.length; i++) {
		a[i].style = "";
	}
}

function hideMenu() {
	let a = document.getElementsByClassName("nav-btn");
	let t = document.getElementById("title");
	t.innerHTML = "<span translate='no' class='material-symbols-outlined ico-btn' onclick='showMenu()'>menu</span>";
	for (let i = 0; i < a.length; i++) {
		a[i].style = "display: none";
	}
}

function filter(f) {
	f = f.toLowerCase();
	if (
		f.startsWith("name:") ||
		f.startsWith("community-availabilty:") ||
		f.startsWith("license:") ||
		f.startsWith("real-application:") ||
		f.startsWith("list-of-bugs:") 
	) {
		f = f.substring(f.indexOf(":") + 1);
	}
	let attribute = document.getElementById("search-filter").value;
	let column;
	let rows;

	if (attribute == "none") {
		rows = document.getElementsByClassName("t-row");
		for (let i = 0; i < rows.length; i++) {
			if (!rows[i].innerText.toLowerCase().includes(f)) rows[i].setAttribute("style",  "display: none");
			else rows[i].setAttribute("style", "")
		}
		return;
	} else if (attribute == "name") {
		column = document.getElementsByClassName("t-value t-projectName");
	} else if (attribute == "community-availabilty") {
		if (type == 0)
			column = document.getElementsByClassName("t-value t-frameworkCommunityAvailability");
		else if (type == 1)
			column = document.getElementsByClassName("t-value t-masCommunityAvailability");
		else 
			column = document.getElementsByClassName("t-value t-extensionCommunityAvailbility");
	} else if (attribute == "license") {
		if (type == 0)
			column = document.getElementsByClassName("t-value t-frameworkLicense");
		else if (type == 1)
			column = document.getElementsByClassName("t-value t-masLicense");
		else 
			column = document.getElementsByClassName("t-value t-extensionLicense");
	} else if (attribute == "list-of-bugs") {
		if (type == 0)
			column = document.getElementsByClassName("t-value t-frameworkListOfBugs");
		else if (type == 1)
			column = document.getElementsByClassName("t-value t-masListOfBugs");
		else 
			column = document.getElementsByClassName("t-value t-extensionListOfBugs");
	} else if (attribute == "real-application") {
		if (type == 0)
			column = document.getElementsByClassName("t-value t-frameworkRealApplication");
		else if (type == 1)
			column = document.getElementsByClassName("t-value t-masRealApplication");
		else 
			column = document.getElementsByClassName("t-value t-extensionRealApplication");
	}

	rows = document.getElementsByClassName("t-row");
	for (let i = 0; i < rows.length; i++) {
		if (!column[i].innerText.toLowerCase().includes(f)) rows[i].setAttribute("style",  "display: none");
		else rows[i].setAttribute("style", "")
	}

}

window.addEventListener('load', async () => {
	let title = document.title;
	
	if (title == "Frameworks") type = 0
	else if (title == "Mas") type = 1
	else type = 2

	let mobileVersion = window.matchMedia("(max-width: 620px)");
	change(mobileVersion);
	mobileVersion.addListener(change);

	let table = document.getElementById("table");
	
	if(table != null) {
		let srch = document.getElementById("search-field");
		let filt = document.getElementById("search-filter");

		srch.addEventListener('keypress', (evt) => {
			if (evt.which === 13) {
				evt.preventDefault();
			}
		});

		srch.onkeyup = () => {
			if (
				srch.innerText.startsWith("name:") ||
				srch.innerText.startsWith("community-availability:") ||
				srch.innerText.startsWith("license:") ||
				srch.innerText.startsWith("real-application:") ||
				srch.innerText.startsWith("list-of-bugs:") 
			) {
				if (srch.getElementsByTagName("span").length == 0) {
					srch.innerHTML = "<span translate='no' style='color:var(--light1-color)'>" + srch.innerHTML.substring(0, srch.innerHTML.indexOf(":")) + "</span>" + srch.innerHTML.substring(srch.innerHTML.indexOf(":"));
					let range = document.createRange()
					let sel = window.getSelection()
					
					range.setStart(srch.childNodes[1], 1);
					range.collapse(true);
					
					sel.removeAllRanges();
					sel.addRange(range);

					filt.value = srch.getElementsByTagName("span")[0].innerText;
				}
			} else {

				if (srch.childNodes.length != 0) {
					srch.innerHTML = srch.innerText;
					let range = document.createRange()
					let sel = window.getSelection()
					
					range.setStart(srch.childNodes[0], srch.innerText.length);
					range.collapse(true);
					
					sel.removeAllRanges();
					sel.addRange(range);
				}

				filt.value = "none";
			}
			filter(srch.innerText)
		};

		filt.onchange = () => {
			if(filt.value == "none") {
				let sp = srch.getElementsByTagName("span");
				if (sp.length != 0) {
					srch.removeChild(sp[0]);
					srch.innerText = srch.innerText.substring(1);
				}
			} else {
				let sp = srch.getElementsByTagName("span");
				if (sp.length != 0) {
					sp[0].innerText = filt.value;
				} else {
					srch.innerText = filt.value + ":" + srch.innerText;
					srch.onkeyup();
				}
			}
		}

		let t = await fetch('src/data.json');
		let row = 0;
		t = await t.json();
		let isVoid = true;
		const link = /https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)/;
		const email = /[\w\.]+@([\w-]+\.)+[\w-]{2,4}/;
		t.sort(function (a, b) {
			return a.projectName.localeCompare(b.projectName);
		});
		t.forEach(e => {
			if (e["frameworkMasExtension"] == type) {
				isVoid = false;
				delete e["frameworkMasExtension"];
				table.innerHTML += "<div class='t-row' id='t-row-" + row + "'></div>";
				let r = document.getElementById("t-row-" + row++);
				let tmpStr = "";
				for (let k in e) {
					tmpStr = e[k];
					if (typeof(e[k]) == "string") {
						tmpStr = e[k].split(/(\(|\)| )/g).map(j => {
							if (link.test(j))
								return "<a href='" + j + "' title='" + j + "'>" + j + "</a>"
							else if (email.test(j))
								return "<a href='mailto:" + j + "' title='" + j + "'>" + j + "</a>"
							else return j
						}).join(" ")
					}
					
					r.innerHTML += "<div class='t-value t-" + k + "' title='" + e[k] + "'>" + tmpStr + "</div>";
				}
			}
		});
		if (isVoid) {
			let t = document.getElementsByTagName("main")[0];
			t.innerHTML = `<h1 style="min-height: 80vh; margin-top: 20px">There are no ${title.toLowerCase()} yet</h1>`;
		}
	}
})

window.addEventListener('load', () => {
	table.onscroll = () => {
		let x = document.getElementsByClassName("t-head")[0];
		console.log(x.style)
		let rec = document.getElementsByClassName("t-row")[0].getBoundingClientRect();
		console.log(rec)
		x.style.transform = `translateX(${rec.left}px)`
	}
})

// let dishes_list = {}
// document.cookie = "dishes=" + JSON.stringify(dishes_list); 

init()

function set_amounts() {
	let items = document.getElementsByClassName("amount") 

	for (let item of items) {
		let item_id = item.nextElementSibling.id
		cookie = JSON.parse(getCookie("dishes"))

		if (cookie[item_id] != null) {
			item.textContent = cookie[item_id]
		}
		console.log(item.textContent)
	}
}


function add_dish(n) {
	let dishes = document.getElementsByClassName("id");
	let dishes_list = JSON.parse(getCookie("dishes"))

	if (dishes_list[n] == null) {
		dishes_list[n] = 1
	} else {
		dishes_list[n] += 1
	}

	document.getElementById(n).nextElementSibling.textContent = dishes_list[n]

	document.cookie = "dishes=" + JSON.stringify(dishes_list); 
	console.log(document.cookie); 
}

function unadd_dish(n) {
	let dishes = document.getElementsByClassName("id");
	let dishes_list = JSON.parse(getCookie("dishes"))

	if (dishes_list[n] == null || dishes_list[n] == 0) {
		return
	} else {
		dishes_list[n] -= 1
	}

	document.getElementById(n).nextElementSibling.textContent = dishes_list[n]

	document.cookie = "dishes=" + JSON.stringify(dishes_list); 
	console.log(document.cookie); 
}

function getCookie(name) {
  let matches = document.cookie.match(new RegExp(
    "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
  ));
  return matches ? decodeURIComponent(matches[1]) : undefined;
}

function init() {
	let dishes_list = {}

	if (getCookie("dishes") == null) {
		document.cookie = "dishes=" + JSON.stringify(dishes_list); 
	}
	set_amounts()
}
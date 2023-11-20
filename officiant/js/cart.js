function gen_cards() {
	let dishes_list = JSON.parse(getCookie("dishes"));
	let orders_div = document.getElementsByClassName("orders");


	for (const [key, value] of Object.entries(dishes_list)) {
		if (value != 0) {
			orders_div[0].innerHTML += `<div class="orders__order"><span class="order__name">Название блюда</span><div class="order__info"><span class="order__cost">1900$</span><span class="order__amount">${value}</span><span class="hint">шт.</span></div></div>`;
		}
	}
}

gen_cards();
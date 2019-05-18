	// задаем функцию с двумя параметрами
	function filter_results(form, results_container, ur, met){
		if (met === undefined) {
   			met = "GET";
  		}
		//инициализация запроса к серверу
		$.ajax({
				url: ur, // url для запроса
				method: met, // метод GET, POST, ...
				data: $(form).serialize(), // метод Jquery для сериализации
				dataType: "html", //тип контента, что мы ожидаем получить
				success: function(data){ // вызывается, кода тип контента совпадает с пришедшим от сервера
					console.log(data);
					let html = data; 
					let results = $(html).find(results_container); // находим в пришедшем html элемент с id (пааметр функции)
					if (results.length){ //проверка, есть ли этот элемент в html
						$(results_container).html(results); //заменяем содержимое элемента содержимым, которое пришло от сервера
					}
				},
				error: function(data){
					console.log(data);
				}
			}
			)		
	}
$(document).ready(function () {
    var counter = 0;
    var records;
    const ulFilter = document.getElementById("filter-list");
    const ulResults = document.getElementById("results-cards");
    const text = document.getElementById("search-text");
    const quantity = document.getElementById("quantity");
    const Url = "/ai/api/search/";
    

    $('#search-btn').click(function () {
        var keywords = [];

        if (ulFilter.hasChildNodes()) {
            for (item of ulFilter.children) {
                keywords.push(item.firstChild.value)
            }

        }

        const data = {
            text: text.value,
            keywords: keywords,
            quantity: quantity.value
        }

        $("#results-title").text("");
        $("#results-status").text("");
        $("#loader-spinner").removeAttr("hidden");

        if (ulResults.hasChildNodes()) {
            $("#results-cards").empty();
        }

        $.ajax({
            url: Url,
            data: JSON.stringify(data),
            dataType: "json",
            contentType: "application/json",
            type: "POST",
            success: function (data) {
                $("#results-title").text("Resultados");
                $("#results-status").text("Busqueda Completada");
                records = data['records']
                console.log(records)

                // records = JSON.parse(data['records']);
                var card = "";
                var match = "";
                var updateData = "";
                // console.log(records)


                if (records.length === 0) {
                    $("#results-status").text("No se han encontrado canditados adecuados");
                }

                for (var i = 0; i < records.length; i += 1) {

                    if (records[i]['similarity'] >= Number(0.83)) {
                        match = "\u2658\u2658\u2658";
                    } else if (records[i]['similarity'] > Number(0.81) && records[i]['similarity'] < Number(0.83)) {
                        match = "\u2658\u2658";
                    } else {
                        match = "\u2658";
                    }

                    updateData = records[i]['updated_at'].split("T")[0]
                    card = `<a href="${records[i]['web_url']}" target="_blank"><figure><div class="card"><div><h3>${match}</h3></div><div><h4>${records[i]['filename']}</h4></div><div><p>Última modificación: ${updateData}</p></div></div><div class="abstract"><p>${records[i]['abstract']}</p></div></figure></a>`;
                    
                    // `<a href="${records[i]['web_url']}" target="_blank"><div class="card"><div><h3>${match}</h3></div><div><h4>${records[i]['filename']}</h4></div><div><p>Última modificación: ${updateData}</p></div></div></a>`;
                    // row = `<tr><td><a href="${records[i]['web_url']}" target="_blank">${records[i]['filename']}</a></td><td>${records[i]['updated_at']}</td><td>`;

                    // row += "</td></tr>";

                    $("#results-cards").append(card);
                }
                $("#loader-spinner").attr("hidden", "");

            },
            error: function (error) {
                console.log(`Error ${error}`)
                $("#results-status").text("An error has ocurred during search_text process");
            }
        })
    });

    $("#add-filter").click(function () {
        $("#filter-list").append('<li><input type="text" class="form-control" aria-describedby="searchHelp"></li>');
        counter += 1;
    });

    $("#remove-filter").click(function () {
        if (ulFilter.hasChildNodes()) {
            ulFilter.removeChild(ulFilter.lastChild);
        }
        if (counter > 0) {
            counter -= 1;
        }

    });

});
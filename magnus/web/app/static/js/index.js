$(document).ready(function () {
    var counter = 0;
    const ulFilter = document.getElementById("filter-list");
    const ulResults = document.getElementById("results-table-body");
    const text = document.getElementById("search-text");
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
            keywords: keywords
        }

        $.ajax({
            url: Url,
            data: JSON.stringify(data),
            dataType: "json",
            contentType: "application/json",
            type: "POST",
            success: function (data) {
                $("#results-status").text("Search completed.");
                console.log(data)

                var records = JSON.parse(data['records']);

                console.log(records)

                if (ulResults.hasChildNodes()) {
                    $("#results-table-body").empty();
                }

                for (var i = 0; i < records.length; i += 1) {
                    $("#results-table-body").append(`<tr><td><a href="${records[i]['web_url']}" target="_blank">Perfil ${i + 1}</a></td><td>${records[i]['updated_at']}</td><td>${records[i]['similarity']}</td></tr>`);
                }

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
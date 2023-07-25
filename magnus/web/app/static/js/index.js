$(document).ready(function () {
    var counter = 0;
    const ulFilter = document.getElementById("filter-list");
    const ulResults = document.getElementById("filter-list");
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
            success: function (response) {
                console.log(response)

                if (ulResults.hasChildNodes()) {
                    $("#results-list").empty();
                }

                for (key of keywords) {
                    $("#results-list").append(`<li>${key}</li>`);
                }

            },
            error: function (error) {
                console.log(`Error ${error}`)
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